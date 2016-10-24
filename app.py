"""
Gather, de-dupe, sort, count, format a list of hashtags for Instagram.
"""

import argparse


def config():
    """Configure args and options."""
    parser = argparse.ArgumentParser(prog='python app.py')
    parser.description = 'An Instagram hashtag formatter.'
    parser.add_argument('file', help='a file of input hashtags')

    spaces = parser.add_mutually_exclusive_group(required=False)
    spaces.add_argument('--spaces', '-s', dest='spaces', action='store_true',
                        help='separate tags with spaces (default)')
    spaces.add_argument('--no-spaces', '-ns', dest='spaces', action='store_false',
                        help='separate tags with newlines')

    dots = parser.add_mutually_exclusive_group(required=False)
    dots.add_argument('--dots', '-d', dest='dots', action='store_true',
                      help='include prefix dots to collapse comment (default)')
    dots.add_argument('--no-dots', '-nd', dest='dots', action='store_false',
                      help='do not include prefix dots')

    parser.set_defaults(spaces=True, dots=True)

    return parser.parse_args()


def load_tags(filename):
    """Load input file."""
    with open(filename) as fp:
        tags = fp.read()
    return tags


def de_hash(tags):
    """Remove optional leading pound signs."""
    return [t.replace('#', '') for t in tags.split()]


def de_dupe(tags):
    """Remove duplicate tags."""
    return list(set(tags))


def output(tags, spaces, dots):
    """Print a list of hashtags to be pasted into Instagram."""
    MAX_TAGS_LIMIT = 30  # more than this and comment will fail
    MIN_LINES_TO_COLLAPSE = 5  # five lines collapses the comment on mobile
    header = '{} tags'.format(len(tags))
    if len(tags) > MAX_TAGS_LIMIT:
        warning = '*Warning: IG limits each photo to {} tags*'.format(MAX_TAGS_LIMIT)
        header = ' '.join([header, warning])
    dots = '\n.' * MIN_LINES_TO_COLLAPSE if dots else ''
    separator = ' ' if spaces else '\n'
    tag_list = separator.join(['#' + t for t in tags])
    print('\n'.join([header, dots, tag_list]))


def main():
    args = config()
    tags = load_tags(filename=args.file)
    tags = de_hash(tags)
    tags = de_dupe(tags)
    tags = sorted(tags)
    output(tags, spaces=args.spaces, dots=args.dots)


if __name__ == '__main__':
    main()
