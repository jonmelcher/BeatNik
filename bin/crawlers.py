"""
This file contains the crawlers for the BeatNik project, as well as the
Song class.

Newest Changes:
    -Changed style to be more pythonic.
    -Copied BPMBD class over from parser.py, removed Class module depen-
     dencies. -J 9/11/14
    -Created file - J 9/9/14
"""

class Song(object):
    'Song Class is for formatting and maintaining song data.'

    def __init__(self, song_data):

        self.data     = song_data
        self.artist   = None
        self.title    = None
        self.album    = None
        self.BPM      = None
        self.genre    = None
        self.label    = None
        self.year     = None
        self.playlist = []


    def refresh(self):
        'Method for assigning and renewing data. Allows data editing to'
        'be done solely with self.data.'
        self.artist = self.data[0]
        self.title  = self.data[1]
        self.album  = self.data[2]
        self.BPM    = self.data[3]
        self.genre  = self.data[4]
        self.label  = self.data[5]
        self.year   = self.data[6]


    def change_to(self, index, new_value):
        'Method for changing song data.'
        try:
            self.data[index] = new_value
        except Exception as e:
            raise IndexError('Index must be values 0-6.')
        return self.refresh()


    def __repr__(self):
        return repr(self.data)



class BPMDB(object):

    'BPMDB class contains the methods for accessing'
    'http://www.BPMdatabase.com.'

    @staticmethod
    def url_helper(begin, gate, ending):

        'Helper function for band_grab and letter_grab'
        'Type: Int -> Bool -> String -> String'

        """
        Updates url for next parse in band_grab and letter_grab.
        """

        rooturl = "http://www.bpmdatabase.com/browse.php?begin="
        query   = "&artist=" if gate else "&letter="
        url     = rooturl
        url    += ("%s%s%s" % (begin, query, ending))

        return url

    @staticmethod
    def raw_table_grab(url):
        'Helper function for Alpha/song_parse'
        'Type: String -> String'

        """
        Accesses search results page from http://www.BPMdatabase.com
        And scrapes out raw table data from HTML source.
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
    def artist_parse(url):
        'Parses all bandnames from alphabet browsing results pages'
        'Type: String -> [String]'

        text = BPMDB.raw_table_grab(url)

        if not text:
            return None

        data = re.findall('artist=(.+?)"', text)

        return data

    @staticmethod
    def song_parse(url):
        'Parses all song data from a result page.'
        'Type: String -> [[String]]'
        'Each entry corresponds to Song initialization data.'
        'Refer to Song class for more information.'

        text = BPMDB.raw_table_grab(url)

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
    def band_grab(bandname):
        'Grabs and parses all songs by the band in question'
        'Type: String -> [Song]'

        bandname     = bandname.rstrip().replace(' ','+')
        songs        = []
        begin        = 0
        url          = BPMDB.url_helper(begin, True, bandname)
        scraped_data = BPMDB.song_parse(url)

        while scraped_data:
            songs       += [Song(x) for x in scraped_data]
            begin       += 10
            url          = BPMDB.url_helper(begin, True, bandname)
            scraped_data = BPMDB.song_parse(url)

        with open("band_grablog.txt", "a") as logfile:

            logfile.write(time.strftime(
                "\n\nNew log created at %H:%M:%S on %d/%m/%Y\n\n"))
            logfile.write(
                "Search http://www.BPMdatabase.com for %s\n" % bandname)

            for song in songs:
                logfile.write('\n' + ', '.join(song.data))

        return songs

    @staticmethod
    def band_multi_grab(bandlist):
        'List version of band_grab'
        'Type: [String] -> [Song]'

        songs = None
        for band in bandlist:
            if not songs:
                songs  = BPMDB.band_grab(band)
            else:
                songs += BPMDB.band_grab(band)

        return songs

    @staticmethod
    def letter_grab(value):
        'Grabs and parses all artists starting with \'value\'.'
        'Type: String -> [String]'

        artists      = []
        begin        = 0
        url          = BPMDB.url_helper(begin, False, value)

        scraped_data = BPMDB.artist_parse(url)

        while scraped_data:
            artists     += scraped_data
            begin       += 25
            url          = BPMDB.url_helper(begin, False, value)
            scraped_data = BPMDB.artist_parse(url)

        return artists

    @staticmethod
    def crawl():
        'Uses above methods to crawl http://www.BPMdatabase.com.'
        'Type: Void -> [Song]'

        """
        Note that band_grablog.txt will list all song information.
        Warning: this will crawl the entire website and may take
        time and resources.
        """
        alphanumeric = '3'   #This is where 0-9A-Z goes
        artists      = None
        songs        = None

        for letter in alphanumeric:
            print letter
            if not artists:
                artists = BPMDB.letter_grab(letter)
            else:
                artists += BPMDB.letter_grab(letter)

        print artists
        print 'Finding songs...'
        return BPMDB.band_multi_grab(artists)



class AudioKC(object):
    'AudioKC class holds the methods for accessing'
    'http://www.audiokeychain.com'

    @staticmethod
    def raw_table_grab(url):
        """
        Accesses search results page from http://www.audiokeychain.com
        And scrapes out pertinent raw table data from HTML source.
        """
        page = urllib2.urlopen(url)
        text = []

        # Finds the line containing the table of search results.
        for line in page:
            if re.findall('<span class="title">', line):
                text += re.findall('<tr class="line2".*tr>', line)[0]
                break

        return text
