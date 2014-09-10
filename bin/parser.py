"""
This file contains files serving to scrape and parse data
found on online databases.

Current databases:

http://www.BPMdatabase.com
    -BPMdatabaseParse   : url ->  [[Song Data]]
    -BPMdatabaseBandGrab: bandname -> [[Songs]]

Newest Changes:
-Added this, please modify below! -J 9/9/14

-Fixed bug where BandGrab would continue onto next bandname due to
 manual database access(?).  Replacing spaces with '+' in bandname
 seems to have worked. -J 9/9/14
"""

import urllib2
import re

import Classes



def BPMdatabaseParse(url):
    'Parses all song data from a page on http://www.BPMdatabase.com.'
    'Type: String -> [[String]]'
    'Each entry corresponds to Song initialization data.'

    page = urllib2.urlopen(url)
    text = []
    
    # Finds the line containing the table of search results.
    for line in page:   
        if re.findall('<tr class="line2".*tr>', line):
            text = re.findall('<tr class="line2".*tr>', line)[0]
            break
            
    if not text or 'No records found.' in text:
        return None

    # Splits up the search results table by row.
    temp_data = re.split('<tr class="line[12]">', text)
    temp_data.remove('')

    # Collects the column entries from each row.
    # Replaces empty column entries with 'NULL'.
    data = []
    for d in temp_data:
        filled   = re.sub('<td></td>','<td>NULL</td>', d)
        new_data = re.findall('<td>([\w ]+?)</td>', filled)
        data.append(new_data)

    return data


def BPMdatabaseBandGrab(bandname):
    'Grabs and parses all songs by the band in question'
    'from http://www.BPMdatabase.com.'
    'Type: String -> [Song]'
    'Each Song is initialized from data returned from'
    'BPMdatabaseParse.'

    bandname = bandname.rstrip().replace(' ','+')
    songs    = []
    begin    = ['?begin=', 0]
    num      = ['&num='  , 1]
    rooturl  = "http://www.bpmdatabase.com/search.php"

    # If you can find a better way to represent the variable URL use it.
    scraped_data = BPMdatabaseParse(rooturl + (''.join(map(str,begin))
          + ''.join(map(str,num)) + "&numBegin=0&artist=" + bandname))

    while scraped_data:
        songs       += [Classes.Song(x) for x in scraped_data]
        begin[1]    += 10
        num[1]      += 1
        scraped_data = BPMdatabaseParse(rooturl + (''.join(map(str,begin))
              + ''.join(map(str,num)) + "&numBegin=0&artist=" + bandname))

    return songs


if __name__ == '__main__':

    example1 = "http://www.bpmdatabase.com/search.php?begin=0&num=1&numBegin=0&artist=tragically+hip"
    example2 = "http://www.bpmdatabase.com/search.php?begin=0&num=1&numBegin=0&artist=tragically Hip"
    example3 = "http://www.bpmdatabase.com/search.php?begin=0&num=1&numBegin=0&artist=Radiohead"
    example4 = "Radiohead"
    example5 = "radiOhead"
    example6 = "Avril Lavigne"
    example7 = "Sum+41"

    print "Example Results for BPMdatabaseParse:"
    print "url for 'tragically+hip', 'tragically Hip', and 'Radiohead'."
    print BPMdatabaseParse(example1)
    print BPMdatabaseParse(example2)
    print BPMdatabaseParse(example3)
    print "Example Results for BPMdatabaseBandGrab:"
    print "Search terms 'Radiohead', 'radiOhead', 'Avril Lavigne', and 'Sum+41'."
    print BPMdatabaseBandGrab(example1)
    print BPMdatabaseBandGrab(example2)
    print BPMdatabaseBandGrab(example3)
