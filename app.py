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


def load_input(filename, caption_divider='---'):
    """Load input file."""
    with open(filename) as fp:
        input_file = fp.read()

    if caption_divider in input_file:
        caption, tags = input_file.split(caption_divider)
        caption = caption.strip()
    else:
        caption = None
        tags = input_file

    tags = tags.strip().split()
    return caption, tags


def de_hash(tags):
    """Remove optional leading pound signs."""
    return [t.replace('#', '') for t in tags]


def de_dupe(tags):
    """Remove duplicate tags."""
    return list(set(tags))


def output(caption, tags, spaces, dots, tag_limit=30):
    """Print a list of hashtags to be pasted into Instagram."""
    MIN_LINES_TO_COLLAPSE = 5  # five lines collapses the comment on mobile
    header = '{} tags'.format(len(tags))
    if len(tags) > tag_limit:
        warning = '*Warning: You have exceeded the max of {} tags*'.format(tag_limit)
        header = ' '.join([header, warning])
    dots = '\n.' * MIN_LINES_TO_COLLAPSE if dots else ''
    separator = ' ' if spaces else '\n'
    tag_list = separator.join(['#' + t for t in tags])
    output_components = [header]
    if caption is not None:
        output_components.append('\n' + caption)
    output_components += [dots, tag_list]
    tag_comment = '\n'.join(output_components)
    print(tag_comment)


def main():
    args = config()
    caption, tags = load_input(filename=args.file)
    tags = de_hash(tags)
    tags = de_dupe(tags)
    tags = sorted(tags)
    output(caption, tags, spaces=args.spaces, dots=args.dots)


if __name__ == '__main__':
    main()
