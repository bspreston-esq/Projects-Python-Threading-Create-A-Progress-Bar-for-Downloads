#!/usr/bin/env python3
"""Progress bar running on its own thread, fed by a download worker."""
import argparse
import io
import queue
import sys
import threading
import time
import urllib.request

class ProgressBar(threading.Thread):
    """Renders a bar from (done, total) messages received on a queue."""

    def __init__(self, width: int = 40, stream=sys.stdout):
        super().__init__(daemon=True)
        self.width = width
        self.stream = stream
        self.updates = queue.Queue()
        self.finished = threading.Event()
        self.last_line = ""

    def update(self, done: int, total: int) -> None:
        self.updates.put((done, total))

    def finish(self) -> None:
        self.finished.set()
        self.join()

    def render(self, done: int, total: int) -> str:
        fraction = 1.0 if total <= 0 else min(1.0, done / total)
        filled = int(self.width * fraction)
        bar = "#" * filled + "-" * (self.width - filled)
        return f"\r[{bar}] {fraction*100:6.1f}%  {done:,}/{total:,} bytes"

    def run(self):
        while not self.finished.is_set() or not self.updates.empty():
            try:
                done, total = self.updates.get(timeout=0.05)
            except queue.Empty:
                continue
            line = self.render(done, total)
            self.stream.write(line)
            self.stream.flush()
            self.last_line = line
        self.stream.write("\n")
        self.stream.flush()

def download(url: str, bar: ProgressBar, chunk_size: int = 65536):
    """Download `url` into memory, reporting progress to the bar thread."""
    request = urllib.request.Request(url, headers={"User-Agent": "progress-download/1.0"})
    buffer = io.BytesIO()
    with urllib.request.urlopen(request, timeout=30) as response:
        total = int(response.headers.get("Content-Length") or 0)
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            buffer.write(chunk)
            bar.update(buffer.tell(), total)
    return buffer.getvalue()

def demo() -> None:
    total = 950_000
    bar = ProgressBar(width=32)
    bar.start()
    written = 0
    chunk = 95_000
    while written < total:
        written = min(total, written + chunk)
        bar.update(written, total)
        time.sleep(0.01)
    bar.finish()
    print(f"simulated download complete: {written:,} bytes in {math_round(written/1e6)} MB")

def math_round(value):
    return f"{value:.2f}"

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo or not args.url:
        demo()
        return
    bar = ProgressBar()
    bar.start()
    data = download(args.url, bar)
    bar.finish()
    print(f"downloaded {len(data):,} bytes")

if __name__ == "__main__":
    main()
