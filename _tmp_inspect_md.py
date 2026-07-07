from pathlib import Path
import sys


path = Path(sys.argv[1])
cmd = sys.argv[2]
lines = path.read_text(encoding="utf-8").splitlines()

if cmd == "show":
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    for i in range(start, min(end, len(lines)) + 1):
        sys.stdout.buffer.write(f"{i}: {lines[i-1]}\n".encode("utf-8"))
elif cmd == "headings":
    for i, line in enumerate(lines, start=1):
        if line.startswith("## ") or line.startswith("### "):
            sys.stdout.buffer.write(f"{i}: {line}\n".encode("utf-8"))
else:
    raise SystemExit(f"unknown cmd: {cmd}")
