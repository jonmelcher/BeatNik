"""
This program will access a search result page from
http://www.bpmdatabase.com and parse all song data
from the page source.

Some examples:
http://www.bpmdatabase.com/search.php?artist=radiohead&title=&mix=&bpm=&gid=&label=&year=&srt=artist&ord=desc

Notes:
Crude but seems to work for this website.  Let me know what you think.
One problem will be multiple word bandnames/albums/songnames as they
get split up by this program into different list entries.
"""

import urllib2
import re


""" This class should be in another file."""
class Song(object):
    'A song.'

    def __init__(self, data):

        self.data   = data
        
    def __repr__(self):
        return repr(self.data)
""""""

def BPMdatabaseParse(url):
    'Parses all song data on a BPMdatabase.com search page into an array'

    page = urllib2.urlopen(url)

    # find the line containing the table of search results
    text = []
    for line in page:
        if re.findall('<tr class="line2".*tr>', line):
            text = re.findall('<tr class="line2".*tr>', line)[0]
            break
    if not text:
        return None

    # split up the search table by row
    temp_data = re.split('<tr class="line[12]">', text)
    temp_data.remove('')

    # collect the column entries for each row
    # filled replaces empty columns with 'NULL'
    data = []
    for d in temp_data:
        filled   = re.sub('<td></td>','<td>NULL</td>', d)
        new_data = re.findall('<td>([\w ]+?)</td>', filled)
        data.append(new_data)

    return data


def BPMdatabaseBandGrab(bandname):
    'Grabs all songs by the band in question.'
    'Stores them in a list of Song instances.'

    songs   = []
    begin   = ['?begin=', 0]
    num     = ['&num='  , 1]
    rooturl = "http://www.bpmdatabase.com/search.php"

    # might be good way to write this, this is quite ugly
    scraped_data = BPMdatabaseParse(rooturl + (''.join(map(str,begin))
          + ''.join(map(str,num)) + "&numBegin=0&artist=" + bandname))

    while scraped_data:

        songs       += [Song(x) for x in scraped_data]
        begin[1]    += 10
        num[1]      += 1
        scraped_data = BPMdatabaseParse(rooturl + (''.join(map(str,begin))
              + ''.join(map(str,num)) + "&numBegin=0&artist=" + bandname))

    return songs


if __name__ == '__main__':

    example = "http://www.bpmdatabase.com/search.php?begin=0&num=1&numBegin=0&artist=tragically+hip"
    data = BPMdatabaseParse(example)
    print data