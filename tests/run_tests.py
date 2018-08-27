#!/usr/bin/env python
import os
import sys
import argparse


sys.path.insert(0, '.')
import noWord as meta


from NWTestCase import NWTestCase


def parserCommandLine(additionalArgs=[]):
    parser = argparse.ArgumentParser(description="noWord test runner")

    parser.add_argument('-v', '--version', action='version',
                        version=meta.__version__)

    parser.add_argument(dest="source", help="Source folder")
    parser.add_argument(dest="output", help="Destination folder")

    for arg in additionalArgs:
        parser.add_argument(**arg)

    return parser.parse_args()


def scanInputRoot(path):
    for item in sorted(os.listdir(path)):
        itemPath = os.path.join(path, item)

        if os.path.isdir(itemPath) and not item.startswith("."):
            inputfile = os.path.join(itemPath, 'input/doc_info.yaml')
            reffile = os.path.join(itemPath, 'ref/ref.pdf')

            # return only valid case folders
            if os.path.exists(inputfile) and \
                    os.path.exists(reffile):
                yield itemPath


def main():
    args = parserCommandLine()

    inputroot = os.path.abspath(args.source)
    outputfolder = os.path.abspath(args.output)

    for casefolder in scanInputRoot(inputroot):
        inputname = os.path.basename(casefolder)
        case1 = NWTestCase(casefolder,
                           os.path.join(outputfolder, inputname))

        case1.run()


if __name__ == '__main__':
    main()
