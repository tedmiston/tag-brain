# Tag Brain

[![CircleCI](https://img.shields.io/circleci/project/github/tedmiston/tag-brain.svg)](https://circleci.com/gh/tedmiston/tag-brain) [![codecov](https://codecov.io/gh/tedmiston/tag-brain/branch/master/graph/badge.svg)](https://codecov.io/gh/tedmiston/tag-brain) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/77dfeba1f8ce49dfadf60f2a2133a94e)](https://www.codacy.com/app/tedmiston/tag-brain?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tedmiston/tag-brain&amp;utm_campaign=Badge_Grade) [![Code Climate](https://codeclimate.com/github/tedmiston/tag-brain/badges/gpa.svg)](https://codeclimate.com/github/tedmiston/tag-brain)

Increase the reach of Instagram posts.

## Setup

```bash
$ pip install -r requirements-dev.txt
```

## Quickstart

Create a file `tags.txt` like this:

```plain
#sometag #anothertag #moartagz
```

See *Input file format* below for options and unit tests for examples.

```bash
$ python app.py tags.txt

3 tags

.
.
.
.
.
#anothertag #moartagz #sometag
```

You can customize output with various options:

```bash
$ python app.py --no-spaces --no-dots tags.txt

3 tags

#anothertag
#moartagz
#sometag
```

## Input file format

- Including # sign in input tags is optional
- Tags can be separate by one or more spaces, newlines, etc
- Duplicates are stripped out and tags are sorted
- You can include an optional caption by formatting your file like this:

  ```plain
  My caption here

  ---

  #tag1 #tag2 #tag3 ...
  ```

## Help

```bash
$ python app.py -h
```

## Lint

```bash
$ invoke lint
```

## Test

```bash
$ invoke test
```
