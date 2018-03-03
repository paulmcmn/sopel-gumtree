from __future__ import print_function
import re, requests, os
import urllib
import json

url_base = 'https://www.gumtree.com.au'
url_loc_search = 'https://www.gumtree.com.au/j-suggest-location.json?query='

url_content_search = 'https://www.gumtree.com.au/ws/search.json?categoryId={}&keywords={}&locationId={}&locationStr={}&pageNum=1&pageSize=24&previousCategoryId=0&radius={}&searchFromSearchBar=true&sortByName=date' \

gtauradius = [0, 2, 5, 10, 20, 50, 100, 250, 500]
default_locid = 0
default_city = 'Australia'
default_rad = 0 ## default with no location set
default_rad_locpresent = 100 ## defaull radius where a location is specified
default_category = 0



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
                ##TODO if file doesnt exist, always add the default location information.
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

def search_gumtree(locid,radius,term):

    ##TODO support error handling
    if radius is None:
        radius = default_rad_locpresent ##setting radius assuming locid is not null

    if locid is None: ## if location id is null then set everything to default to australia
        locid = default_locid
        radius = default_rad
        city = default_city
    else:
        city = get_city(locid) ## loc id is formed, thus pickup city and format appropriately

    searchstr = url_content_search.format(default_category, urllib.parse.quote(term), locid.strip('_'), urllib.parse.quote(city), str(radius))
    print(searchstr)
    request = requests.get(searchstr)
    if request.status_code == 200:

        return request.text
    else:
        # TODO: Add error handlings
        print("Server returned code: " + str(request.status_code))
        print(searchstr)
        return []


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
            return None
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
        results = json.loads(search_gumtree(gt_search_locid,gt_search_radius,gt_search_string))

        responses = str(results['data']['breadCrumbs']['numberFound'])
        bot.say('%s results found on gumtree for %s, within %s kms of %s ' % (responses, gt_search_string, gt_search_radius, str(gt_search_city)))
        count = 0
        for result in results['data']['results']['resultList']:
            print('trying to print result')
            print(result)
            if count == 3:
                break
            bot.say('%s, posted %s' % (str(result['title']), str(result['age'])))
            count = count + 1

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
