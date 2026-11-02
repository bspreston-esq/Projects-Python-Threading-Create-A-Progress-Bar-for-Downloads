# Create A Progress Bar for Downloads

**Category:** Threading

## Problem

Create a progress bar for applications that can keep track of a download in progress. The progress bar will be on a separate thread and will communicate with the main thread using delegates.

## Solution

A `ProgressBar` thread owns rendering and consumes `(done, total)` messages from a `queue.Queue`, while the downloader (main or worker thread) only posts updates. That queue is Python's equivalent of the delegate callback the problem describes, and it keeps I/O and terminal output decoupled.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py --url https://example.com/file.bin
python3 main.py --demo
```

## Example

```text
[################################]  100.0%  950,000/950,000 bytes
simulated download complete: 950,000 bytes in 0.95 MB
```

## Attribution

The problem statement is from [karan/Projects](https://github.com/karan/Projects), a list of practical projects that anyone can solve in any programming language (MIT License, Copyright (c) 2013 Karan Goel). The Python solution in this repository was implemented by [bspreston-esq](https://github.com/bspreston-esq).

This repository is part of the [Projects-Python-All](https://github.com/bspreston-esq/Projects-Python-All) collection.
