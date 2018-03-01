from __future__ import print_function
import re, requests, os
import urllib
import json

url_loc_search = 'https://www.gumtree.com.au/j-suggest-location.json?query='


def get_loc_search_results(term):
    locations = []
    encoded_term = urllib.parse.quote(term)
    req = requests.get(url_loc_search + encoded_term).json()
    print(type(req))
    if '1'=='1':
        locations = req
        # open file and update dict
        with open('locationdata.json', 'r+') as f:
            try: #try read file
                d = json.loads(f.read())
                print('Current File contents')
                print(d)
                d.update(locations)
                f.seek(0)
                json.dump(d, f)
            except: #nothing in the file
                json.dump(locations,f)

        return locations
    else:
        return None

def set_loc(gtlocid):
    with open('locationdata.json', 'r+') as json_data:
        d = json.loads(json_data.read())
        json_data.close()
        if gtlocid in d.keys():
            bot.db.set_nick_value(trigger.nick, 'gtlocid', term)
            gtcity = d.get("gtlocid")
            bot.say('I have now set your Location as %s' % gtcity)
        else:
            bot.say('I cant find location %s' % gtlocid)


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
        if not trigger.group(2):
            bot.reply('No funny buggers.. give me something to search for')
            return NOLIMIT
        location = trigger.group(2)
        set_loc(location)



if __name__ == '__main__':
    import sys
    query = 'Marr'
    results1 = get_loc_search_results(query)
    quer = 'Sed'
    results1 = get_loc_search_results(quer)
    print(results1)
    query1 = '_3006407'
    output = set_loc(query1)
    print(output)




