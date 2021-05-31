import json
import time
from datetime import datetime
import copy
import random
from methods import get_tweets, get_api, get_access, check_if_valid_api
from db.mongo_setup import init, disconnect_conn
from location_terms import tweeted_from, search_term, added_terms

if __name__ == "__main__":
    random.seed(1)
    # username = input('Enter username for database: ')
    # password = input('Enter password for database: ')
    # Setup user database
    # init(username=username, password=password)

    CK, CS, AT, AS = get_access('twitter_access_keys.csv')

    i = 0
    twt_count_asked = int(input('How many tweets would you like? '))
    startTime = datetime.now()
    tweets = 0
    query_terms = search_term
    point_terms = tweeted_from#list(set(tweeted_from + added_terms))
    while (tweets < twt_count_asked):
        try:
            api = get_api(CK[i], CS[i], AT[i], AS[i])
            if(check_if_valid_api(api, i)):
                query = random.randrange(0, len(query_terms), 1)
                point = 0#random.randrange(0, len(point_terms), 1)
                print('Currently processing ' +
                      query_terms[query] + ' from ' + point_terms[point])
                tweets += get_tweets(api, query_terms[query],
                                     point_terms[point], numItems=25)
            else:
                i += 1
        except:
            if(i > 26):
                rem_time = 0#15*60 - (datetime.now() - startTime).seconds
                print('All keys exhausted; Have to go to sleep, wake up in ' +
                      str(rem_time) if rem_time > 0 else str(0) + ' seconds!')
                if(rem_time > 0):
                    time.sleep(rem_time)
                startTime = datetime.now()
                i = 0
            else:
                i += 1
    # disconnect_conn()
