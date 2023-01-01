import argparse

from .crypto import transform


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command', help='sub-command help')
    subparsers.required = True

    parser_transform = subparsers.add_parser('transform')
    parser_transform.add_argument('src')

    args = parser.parse_args()

    if args.command == 'transform':
        transform(args.src)
