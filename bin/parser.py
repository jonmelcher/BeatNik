"""
This file contains files serving to scrape and parse data
found on online databases.

Current databases:

http://www.BPMdatabase.com
    -BPMdatabaseParse   : url ->  [[Song Data]]
    -BPMdatabaseBandGrab: bandname -> [[Songs]]

Newest Changes:
-Added this, please modify below! -J 9/9/14

-Major overhaul, made a class for BPMdatabase methods, will trans-
 fer over to Classes.py.  -J 9/10/14
-Removed Song class and started using Classes.py. -J 9/9/14
-Fixed bug where BandGrab would continue onto next bandname due to
 manual database access(?).  Replacing spaces with '+' in bandname
 seems to have worked. -J 9/9/14
"""

import urllib2
import re
import time

import Classes


class BPMDB(object):

    'Class BPMDB holds the methods for accessing'
    'http://www.BPMdatabase.com.'

    def __init__(self):
        #Can't think of anything necessary here.
        return


    def ParseHelper(self, url):
        'Helper function for Alpha/SongParse'
        'Type: String -> String'

        page = urllib2.urlopen(url)
        text = []
    
        # Finds the line containing the table of search results.
        for line in page:   
            if re.findall('<tr class="line2".*tr>', line):
                text = re.findall('<tr class="line2".*tr>', line)[0]
                break

        return text


    def ArtistParse(self, url):
        'Parses all bandnames from alphabet browsing results pages'
        'Type: String -> [String]'

        text = self.ParseHelper(url)

        if not text:
            return None

        data = re.findall('artist=(.+?)"', text)
        for i, artist in enumerate(data):
            while '%' in artist:
                pct = artist.index('%')
                new = data[i][pct+1:pct+3].decode("hex")
                print new
                data[i] = data[i][:pct] + new + data[i][pct+3:]
                print data[i]

        return data


    def SongParse(self, url):
        'Parses all song data from a result page.'
        'Type: String -> [[String]]'
        'Each entry corresponds to Song initialization data.'
        'Refer to Song class for more information.'

        text = self.ParseHelper(url)
                
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
            
            if len(new_data) == 7:
                data.append(new_data)

        return data


    def BandGrab(self, bandname):
        'Grabs and parses all songs by the band in question'
        'Type: String -> [Song]'

        bandname = bandname.rstrip().replace(' ','+')
        songs    = []
        begin    = ['?begin=', 0]
        num      = ['&num='  , 1]
        rooturl  = "http://www.bpmdatabase.com/search.php"

        # If you can find a better way to represent the variable URL use it.
        scraped_data = self.SongParse(rooturl + (''.join(map(str,begin))
              + ''.join(map(str,num)) + "&numBegin=0&artist=" + bandname))

        while scraped_data:
            songs       += [Classes.Song(x) for x in scraped_data]
            begin[1]    += 10
            num[1]      += 1
            scraped_data = self.SongParse(rooturl + (''.join(map(str,begin))
                  + ''.join(map(str,num)) + "&numBegin=0&artist=" + bandname))

        with open("bandgrablog.txt", "a") as logfile:
            logfile.write(time.strftime(
                "\n\nNew log created at %H:%M:%S on %d/%m/%Y\n\n"))
            logfile.write("Search http://www.BPMdatabase.com for %s\n" % bandname)
            for song in songs:
                logfile.write('\n' + ', '.join(song.data))

        return songs


    def MultiGrab(self, bandlist):
        'List version of BPMdatabaseBandGrab'
        'Type: [String] -> [Song]'

        songs = None
        for band in bandlist:
            if not songs:
                songs = self.BandGrab(band)
            songs += self.BandGrab(band)

        return songs


    def Crawl(self):
        return


if __name__ == '__main__':

    X = BPMDB()
    example1 = "http://www.bpmdatabase.com/search.php?begin=0&num=1&numBegin=0&artist=tragically+hip"
    example2 = "http://www.bpmdatabase.com/search.php?begin=0&num=1&numBegin=0&artist=tragically Hip"
    example3 = "http://www.bpmdatabase.com/search.php?begin=0&num=1&numBegin=0&artist=Radiohead"
    example4 = "Radiohead"
    example5 = "radiOhead"
    example6 = "Avril Lavigne"
    example7 = "Sum+41"
    example8 = [example1, example2, example3]

    print "Example Results for BPMdatabaseParse:"
    print "url for 'tragically+hip', 'tragically Hip', and 'Radiohead'."
    print X.SongParse(example1)
    print X.SongParse(example2)
    print X.SongParse(example3)
    print "Example Results for BPMdatabaseBandGrab:"
    print "Search terms 'Radiohead', 'radiOhead', 'Avril Lavigne', and 'Sum+41'."
    print X.BandGrab(example4)
    print X.BandGrab(example5)
    print X.BandGrab(example6)
    print "Example Results for BPMdatabaseMultiGrab:"
    print X.MultiGrab(example8)