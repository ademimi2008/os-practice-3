#!/usr/bin/env python3
import os


def mem(pid="self"):
    res = {}
    with open(f"/proc/{pid}/status") as f:
        for line in f:
            if line.startswith("VmRSS:"):
                res["RSS"] = int(line.split()[1])
    with open(f"/proc/{pid}/smaps_rollup") as f:
        for line in f:
            for key in ("Pss:", "Private_Dirty:", "Shared_Dirty:"):
                if line.startswith(key):
                    res[key[:-1]] = int(line.split()[1])
    return res


def show(title, m):
    print(f"{title:<28} " + "  ".join(f"{k}={v} kB" for k, v in m.items()))


N = 5_000_000
big = list(range(N))                 # большой список, создаётся в родителе
show("[parent] до fork", mem())

pid = os.fork()
if pid == 0:
    show("[child]  сразу после fork", mem())
    for i in range(N):               # меняем весь список
        big[i] += 1
    show("[child]  после изменения", mem())
    os._exit(0)

os.waitpid(pid, 0)