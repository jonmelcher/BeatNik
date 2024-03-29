"""
This file contains the scrapers for the BeatNik project.
Please see BeatNik/documentation.txt for further information
regarding this file.

Newest Changes:
    -Added documentation.txt descriptions for scraper.py -J 9/12/14
    -Added AudioKC class, needs to be tested more diligently. -J 9/11/14
"""
import urllib2
import re
import time

import music


class BPMDB(object):

    'BPMDB class contains the methods for accessing'
    'http://www.BPMdatabase.com.'

    @staticmethod
    def url_helper(begin, is_artist, ending):
        'Helper function for artist_grab and letter_grab'
        'Type: Int -> Bool -> String -> String'

        """
        Updates url for next parse in artist_grab and letter_grab.
        """
        rooturl       = "http://www.bpmdatabase.com/browse.php?begin="
        artist_option = "&artist=" if is_artist else "&letter="
        new_url       = rooturl + ("%s%s%s" %
                        (begin, artist_option, ending))

        return new_url

    @staticmethod
    def raw_table_grab(url, test = ""):
        'Helper function for artist/song_parse'
        'Type: String -> String'

        """
        Accesses search results page from http://www.BPMdatabase.com
        And scrapes out raw table data from HTML source.
        """
        #Testing the regular expression pattern:
        if test:
            return re.findall('<tr class="line2".*tr>', test)

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
        data = re.findall('artist=(.+?)"', text) if text else None

        return data

    @staticmethod
    def song_parse(url = None, text = None):
        'Parses all song data from text taken from a result page.'
        'Each entry corresponds to Song initialization data.'
        'It will have to be formatted correctly to go to output.'
        'The required format for Song class is:'
        '[artist, title, album, BPM, genre, label, year, key]'
        'Type: String -> [[String]]'

        # Conditional to allow testing.
        if url:
            text = BPMDB.raw_table_grab(url)
        # Conditional for negative result.
        if not text or 'No records found.' in text:
            return None
        # Splits up the search results table by row.
        split_text = re.split('<tr class="line[12]">', text)
        # Collects the column entries from each row.
        # Replaces empty column entries with 'NULL'.
        data = []
        for splt in split_text:
            song_data = re.findall("<td>(.*?)</td>", splt)
            if len(song_data) == 7:
                #song_data is in form
                #[artist, title, album, BPM, genre, label, year].
                #current formatting to match Song format:
                song_data.append("")
                data.append(song_data)

        return data

    @staticmethod
    def artist_grab(artist):
        'Grabs and parses all songs by the artist in question'
        'Relies on url_helper and song_parser to work'
        'In this function the bool in url_helper is set to True'
        'As we are searching for artists.'
        'Type: String -> [Song]'

        artist       = artist.rstrip().replace(' ','+')
        songs        = []
        begin        = 0
        url          = BPMDB.url_helper(begin, True, artist)
        scraped_data = BPMDB.song_parse(url)

        while scraped_data:
            songs       += [music.Song(song) for song in scraped_data]
            begin       += 10
            next_url     = BPMDB.url_helper(begin, True, artist)
            scraped_data = BPMDB.song_parse(next_url)

        return songs

    @staticmethod
    def artist_multi_grab(artists):
        'List version of artist_grab'
        'Type: [String] -> [Song]'

        songs = None
        for artist in artists:
            if not songs:
                songs  = BPMDB.artist_grab(artist)
            else:
                songs += BPMDB.artist_grab(artist)

        return songs

    @staticmethod
    def letter_grab(value):
        'Grabs and parses all artists starting with \'value\'.'
        'In this function the bool in url_helper is set to False'
        'As we are searching for a letter.'
        'Type: String -> [String]'

        artists      = []
        begin        = 0
        url          = BPMDB.url_helper(begin, False, value)

        scraped_data = BPMDB.artist_parse(url)
        while scraped_data:
            artists     += scraped_data
            begin       += 25
            next_url     = BPMDB.url_helper(begin, False, value)
            scraped_data = BPMDB.artist_parse(next_url)

        return artists

    @staticmethod
    def scrape(alphanumeric = '3', write_to_text = False):
        'Uses above methods to scrape http://www.BPMdatabase.com.'
        'Type: Void -> [Song]'

        """
        Note that scrapelog.txt will list all song information.
        Warning: changing alphanumeric value will change breadth
        of scrape.
        """
        artists = None

        for letter in alphanumeric:
            print letter
            if not artists:
                artists  = BPMDB.letter_grab(letter)
            else:
                artists += BPMDB.letter_grab(letter)

        print "Now finding songs by %s" % (artists)
        print "Working..."

        songs = BPMDB.artist_multi_grab(artists)
        # Writing to text log.  This should be written as a function elsewhere.
        if write_to_text:
            with open("scrapelog.txt", "a") as logfile:

                logfile.write(time.strftime(
                    "\n\nNew log created at %H:%M:%S on %d/%m/%Y\n\n"))

                logfile.write(
                    "Searched http://www.BPMdatabase.com for the following:\n")

                for song in songs:
                    logfile.write('\n' + ', '.join(song.data))


    def __repr__(self):
        return 'Scraper Class for http://www.BPMdatabase.com.'



