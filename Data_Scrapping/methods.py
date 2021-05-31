import requests
import json
import tweepy
import time
import copy
import pandas
import csv   
from bs4 import BeautifulSoup
import numpy as np
from geopy.distance import distance
from db.user import User
from db.tweet_user import tweetUser
from db.tweets import Tweet

# Auth functions


def get_access(x):
    f = open(x, 'r')
    CK = []
    CS = []
    AT = []
    AS = []
    access_data = f.readline()
    while access_data != '':
        temp = access_data[:-1].split(';')
        CK.append(temp[0])
        CS.append(temp[1])
        AT.append(temp[2])
        AS.append(temp[3])
        access_data = f.readline()
    f.close()
    return CK, CS, AT, AS


def get_api(CK, CS, AT, AS):
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    try:
        if len(api.followers_ids(user_id='268201193')) >= 0:
            return api
    except:
        return None


def check_valid_tokens():
    # // file name of access token files
    CK, CS, AT, AS = get_access('twitter_access_keys.csv')
    print('We have ' + str(len(CK)) + ' keys')
    for i in range(len(CK)):
        api = get_api(CK[i], CS[i], AT[i], AS[i])
        try:
            print(i, len(api.followers_ids(user_id='268201193'))
                  > 0, ' : token is working')
        except tweepy.error.TweepError as e:
            print(i, e.reason)


def check_if_valid_api(api, i):
    try:
        print(i, len(api.followers_ids(user_id='268201193'))
              >= 0, ' : token is working')
        return len(api.followers_ids(user_id='268201193')) >= 0
    except tweepy.error.TweepError as e:
        print(i, e.reason)
        return False
    except AttributeError as e:
        print(i, ': key currently not valid - ', e)
        return False

# Tweet Methods

# TODO : if twt_count == numItems recall function (while testing atleast)


def get_tweets(api, query, point, numItems=100):
    twt_count = 0
    try:
        point_details = get_district_data_from_KML(point)
    except AttributeError as e:
        print(e, '. You have chosen a state as a point, functionality not added yet')
        return twt_count

    tweets = tweepy.Cursor(api.search, q=query.lower(), geocode=str(point_details['rms_coordinates'][0])+','+str(
        point_details['rms_coordinates'][1])+',' + str(point_details['radius']['rms_radius'])+'mi').items(numItems)
    print('here')

    for twt in tweets:
        tweet = twt._json
        user = api.get_user(tweet['user']['id'])._json
        # print('user', user['screen_name'], 'tweet id:', tweet['id_str'])
        print('here1')
        fields1=[point,user['id_str'],tweet['id_str'],point_details['state'],
            str(point_details['mean_coordinates'][0]),query,
            str(point_details['mean_coordinates'][1])]

        with open(r'userWhoTweeted.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields1)

        fields2 = [tweet['retweet_count'],point,user['id_str'],query,tweet['id_str'],
            user['screen_name'],tweet['text'],user['name']]

        with open(r'tweets2.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields2)
        
        twt_count += 1

    return twt_count


def get_district_data_from_KML(query):
    with open('./map.kml') as f:
        soup = BeautifulSoup(f, 'lxml-xml')

    district = soup.find(text=query)
    district = district.parent.parent.parent.parent

    # To clear memory
    del soup

    district_name = district.ExtendedData.find(
        'Data', attrs={'name': 'DISTRICT'}).value.contents[0]
    state_name = district.ExtendedData.find(
        'Data', attrs={'name': 'ST_NM'}).value.contents[0]
    coordinates = district.Polygon.outerBoundaryIs.LinearRing.coordinates.contents[0].split(
        ' ')
    latitudes = []
    longitudes = []
    for idx, coordinate in enumerate(coordinates):
        coordinate = coordinate.split(',')
        coordinates[idx] = (float(coordinate[1]), float(coordinate[0]))
        longitudes.append(float(coordinate[0]))
        latitudes.append(float(coordinate[1]))
    latitudes = np.array(latitudes)
    longitudes = np.array(longitudes)

    rms_latitude = np.sqrt(np.mean(latitudes**2))
    mean_latitude = np.mean(latitudes)
    rms_longitude = np.sqrt(np.mean(longitudes**2))
    mean_longitude = np.mean(longitudes)
    mean_coordinates = (mean_latitude, mean_longitude)
    rms_coordinates = (rms_latitude, rms_longitude)

    radius = []
    idx_rms_lat = (np.abs(latitudes - rms_latitude)).argmin()
    closest_to_rms_latitude = coordinates[idx_rms_lat]
    radius.append(distance(rms_coordinates, closest_to_rms_latitude).miles)

    idx_rms_long = (np.abs(longitudes - rms_longitude)).argmin()
    closest_to_rms_longitude = coordinates[idx_rms_long]
    radius.append(distance(rms_coordinates, closest_to_rms_longitude).miles)

    idx_mean_lat = (np.abs(latitudes - mean_latitude)).argmin()
    closest_to_mean_latitude = coordinates[idx_mean_lat]
    radius.append(distance(mean_coordinates, closest_to_mean_latitude).miles)

    idx_mean_long = (np.abs(longitudes - mean_longitude)).argmin()
    closest_to_mean_longitude = coordinates[idx_mean_long]
    radius.append(distance(mean_coordinates, closest_to_mean_longitude).miles)

    radius = np.array(radius)
    mean_radius = np.mean(radius)
    rms_radius = np.sqrt(np.mean(radius**2))

    return {
        'district': district_name,
        'state': state_name,
        'mean_coordinates': mean_coordinates,
        'rms_coordinates': rms_coordinates,
        'closest_to_rms_latitude': closest_to_rms_latitude,
        'closest_to_rms_longitude': closest_to_rms_longitude,
        'closest_to_mean_latitude': closest_to_mean_latitude,
        'closest_to_mean_longitude': closest_to_mean_longitude,
        'radius': {
            'rms_latitude_radius': radius[0],
            'rms_longitude_radius': radius[1],
            'mean_latitude_radius': radius[2],
            'mean_longitude_radius': radius[3],
            'mean_radius': mean_radius,
            'rms_radius': rms_radius
        }
    }


# TODO: Add support for states
def get_all_query_terms():
    with open('./map.kml') as f:
        soup = BeautifulSoup(f, 'lxml-xml')

    districts = soup.find_all('Data', attrs={'name': 'DISTRICT'})
    states = soup.find_all('Data', attrs={'name': 'ST_NM'})

    del soup

    query_terms = set()
    for district in districts:
        query_terms.add(district.value.contents[0])

    for state in states:
        query_terms.add(state.value.contents[0])

    return list(query_terms)


def get_all_points():
    with open('./map.kml') as f:
        soup = BeautifulSoup(f, 'lxml-xml')

    districts = soup.find_all('Data', attrs={'name': 'DISTRICT'})
    # states = soup.find_all('Data',attrs={'name':'ST_NM'})

    del soup

    query_terms = set()
    for district in districts:
        query_terms.add(district.value.contents[0])

    return list(query_terms)
