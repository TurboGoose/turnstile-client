import argparse

from benchmark import benchmark
from live import live_recognition

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", dest="mode", default="benchmark")
    args = parser.parse_args()

    mode = args.mode
    if mode == "benchmark":
        benchmark.run()
    elif mode == "live":
        live_recognition.run()
