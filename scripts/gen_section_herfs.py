#!/usr/bin/python3
# coding: utf-8
# rfc4918-cn (c) by weooh
#
# rfc4918-cn is licensed under a
# Creative Commons Attribution-ShareAlike 4.0 International License.
#
# You should have received a copy of the license along with this
# work. If not, see <http://creativecommons.org/licenses/by-sa/4.0/>.

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True)
    return parser


def get_result(path):
    import os
    result = []
    for p in os.listdir(path):
        if p == 'README.md':
            result.append((0, 'README.md'))
            continue
        idx, *_ = p.split('-', maxsplit=1)
        if not idx.isdigit():
            continue
        result.append((int(idx), p))
    result.sort(key=lambda e: e[0])
    return os.linesep.join(f"[SECTION#{e[0]}]: {e[1]}" for e in result)


def main():
    parser = parse_args()
    args = parser.parse_args()
    result = get_result(args.path)
    print(result)


if __name__ == '__main__':
    main()