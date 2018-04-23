#import libraries: json, re, url
import re
import json
import urllib

#list of search result items


#open up html files
filename = "./soundcloud-hiphop.html"
f = open(filename,"r")
'''
for line in f:
  #parse line
  tmp = 
  #append to json list
'''

userList = []

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
    #the rest are optional

    pro       = re.match("",line) #TODO: match for pro account
    location  = re.match("",line) #TODO: match for location
    followers = re.match("(<li title=\")([0-9,\.]+)( followers)",line) #TODO: match for number of followers
    tracks    = re.match("(<li title=\")([0-9,\.]+)(\ tracks)",line) #TODO: match for number of tracks

    while not (pro or location or followers or tracks):
      #if new section, break
      if re.match("<div class=\"sc-media-content\">"):
        #update userList
        break
      #location (3 lines after   <h3 class="userItem__details sc-type-light">)
      
      #read a new line
      line = f.readline()
      
      pro       = re.match("",line) #TODO: match for pro account
      location  = re.match("",line) #TODO: match for location
      followers = re.match("",line) #TODO: match for number of followers
      tracks    = re.match("",line) #TODO: match for number of tracks

      if pro:
        userTemplate["pro"] = pro

      if location:
        userTemplate["location"] = location

      if followers:
        userTemplate["followers"] = followers
      
      if tracks:
        userTemplate["tracks"] = tracks

    #update userList

print("DONE!")
