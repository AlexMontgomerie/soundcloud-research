#import libraries: json, re, url
import re
import json
import urllib.request
#list of search result items


#open up html files
filename = "./soundcloud-london.html"
f = open(filename,"r")
'''
for line in f:
  #parse line
  tmp = 
  #append to json list
'''

userList = []
count=0
#load first line
line = f.readline()
while line:
  #reset user template
  userTemplate = {'username' : '', 'pro' : False, 'location' : '', 'followers' : 0, 'tracks' : 0}
  #print(line)
  #parse to find account username
  line = f.readline()
  if re.match("  <h2 class=\"userItem__title\">", line):
    #new user matched
    line = f.readline()
    #find username (after previous regex, form of href="/[str]" )
    
    match_tmp = re.match("(\ \ \ \ <a href=\"\/)([a-z,A-Z,0-9,\-]*)",line) #TODO: find 
    userTemplate['username'] = match_tmp.group(2) 
    print(userTemplate['username'])
    
    '''
    #the rest are optional
    count += 1
    pro       = re.match("",line) #TODO: match for pro account
    location  = re.match("",line) #TODO: match for location
    followers_match = re.match("(<li title=\")([0-9,\.]+)( followers)",line) #TODO: match for number of followers
    tracks_match    = re.match("(<li title=\")([0-9,\.]+)(\ tracks)",line) #TODO: match for number of tracks

    if followers_match:    
      followers = followers_match.group(2)
    if tracks_match:
      tracks    = tracks_match.group(2)
    '''
    print("http://soundcloud.com/" + userTemplate['username'])
    req = urllib.request.Request('https://soundcloud.com/robotrump') 
    response = urllib.request.urlopen('https://soundcloud.com/robotrump')
    html = response.read()
    profile_json_match = re.match("(  <script>webpackJsonp\(\[\],)(.*?)(\);<\/script>)",html)
    print(profile_json_match)


'''
    while not (followers_match or tracks_match):
      #if new section, break
      if re.match("<div class=\"sc-media-content\">", line):
        #update userList
        break
      #location (3 lines after   <h3 class="userItem__details sc-type-light">)
      
      #read a new line
      line = f.readline()
      
      pro       = re.match("",line) #TODO: match for pro account
      location  = re.match("",line) #TODO: match for location
      followers_match = re.match("(<li title=\")([0-9,\.]+)( followers)",line) #TODO: match for number of followers
      tracks_match    = re.match("(<li title=\")([0-9,\.]+)(\ tracks)",line) #TODO: match for number of tracks

      if followers_match:    
        followers = followers_match.group(1)
        print(followers)
      if tracks_match:
        tracks    = tracks_match.group(1)
        print(tracks)      

     #update userList
'''

# RegEx for getting user json field
# (  <script>webpackJsonp\(\[\],)(.*?)(\);<\/script>)

print("DONE!")
print(count)
