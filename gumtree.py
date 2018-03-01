from __future__ import print_function
import re, requests, os
import urllib
import json

url_loc_search = 'https://www.gumtree.com.au/j-suggest-location.json?query='
gtauradius = [0, 2, 5, 10, 20, 50, 100, 250, 500]



def get_loc_search_results(term):
    locations = []
    encoded_term = urllib.parse.quote(term)
    req = requests.get(url_loc_search + encoded_term).json()
    print(type(req))
    if '1'=='1':
        locations = req
        print(locations)
        # open file and update dict
        with open('locationdata.json', 'r+') as f:
            try:
                # read file
                d = json.loads(f.read())
                print("Current File contents")
                print(d)
                d.update(locations)
                f.seek(0)
                json.dump(d, f)
            except:
                json.dump(locations, f)
        return locations
    else:
        return None

def set_loc(gtlocid):
    with open('locationdata.json', 'r+') as json_data:
        d = json.loads(json_data.read())
        json_data.close()
        print("d is coming")
        print(d)
        print(gtlocid)
        if str(gtlocid) in d.keys():
            print("wa found")
            return gtlocid
        else:
            return None

def get_city(gtlocid):
    with open('locationdata.json', 'r+') as json_data:
        d = json.loads(json_data.read())
        json_data.close()
        if str(gtlocid) in d.keys():
            gtcity = d.get(gtlocid)
            return gtcity
        else:
            return None

def set_rad(gtradius):
    return min(gtauradius, key=lambda x: abs(x - gtradius))


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
            bot.say(json.dumps(results), trigger.sender, len(json.dumps(results) * 2))
        else:
            bot.say('Can\'t find any locations for "{}".'.format(searchterm), trigger.sender)
        return sopel.module.NOLIMIT

    @sopel.module.commands('gt-setlocation')
    @sopel.module.example('.gt-setlocation 3003906')
    def f_locationset(bot, trigger):
        """Sets a location for a user"""
        if not trigger.group(2):
            bot.reply('No funny buggers.. give me something to search for')
            return NOLIMIT
        location = trigger.group(2)
        results = set_loc(location)
        if results and len(results):
            bot.db.set_nick_value(trigger.nick, 'gtlocid', results)

            bot.say('I have now set your Location as %s' % str(get_city(results)))
        else:
            bot.say('I cant find location %s' % location)

    @sopel.module.commands('gt-setradius')
    @sopel.module.example('.gt-setradius 300')
    def f_radiusset(bot, trigger):
        """Sets a radius"""
        if not trigger.group(2):
            bot.reply('No funny buggers.. give me a number')
            return
        radius = int(trigger.group(2))
        results = set_rad(radius)
        bot.db.set_nick_value(trigger.nick, 'gtradius', results)
        bot.say('I have now set your radius as %s km' % str(results))

    @sopel.module.commands('gt-getradius')
    @sopel.module.example('.gt-getradius')
    def f_getradius(bot,trigger):
        """get a radius"""
        results = bot.db.get_nick_value(trigger.nick, 'gtradius')
        bot.say('Yep its %s km' % str(results))


    @sopel.module.commands('gumtree')
    @sopel.module.example('.gumtree tools')
    def f_searchgumtree(bot, trigger):
        """conduct a search"""
        gt_search_string = trigger.group(2)
        ##get locid
        gt_search_locid = bot.db.get_nick_value(trigger.nick, 'gtlocid')
        ##get city details
        gt_search_city = str(get_city(gt_search_locid))
        gt_search_radius = bot.db.get_nick_value(trigger.nick, 'gtradius')
        bot.say('So tomorrow, we can figure out how to search gumtree for %s, within %s kms of %s ' % (gt_search_string, gt_search_radius, gt_search_city))
        
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




