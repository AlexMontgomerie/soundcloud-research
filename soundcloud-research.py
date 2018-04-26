#import libraries: json, re, url
import re
import json
import urllib

#open up html files
def getUsers(filename): 

  f = open(filename,"r")

  userList = []

  #load first line
  line = f.readline()
  while line:
    #reset user template
    #parse to find account username
    line = f.readline()
    if re.match("  <h2 class=\"userItem__title\">", line):
      #new user matched
      line = f.readline()
      #find username (after previous regex, form of href="/[str]" )
    
      match_tmp = re.match("(\ \ \ \ <a href=\"\/)([a-z,A-Z,0-9,\-]*)",line) #TODO: find 
      userList.append(match_tmp.group(2)) 
  return userList

def getUserInfo(userList):
  
  data = []
  
  #go through all users
  for user in userList:
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
                    "username"              : ""
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
  
        data.append(userDict)
        break
  
  return data
# (followings_count":)([0-9]+(,[0-9]+)*)
# (followers_count":)([0-9]+(,[0-9]+)*)
# (track_count":)([0-9]+(,[0-9]+)*)
# (reposts_count":)([0-9]+(,[0-9]+)*)
# (playlist_count":)([0-9]+(,[0-9]+)*)
# (comments_count":)([0-9]+(,[0-9]+)*)
# (city":")(.*?)(")
# (description":")(.*?)(")
# ("likes_count":)([0-9]+(,[0-9]+)*)
# ("playlist_likes_count":)([0-9]+(,[0-9]+)*)
# (username":")(.*?)(")


if __name__=="__main__":
  filename = "./data/soundcloud-hiphop.html"
  userList = getUsers(filename)
  data = getUserInfo(userList)
  #data = getUserInfo(['dipsartist'])
  json.dumps(data)
  with open('data.txt', 'w') as outfile:
    json.dump(data, outfile, indent=4, sort_keys=True) 
 
