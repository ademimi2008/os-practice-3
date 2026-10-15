#!/usr/bin/env python3
"""Использование: python3 runner.py N команда [аргументы...]"""
import os
import sys
import time


def main():
    if len(sys.argv) < 3:
        print("Использование: python3 runner.py N команда [аргументы...]")
        sys.exit(1)

    n = int(sys.argv[1])
    cmd = sys.argv[2:]
    started = {}  # pid -> время старта

    for i in range(n):
        pid = os.fork()
        if pid == 0:
            # ребёнок: заменяем процесс командой
            try:
                os.execvp(cmd[0], cmd)
            except OSError as e:
                print(f"[child {i}] exec не удался: {e}", file=sys.stderr)
                os._exit(127)
        else:
            started[pid] = (i, time.monotonic())

    print(f"[parent {os.getpid()}] запущено {n} дочерних процессов, жду...")

    results = []
    while started:
        pid, status = os.wait()          # ждём любого завершившегося
        elapsed = time.monotonic() - started[pid][1]
        idx = started.pop(pid)[0]
        code = os.waitstatus_to_exitcode(status)
        results.append((idx, pid, code, elapsed))

    print(f'\n{"#":<3} {"PID":<8} {"код":<5} {"время, с":<10}')
    for idx, pid, code, elapsed in sorted(results):
        print(f"{idx:<3} {pid:<8} {code:<5} {elapsed:<10.3f}")


if __name__ == "__main__":
    main()