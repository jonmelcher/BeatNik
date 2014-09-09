"""
This file is for working on the regular expressions needed
to parse the data scraped online.
"""

"""
http://www.bpmdatabase.com

After searching (eg. Radiohead), the results page's source
shows us that <tr class="line2"></tr> and <tr class="line1"></tr>
mark the boundaries of the pertinent data. Between, <td></td> 
mark boundaries for each data entry. They may be empty.

Is there a way to grab each <tr class=...></tr> using regex?
If possible you can go further and grab each <td></td> inside,
order them by appearance in source and have your data that way.
"""

# <tr class=(\.+)></tr> will grab all the dots that you wanted to grab.
# if ... may be empty, then <tr class=(\.*)></tr> will work
