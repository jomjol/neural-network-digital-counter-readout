import argparse
import sys
from collectmeterdigits.collect import collect
from collectmeterdigits.labeling import label
from collectmeterdigits import glob


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--collect',
                        help='collect all images. The edgeAI meter server name must be set')
    parser.add_argument('--days', type=int, default=3, help='count of days back to read. (default: 3)')
    parser.add_argument('--labeling', default='', help='labelpath if you want label the images')
    parser.add_argument('--keepdownloads', action='store_true',
                        help='Normally all downloaded data will be deleted. If set it keeps the images.')
    parser.add_argument('--nodownload', action='store_true',
                        help='Do not download pictures. Only remove duplicates and labeling.')
    parser.add_argument('--startlabel', type=float, default=0.0, help='only images >= startlabel. (default: all)')
    parser.add_argument('--savedublicates', action='store_true',
                        help='Save the dublicates in an intermediate subdirectory in raw_images.')
    parser.add_argument('--labelfile', default=None,
                        help='file with list of image urls if you want label specific images.')
    parser.add_argument('--model', default=None, help='model file path if a external model should be used')

    # print help message if no argument is given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.model is not None:
        glob.model_path = args.model

    if args.labeling == '':
        if args.labelfile is not None:
            label(args.labeling, args.startlabel, args.labelfile)
        else:
            collect(args.collect, args.days, keepolddata=args.keepdownloads, download=not args.nodownload,
                    startlabel=args.startlabel)
    else:
        label(args.labeling, args.startlabel)


if __name__ == '__main__':
    main()
