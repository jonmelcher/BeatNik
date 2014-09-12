"""
This file contains the crawlers for the BeatNik project, as well as the
Song class.

Newest Changes:
    -Added AudioKC class, needs to be tested more diligently. -J 9/11/14
    -Changed style to be more pythonic.
    -Copied BPMBD class over from parser.py, removed Class module depen-
     dencies. -J 9/11/14
    -Created file - J 9/9/14
"""
import urllib2
import re
import time


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
        self.key      = None


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
        self.key    = self.data[7]


    def change_to(self, index, new_value):
        'Method for changing song data.'
        try:
            self.data[index] = new_value
        except Exception as e:
            raise IndexError('Index must be values 0-6.')
        return self.refresh()


    def __eq__(self, other):
        'Method for determining equality of songs.'
        'Type: Song -> Song -> Bool'
        if self.data[:2] == other.data[:2]:
            return True
        return False


    def __ne__(self, other):
        return not self.__eq__(other)


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
        text = ""

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

        with open("scrapelog.txt", "a") as logfile:

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
        Note that scrapelog.txt will list all song information.
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
    def url_helper(genre, page_number):
        'Helper function for crawl'
        rooturl = "http://www.audiokeychain.com/database?genre[]="
        url     = rooturl + "%s&page=%s" % (genre, page_number)
        return url


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
            if '<span class="title"' in line:
                text.append([line] + [page.next() for i in range(3)])
        return text[1:]

    @staticmethod
    def page_parse(url):
        'Parses raw_table_grab(url) and returns list of Song objects'
        'Type: String -> [Song]'
        text  = AudioKC.raw_table_grab(url)
        songs = []
        for raw_song_data in text:
            concatenated_song = ''.join(raw_song_data)
            song_data = re.findall('<span class="[takb][^"]*?">(.*?)<',
                                                     concatenated_song)
            #song_data is in the form [title, artist, key, bpm] so must
            #convert to a valid form for Song class.
            formatted_song_data = [song_data[1], song_data[0], 'NULL',
                                   song_data[3], 'Null'      , 'Null',
                                   'Null'      , song_data[2]]
            songs.append(Song(formatted_song_data))

        return songs

    @staticmethod
    def crawl(lower, upper):
        'Scrapes all song data from http://audiokeychain.com within'
        'specified genres. Type: Int -> Int -> [Song].'

        """
        Select slice of crawl_genres (must be list) to crawl that portion
        of the genres on the website.
        """
        crawl_genres = [
        'pop'   , 'rock'   , 'hip+hop'   , 'house'        , 'r%26b'     ,
        'dance' , 'rap'    , 'country'   , 'electronic'   , 'blues'     ,
        'trance', 'dubstep', 'other'     , 'soul'         , 'gospel'    ,
        'punk'  , 'reggae' , 'folk'      , 'techno'       , 'remix'     ,
        'club'  , 'funk'   , 'soundtrack','electronica'   , 'jazz'      ,
        'grime' , 'emo'    , 'electro'   , 'drum+and+bass', 'indie+rock',
        'latin' , 'bachata','dancehall'  ,'electro+house' , 'dancehall' ,
        'edm'   , 'trap'   , 'indie'     , 'christian+rap', 'reggaeton' ,
        'singer-songwriter', 'christian' , 'disco'        , 'new+age'   ,
        'progressive+house', 'eurodance' , 'alternative'  , 'classical' ,
        'rap/hip-hop'      , 'synthpop'  , 'indie+pop'    , 'boy+band'  ,
        'worship+music'    , 'comedy'    , 'post-hardcore', 'crunk'     ,
        'alternative+rock' ,  'metal'    , 'hip+hop/rap'  , 'hardstyle' ,
        'swedish+house'    , 'industrial', 'heavy+metal'  , 'kulemina'  ,
        'electropop'       , 'big+beat'  , 'electropop'   , 'ambient'   ,
        'soca', 'kpop'     , 'anime'     , 'lmp'          , 'minimal'   ,
        'pony'
                    ]

        genres = crawl_genres[lower:upper]
        songs  = []
        for genre in genres:
            print 'Beginning to scrape genre %s.' % (genre)
            #Initializes songs with [Song] result from parsing first page.
            previous_size = len(songs)
            previous_page = None
            page_number   = 1
            next_page     = AudioKC.page_parse(AudioKC.url_helper(genre,
                                                           page_number))
            songs        += next_page

            while next_page  != previous_page:
                print "Scraped page %s for %s genre." % (page_number, genre)
                songs_size    = len(songs)
                print "Scraped a total of %s songs." % (songs_size)
                page_number  += 1
                previous_page = next_page
                next_page     = AudioKC.page_parse(AudioKC.url_helper(genre,
                                                               page_number))
                songs += next_page

        with open("scrapelog.txt", "a") as logfile:

            logfile.write(time.strftime(
                "\n\nNew log created at %H:%M:%S on %d/%m/%Y\n\n"))
            logfile.write(
                "Searched http://www.audiokeychain.com for the following:\n")

            for song in songs:
                logfile.write('\n' + ', '.join(song.data))

        return songs
