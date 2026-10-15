#!/usr/bin/env python3
import os
import time

pid = os.fork()
if pid == 0:
    print(f"[child]  pid={os.getpid()} завершаюсь сразу")
    os._exit(0)

print(f"[parent] pid={os.getpid()}, ребёнок pid={pid}. wait() НЕ вызываю")
time.sleep(1)
print("--- ps: ребёнок должен быть зомби (Z) ---")
os.system(f"ps -o pid,ppid,stat,cmd -p {pid}")

time.sleep(20)   # окно, чтобы успеть выполнить ps вручную в другом терминале

os.waitpid(pid, 0)   # теперь пожинаем зомби
print("--- после waitpid ---")
os.system(f"ps -o pid,ppid,stat,cmd -p {pid}")