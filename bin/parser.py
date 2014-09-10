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



def BPMdatabaseparse(url):
    'Parses all song data on a BPMdatabase.com search page into an array'

    page = urllib2.urlopen(url)

    # find the line containing the table of search results
    for line in page:
        text = re.findall('<tr class="line2".*tr>', line)[0]
        if re.findall('<tr class="line2".*tr>', line):
            break

    # split up the search table by row
    temp_data = re.split('<tr class', text)
    temp_data.remove('')

    # collect the column entries for each row
    data = []
    for d in temp_data:
        new_data = re.findall('<td>([\w ]+?)</td>', d)
        data.append(new_data)


    return data


if __name__ == '__main__':
    ls = ["http://www.bpmdatabase.com/","search.php?artist=radiohead",
        "&title=&mix=&bpm=&gid=","&label=&year=&srt=artist&ord=desc"]

    example = ''.join(ls)
    data = BPMdatabaseparse(example)
    print data
