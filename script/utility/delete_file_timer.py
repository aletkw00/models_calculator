import time
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate models')
    parser.add_argument('-file',
                        help='path to the file', required=True)
    parser.add_argument('-time',
                        help='time', type=int, default=15)

    args = parser.parse_args()

    time.sleep(args.time)

    os.remove(args.file)