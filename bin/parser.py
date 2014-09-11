"""
This file contains files serving to scrape and parse data
found on online databases.

Current databases:

http://www.BPMdatabase.com
    -BPMdatabaseParse   : url ->  [[Song Data]]
    -BPMdatabaseBandGrab: bandname -> [[Songs]]

Newest Changes:
-Added this, please modify below! -J 9/9/14

-Changed BPMDB methods to static, removed instantiation - J 9/11/14
-Major overhaul, made a class for BPMdatabase methods, will trans-
 fer over to Classes.py. Full crawl should work now, had to edit
 regular expressions in SongParse for weird characters in bandnames
 etc. if there is a more succinct way of writing those expressions
 please change.  -J 9/10/14
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

    @staticmethod
    def urlHelper(begin, gate, ending):

        'Helper function for BandGrab and LetterGrab'
        'Type: Int -> Bool -> String -> String'

        """
        Updates url for next parse in BandGrab and LetterGrab.
        """

        rooturl = "http://www.bpmdatabase.com/browse.php?begin="
        query   = "&artist=" if gate else "&letter="
        url     = rooturl
        url    += ("%s%s%s" % (begin, query, ending))

        return url

    @staticmethod
    def RawTableGrab(url):
        'Helper function for Alpha/SongParse'
        'Type: String -> String'

        """
        Accesses search results page from http://www.BPMdatabase.com
        And parses out raw table data from HTML source.
        """
        page = urllib2.urlopen(url)
        text = []

        # Finds the line containing the table of search results.
        for line in page:
            if re.findall('<tr class="line2".*tr>', line):
                text = re.findall('<tr class="line2".*tr>', line)[0]
                break

        return text

    @staticmethod
    def ArtistParse(url):
        'Parses all bandnames from alphabet browsing results pages'
        'Type: String -> [String]'

        text = BPMDB.RawTableGrab(url)

        if not text:
            return None

        data = re.findall('artist=(.+?)"', text)

        return data

    @staticmethod
    def SongParse(url):
        'Parses all song data from a result page.'
        'Type: String -> [[String]]'
        'Each entry corresponds to Song initialization data.'
        'Refer to Song class for more information.'

        text = BPMDB.RawTableGrab(url)

        if not text or 'No records found.' in text:
            return None

        # Splits up the search results table by row.
        temp_data = re.split('<tr class="line[12]">', text)
        if '' in temp_data:
            temp_data.remove('')

        # Collects the column entries from each row.
        # Replaces empty column entries with 'NULL'.
        data = []
        for d in temp_data:
            filled   = re.sub("<td></td>", "<td>NULL</td>", d)
            new_data = re.findall("<td>(.*?)</td>", filled)

            if len(new_data) == 7:
                data.append(new_data)

        return data

    @staticmethod
    def BandGrab(bandname):
        'Grabs and parses all songs by the band in question'
        'Type: String -> [Song]'

        bandname     = bandname.rstrip().replace(' ','+')
        songs        = []
        begin        = 0
        url          = BPMDB.urlHelper(begin, True, bandname)
        scraped_data = BPMDB.SongParse(url)

        while scraped_data:
            songs       += [Classes.Song(x) for x in scraped_data]
            begin       += 10
            url          = BPMDB.urlHelper(begin, True, bandname)
            scraped_data = BPMDB.SongParse(url)

        with open("bandgrablog.txt", "a") as logfile:

            logfile.write(time.strftime(
                "\n\nNew log created at %H:%M:%S on %d/%m/%Y\n\n"))
            logfile.write(
                "Search http://www.BPMdatabase.com for %s\n" % bandname)

            for song in songs:
                logfile.write('\n' + ', '.join(song.data))

        return songs

    @staticmethod
    def BandMultiGrab(bandlist):
        'List version of BandGrab'
        'Type: [String] -> [Song]'

        songs = None
        for band in bandlist:
            if not songs:
                songs  = BPMDB.BandGrab(band)
            else:
                songs += BPMDB.BandGrab(band)

        return songs

    @staticmethod
    def LetterGrab(value):
        'Grabs and parses all artists starting with \'value\'.'
        'Type: String -> [String]'

        artists      = []
        begin        = 0
        url          = BPMDB.urlHelper(begin, False, value)

        scraped_data = BPMDB.ArtistParse(url)

        while scraped_data:
            artists     += scraped_data
            begin       += 25
            url          = BPMDB.urlHelper(begin, False, value)
            scraped_data = BPMDB.ArtistParse(url)

        return artists

    @staticmethod
    def Crawl():
        'Uses above methods to crawl http://www.BPMdatabase.com.'
        'Type: Void -> [Song]'

        """
        Note that bandgrablog.txt will list all song information.
        Warning: this will crawl the entire website and may take 
        time and resources.
        """
        alphanumeric = '3'   #This is where 0-9A-Z goes
        artists      = None
        songs        = None

        for letter in alphanumeric:
            print letter
            if not artists:
                artists = BPMDB.LetterGrab(letter)
            else: 
                artists += BPMDB.LetterGrab(letter)

        print artists
        print 'Finding songs...'
        return BPMDB.BandMultiGrab(artists)



if __name__ == '__main__':

    example_url = 'http://www.bpmdatabase.com/search.php?artist=radiohead&title=&mix=&bpm=&gid=&label=&year=&srt=artist&ord=asc'

    results = BPMDB.SongParse(example_url)
    crawl   = BPMDB.Crawl()
    print results[0]
    print crawl