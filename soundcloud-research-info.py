#import libraries: json, re, url
import re
import json
import urllib
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import dryscrape

regexGenres = [
  [re.compile(r"([H,h]ip [H,h]op)"),'hip hop'],
  [re.compile(r"([R,r]ap)"),'rap'],
  [re.compile(r"([J,j]azz)"),'jazz'],
  [re.compile(r"([R,r]ock)"),'rock'],
  [re.compile(r"([H,h]ouse)"),'house'],
  [re.compile(r"([E,e]lectronic)"),'electronic']
  ]

regexSkills = [
  [re.compile(r"([P,p]roducer)"),'producer'],
  [re.compile(r"([R,r]apper)"),'rapper'],
  [re.compile(r"([S,s]ing)"),'singer'],
  [re.compile(r"([G,g]uitar)"),'guitarist']
  ]

def getUserInfo(userList):
  
  data = []
  
  #go through all users
  for user in userList:
    print('processing user: '+user)
    response = urllib.urlopen('https://soundcloud.com/'+user)
    html = response.read()
    html = html.split('\n')
    for line in html:
      match_tmp = re.match("(\ \ <script>webpackJsonp\(\[\],)(.*?)(\);<\/script>)",line)
      if match_tmp:
        json_data = match_tmp.group(2)

        followings_count      = re.search('(followings_count\":)([0-9]+(,[0-9]+)*)',json_data)
        followers_count       = re.search('(followers_count\":)([0-9]+(,[0-9]+)*)',json_data)
        track_count           = re.search('(track_count\":)([0-9]+(,[0-9]+)*)',json_data)
        reposts_count         = re.search('(reposts_count\":)([0-9]+(,[0-9]+)*)',json_data)
        playlist_count        = re.search('(playlist_count\":)([0-9]+(,[0-9]+)*)',json_data)
        comments_count        = re.search('(comments_count\":)([0-9]+(,[0-9]+)*)',json_data)
        city                  = re.findall('(city\":\")(.*?)(\")',json_data)
        description           = re.search('(description\":\")(.*?)(\")',json_data)
        likes_count           = re.search('(\"likes_count\":)([0-9]+(,[0-9]+)*)',json_data)
        playlist_likes_count  = re.search('(\"playlist_likes_count\":)([0-9]+(,[0-9]+)*)',json_data)
        username              = re.search('(username\":\")(.*?)(\")',json_data)

        userDict = {
                    "followings_count"      : 0,
                    "followers_count"       : 0,
                    "track_count"           : 0,
                    "reposts_count"         : 0,
                    "playlist_count"        : 0,
                    "comments_count"        : 0,
                    "city"                  : "",
                    "description"           : "",
                    "likes_count"           : 0,
                    "playlist_likes_count"  : 0,
                    "username"              : "",
                    "skills"                : [],
                    "genres"                : []
                    }
        if followings_count:
          userDict["followings_count"] = followings_count.group(2)

        if followers_count:
          userDict["followers_count"] = followers_count.group(2)

        if track_count:
          userDict["track_count"] = track_count.group(2)

        if reposts_count:
          userDict["reposts_count"] = reposts_count.group(2)
  
        if playlist_count:
          userDict["playlist_count"] = playlist_count.group(2)

        if comments_count:
          userDict["comments_count"] = comments_count.group(2)

        if city:
          if len(city)==2:
            userDict["city"] = city[1][1]

        if description:
          userDict["description"] = description.group(2)

        if likes_count:
          userDict["likes_count"] = likes_count.group(2)

        if playlist_likes_count:
          userDict["playlist_likes_count"] = playlist_likes_count.group(2)

        if username:
          userDict["username"] = username.group(2) 
 
        #parse description
        for regex in regexSkills:
          skill_tmp = regex[0].search(userDict["description"])
          if skill_tmp:
            userDict["skills"].append(regex[1])
 
        for regex in regexGenres:
          genre_tmp = regex[0].search(userDict["description"])
          if genre_tmp:
            userDict["genres"].append(regex[1])
        
        data.append(userDict)
        break
  
  return data

def getUserInfo2(user):
  #r = requests.get("https://soundcloud.com/"+user)
  driver = webdriver.PhantomJS()
  driver.get("https://soundcloud.com/"+user)
  soup = BeautifulSoup(driver.text,"lxml") 

  userDict = {
    "followings_count"      : 0,
    "followers_count"       : 0,
    "track_count"           : 0,
    "reposts_count"         : 0,
    "playlist_count"        : 0,
    "comments_count"        : 0,
    "city"                  : "",
    "description"           : "",
    "likes_count"           : 0,
    "playlist_likes_count"  : 0,
    "username"              : "",
    "skills"                : [],
    "genres"                : []
  }
  
  #if(soup.find("table",class_="infoStats__table sc-type-small")):
  if(soup.find_all("tbody")): 
    print('here')
   

if __name__=="__main__":
  #userList = json.load(open('./data/users.json'))
  #data = getUserInfo(userList)
  getUserInfo2('bluenoterecords')
  #data = getUserInfo(['dipsartist'])
  #json.dumps(data)
  #with open('./data/user-data.json', 'w') as outfile:
  #  json.dump(data, outfile, indent=4, sort_keys=True) 
