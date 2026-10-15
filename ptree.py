#!/usr/bin/env python3
"""Дерево процессов текущего пользователя по данным /proc (без ps)."""
import os


def read_proc(pid):
    try:
        with open(f"/proc/{pid}/stat") as f:
            data = f.read()
        uid = os.stat(f"/proc/{pid}").st_uid
        rss_kb = 0
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    rss_kb = int(line.split()[1])
                    break
    except (FileNotFoundError, ProcessLookupError, PermissionError):
        return None  # процесс успел завершиться или недоступен

    left = data.index("(")
    right = data.rindex(")")          # имя может содержать пробелы и скобки
    name = data[left + 1:right]
    rest = data[right + 2:].split()
    return {
        "pid": pid,
        "name": name,
        "state": rest[0],
        "ppid": int(rest[1]),
        "uid": uid,
        "rss": rss_kb,
    }


def main():
    my_uid = os.getuid()
    procs = {}
    for entry in os.listdir("/proc"):
        if entry.isdigit():
            info = read_proc(int(entry))
            if info and info["uid"] == my_uid:
                procs[info["pid"]] = info

    children = {}
    for p in procs.values():
        children.setdefault(p["ppid"], []).append(p["pid"])

    # корни: процессы, чей родитель не принадлежит текущему пользователю
    roots = sorted(pid for pid, p in procs.items() if p["ppid"] not in procs)

    def show(pid, depth):
        p = procs[pid]
        print(f'{"    " * depth}{p["pid"]} {p["name"]}  '
              f'[{p["state"]}]  RSS={p["rss"]} kB')
        for child in sorted(children.get(pid, [])):
            show(child, depth + 1)

    for r in roots:
        show(r, 0)


if __name__ == "__main__":
    main()