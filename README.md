# samenlopen
An innovative way to orchestrate multiple processes in an efficient manner

Disclaimer:
Northern Capital provides with this code as is and is not responsible for any damage caused by it, in any way.

# Concept
Occassionally comes the need to run multiple processes within a program. Very often do these subprocesses need access to a shared resource. Indeed, this is an old topic and many common solutions have been written about it, from mutexe (mutual exclusion), locks, semaphors and locks. These solutions work well for either subprocesses, threads or coroutines.
However, all these processes work either within the big process, or between 2 (or more) processes.
The issue arises when one wants to have multiple threads/coroutines within multiple processes so that each of the threads/coros can access an asset **outside its big process**.
The following diagram simulates the problem visually.

![diagram](https://github.com/ncapital/samenloop/blob/master/diagram.png?raw=true)

This is an extrapulation of a previously disucssed matter in computer-science, in order to innovate towards a wholistic solution.

We hope you enjoy and make use of the tool. Please star/watch the repository if you like it.
Also feel free to open a pull-request with features, or send a message if you'd like to receive more info/instructions.
