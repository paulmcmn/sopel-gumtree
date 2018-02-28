from __future__ import print_function
import re, requests, os
import urllib
import json

url_loc_search = 'https://www.gumtree.com.au/j-suggest-location.json?query='


def get_loc_search_results(term):
    locations = []
    encoded_term = urllib.parse.quote(term)
    req = requests.get(url_loc_search + encoded_term)
    if req.ok:

        # open file and update dict
        with open('locationdata.json', 'a+') as f:
            try: #try read file
                d = json.loads(f.read())
                d.update(locations)
                f.seek(0)
                json.dump(d, f)
            except: #nothing in the file
                json.dump(locations,f)
        return locations
    else:
        return None


try:
    import sopel.module
except ImportError:
    pass
else:
    ## Manage Location Functions
    @sopel.module.commands('gt-searchlocation')
    @sopel.module.example('.gt-searchlocation Marrickville')
    def f_locationsearch(bot, trigger):
        """Search gumtree for something"""
        searchterm = trigger.group(2)

        results = get_loc_search_results(searchterm)
        if results and len(results):
            bot.say(locations, trigger.sender, len(definitions) * 2)
        else:
            bot.say('Can\'t find any locations for "{}".'.format(phrase), trigger.sender)
        return sopel.module.NOLIMIT


    @sopel.module.commands('gt-setlocation')
    @sopel.module.example('.gt-setlocation 3003906')
    def f_locationset(bot, trigger):
        """Sets a location for a user"""
        location = trigger.group(2)
        with open('locationdata.json', 'a+') as f:
            try:  # try read file
                d = json.loads(f.read())
                d.update(locations)
                f.seek(0)
                json.dump(d, f)
                if 'location' in d.keys:
                    bot.say(d["location"])
                else:
                    bot.say('Mate that location doesnt exist')
            except:  # nothing in the file
                bot.say('Mate that location doesnt exist')

        return sopel.module.NOLIMIT






if __name__ == '__main__':
    import sys


