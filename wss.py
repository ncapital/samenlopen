import hashlib
import hmac
import json
import socket
import time

import arrow
from websocket import create_connection, WebSocket, WebSocketConnectionClosedException


#
from arbi.exchanges.cex.config import CexConfig


class MyWebSocket(WebSocket):
    def recv_frame(self):
        frame = super().recv_frame()
        return frame
        # print('yay! I got this frame: ', frame)


def on_message(ws, msg):
   print(msg)


def on_error(ws, err):
    raise err


def on_close(ws):
    raise Exception(f'ws is closed!')

origin = "https://test.io"
last_sent = arrow.utcnow()

while True:
    print('connecting..')
    ws = create_connection('wss://ws.test.io/ws/', header={"User-Agent": "cexio/1.0b"}, origin=origin,
                           sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),), class_=MyWebSocket)

    msg = ws.recv()
    assert "connected" in msg
    # import IPython;IPython.embed()

    ts = arrow.utcnow().timestamp
    message = f"{ts}{CexConfig.KEY}"
    signature = hmac.new(CexConfig.SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    msg = {'e': 'auth',
           'auth': {'key': CexConfig.KEY, 'signature': signature, 'timestamp': ts},
           'oid': 'auth'}

    ws.send(json.dumps(msg))
    print(ws.recv())

    for pair in config.pairs:
        coin1, coin2 = pair.split(':')
        msg = {"e": "subscribe", "rooms": [f"pair-{coin1}-{coin2}"]}  # get some test data
        ws.send(json.dumps(msg))

    try:
        while True:
            msg = ws.recv()
            if 'ping' in msg.lower():
                print(f"[{arrow.utcnow().float_timestamp}] incoming ping")
                ws.send(json.dumps({"e": "pong"}))
                time.sleep(0.01)

            if (arrow.utcnow() - last_sent).seconds > 20:
                ws.send(json.dumps({
                    "e": "get-balance",
                    "oid": "test-data"
                }))
                print(f"[{arrow.utcnow().float_timestamp}] sent balance")
                time.sleep(0.01)
                last_sent = arrow.utcnow()

    except (WebSocketConnectionClosedException, TimeoutError) as e:
        print(f'connection dropped {str(e)[:200]}')
        pass

    except Exception as e:
        print(f"[{arrow.utcnow().float_timestamp}] {e}")
        raise e