class AudioKC(object):
    'AudioKC class holds the methods for accessing'
    'http://www.audiokeychain.com'

    @staticmethod
    def url_helper(genre, page_number):
        'Helper function for scrape.'
        'Returns updated url based on parameters.'
        rooturl = "http://www.audiokeychain.com/database?genre[]="
        new_url = rooturl + "%s&page=%s" % (genre, page_number)

        return new_url

    @staticmethod
    def raw_table_grab(url):
        'Accesses search results page from http://www.audiokeychain.com'
        'And scrapes out pertinent raw table data from HTML source.'
        'This differs from BPMDBs function by taking blocks of full lines.'
        'Type: String -> [[String]]'
        page = urllib2.urlopen(url)
        text = []
        # Finds the line containing the table of search results.
        for line in page:
            if '<span class="title"' in line:
                text.append([line] + [page.next() for i in range(3)])

        return text[1:]

    @staticmethod
    def page_parse(url = None, text = None):
        'Parses all song data from text taken from a result page.'
        'Each entry corresponds to Song initialization data.'
        'It will have to be formatted correctly to go to output.'
        'The required format for Song class is:'
        '[artist, title, album, BPM, genre, label, year, key]'
        'Type: String -> [Song]'
        # Condition for testing
        # For testing, set text = [[String]] type
        if url:
            text  = AudioKC.raw_table_grab(url)

        songs = []
        for raw_song_data in text:
            concatted_song = ''.join(raw_song_data)
            song_data = re.findall('<span class="[takb][^"]*?">(.*?)<',
                                                        concatted_song)
            #song_data is in the form [title, artist, key, bpm] so must
            #convert to a valid form for Song class.
            formatted_song_data = [song_data[1], song_data[0], 'NULL',
                                   song_data[3], 'Null'      , 'Null',
                                   'Null'      , song_data[2]]
            songs.append(music.Song(formatted_song_data))

        return songs

    @staticmethod
    def scrape(lower, upper, write_to_text = False):
        'Scrapes all song data from http://audiokeychain.com within'
        'specified genres. Type: Int -> Int -> [Song].'

        """
        Select slice of scrape_genres (must be list) to scrape that portion
        of the genres on the website.  Length of scrape_genres = 74.
        """
        scrape_genres = [  # length of scrape_genres is 74
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
        #Handling exceptions
        if lower == upper:
            raise TypeError('lower and upper must provide a list slice as input')
        elif lower > upper:
            lower, upper = upper, lower
        if lower < 0 || upper > 74:
            raise IndexError('List slice must fall directly within 0:74.')

        genres = scrape_genres[lower:upper]
        songs  = []
        for genre in genres:
            print 'Beginning to scrape for the genre %s.' % (genre)
            #Initializes songs with [Song] output from parsing first page.
            previous_size, previous_page, page_number = len(songs), None, 1
            next_page = AudioKC.page_parse(AudioKC.url_helper(genre,
                                                        page_number))
            songs     += next_page

            while next_page  != previous_page:
                songs_size    = len(songs)
                print "Scraped page %s for the genre %s." % (page_number, genre)
                print "Scraped a grand total of %s songs." % (songs_size)
                page_number  += 1
                previous_page = next_page
                next_page     = AudioKC.page_parse(AudioKC.url_helper(genre,
                                                               page_number))
                songs += next_page
        # Writing to text log.  This should be written as a function elsewhere.
        if write_to_text:
            with open("scrapelog.txt", "a") as logfile:

                logfile.write(time.strftime(
                    "\n\nNew log created at %H:%M:%S on %d/%m/%Y\n\n"))

                logfile.write(
                    "Searched http://www.audiokeychain.com for the following:\n")

                for song in songs:
                    logfile.write('\n' + ', '.join(song.data))

        return songs


    def __repr__(self):
        return 'Scraper Class for http://www.audiokeychain.com.'
