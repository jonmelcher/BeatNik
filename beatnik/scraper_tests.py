"""
This file is intended to test the scrapers.py module.
This namely is to do with regex pattern matching and
formatting found data afterwards.

- For the regex pattern matching, we will insert
  valid data in the midst of random strings of random
  length.
"""
import random
import string

import scrapers

#Valid datapoints for either scraper.  In form (raw_input, output).'
example_0 = (
            "</tr><tr class=\"line2\"><td>1</td><td>1</td><td></td><td>1 BPM</td><td></td><td>"  +
            "</td><td></td></tr><tr class=\"line1\"><td>1</td><td>1</td><td></td><td>1 BPM</td>" +
            "<td></td><td></td><td></td></tr><tr class=\"line2\"><td>1</td><td>1</td><td></td>"  +
            "<td>1 BPM</td><td></td><td></td><td></td></tr><tr class=\"line1\"><td>1</td><td>1"  +
            "</td><td>1</td><td>1 BPM</td><td>Acid Techno</td><td>1</td><td>1</td></tr><tr class"+
            "=\"line2\"><td>1</td><td>-1'</td><td>1</td><td>1 BPM</td><td>Acid Techno</td><td>1" +
            "</td><td>1</td></tr><tr class=\"line1\"><td>1</td><td>1</td><td>-1'</td><td>1 BPM"  +
            "</td><td>Acid Techno</td><td>1</td><td>1</td></tr><tr class=\"bar\" align=\"cente"  +
            "r\"><td colspan=\"7\">Page: <a href='?begin=0&num=1&numBegin=1&artist=1'></a><b>1"  +
            "</b><a></a>",
            '<tr class="line2"><td>1</td><td>1</td><td></td><td>1 BPM</td><td></td><td></td><td></td></tr><tr class="line1"><td>1</td><td>1</td><td></td><td>1 BPM</td><td></td><td></td><td></td></tr><tr class="line2"><td>1</td><td>1</td><td></td><td>1 BPM</td><td></td><td></td><td></td></tr><tr class="line1"><td>1</td><td>1</td><td>1</td><td>1 BPM</td><td>Acid Techno</td><td>1</td><td>1</td></tr><tr class="line2"><td>1</td><td>-1\'</td><td>1</td><td>1 BPM</td><td>Acid Techno</td><td>1</td><td>1</td></tr><tr class="line1"><td>1</td><td>1</td><td>-1\'</td><td>1 BPM</td><td>Acid Techno</td><td>1</td><td>1</td></tr>',
            [['1', '1', '', '1 BPM', '', '', '', ''], ['1', '1', '', '1 BPM', '', '', '', ''], ['1', '1', '', '1 BPM', '', '', '', ''], ['1', '1', '1', '1 BPM', 'Acid Techno', '1', '1', ''], ['1', "-1'", '1', '1 BPM', 'Acid Techno', '1', '1', ''], ['1', '1', "-1'", '1 BPM', 'Acid Techno', '1', '1', '']]
            )
BPMDB_raw_positive = [example_0]


def random_char(alphabet = string.printable + ' '):
    return random.choice(alphabet)

def random_small_string():
    return ''.join([random_char() for i in xrange(random.randint(0,25))])

def random_large_string():
    return ''.join([random_char() for i in xrange(random.randint(26,150))])

def test_string(is_large, positive_raw):
    #match_source needs to be [String] type.
    if is_large:
        left, right = random_large_string(), random_large_string()
    else:
        left, right = random_small_string(), random_small_string()
    return left + positive_raw + right

def test_BPMD_raw_table_grab(raw_table_positive, is_large):

    insertion_string = raw_table_positive[0]

    if is_large:
        to_test = test_string(True, insertion_string)
    else:
        to_test = test_string(False, insertion_string)

    if scrapers.BPMDB.raw_table_grab("", to_test) == raw_table_positive[1]:
        return True
    else:
        return False

def test_BPMD_song_parse(song_parse_positive, is_large):

    insertion_string = song_parse_positive[0]

    if is_large:
        to_test = test_string(True, insertion_string)
    else:
        to_test = test_string(False, insertion_string)

    if scrapers.BPMDB.song_parse("", to_test) == song_parse_positive[2]:
        return True
    else:
        return False

