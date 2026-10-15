#!/usr/bin/env python3
import os
import time

pid = os.fork()
if pid > 0:
    print(f"[parent] pid={os.getpid()}, ребёнок={pid}. Родитель завершается")
    os._exit(0)

print(f"[child]  pid={os.getpid()}, ppid до: {os.getppid()}")
time.sleep(3)
new_ppid = os.getppid()
print(f"[child]  ppid после: {new_ppid}")
os.system(f"ps -o pid,ppid,stat,cmd -p {new_ppid}")
print("--- PID 1 в этой системе ---")
os.system("ps -o pid,cmd -p 1")
time.sleep(1)