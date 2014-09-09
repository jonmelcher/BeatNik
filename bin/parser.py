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

ls = ["http://www.bpmdatabase.com/","search.php?artist=radiohead",
     "&title=&mix=&bpm=&gid=","&label=&year=&srt=artist&ord=desc"]

example = ''.join(ls)


def BPMdatabaseparse(url):
    'Parses all song data on a BPMdatabase.com search page into an array'

    page = urllib2.urlopen(url)
    # page = page.read()

    # print page[:100]
    # a = re.findall(page, '<html>')
    # print a
    # print page
    linedata = []

    for line in page:
        linedata += re.findall('<tr class="line2">', line)


    print linedata
    # linedata = ''.join(linedata)

    # data = re.findall('<td>.*td>', linedata)
    # data = ''.join(data)
    # data = re.sub('</?tr>|</?td>|<tr class="line[12]">',' ', data)
    # data = data.rsplit()

    # bandname = data[0]
    # parsed_data = []
    # new_entry = []
    # i = 0

    # while i < len(data):
    #     if data[i] == bandname:
    #         if new_entry:
    #             parsed_data.append(new_entry)
    #             new_entry = []
    #     new_entry.append(data[i])
    #     i += 1
    # else:
    #     parsed_data.append(new_entry)

    # return parsed_data



if __name__ == '__main__':
    data = BPMdatabaseparse(example)
    # print data[1]
