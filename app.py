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
    """Load an input file of zero or more tags with optional caption."""
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


def build_header(tags):
    """Construct a header line with tag count and warn if too many."""
    MAX_TAGS = 30  # max hashtags allowed per post
    header = '{} tags'.format(len(tags))
    warning_tmpl = '*Warning: You have exceeded the max of {} tags*'
    warning = warning_tmpl.format(MAX_TAGS) if len(tags) > MAX_TAGS else ''
    return ' '.join([header, warning]).strip()


def get_collapser(show):
    """Preceding a comment with five dots collapses it on mobile."""
    return '\n.' * 5 if show else ''


def create_tag_str(tags, spaces):
    """Convert a list of tags into a joined string."""
    separator = ' ' if spaces else '\n'
    tag_list = ['#' + t for t in tags]
    return separator.join(tag_list)


def output(caption, tags, spaces, dots):
    """Print the caption and hashtags to be pasted into Instagram."""
    header = build_header(tags)
    pre_caption = '' if caption is not None else None
    dots = get_collapser(show=dots)
    tag_str = create_tag_str(tags=tags, spaces=spaces)
    components = [header, pre_caption, caption, dots, tag_str]
    print('\n'.join([i for i in components if i is not None]))


def main():
    args = config()
    caption, tags = load_input(filename=args.file)
    tags = de_hash(tags)
    tags = de_dupe(tags)
    tags = sorted(tags)
    output(caption, tags, spaces=args.spaces, dots=args.dots)


if __name__ == '__main__':
    main()
