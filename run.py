from overlay import Overlay
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=str)
    parser.add_argument("--overlay", type=str)
    args = parser.parse_args()
    try:
        app = Overlay.color_key_overlay(args.base, args.overlay)
    finally:
        sys.exit(app)