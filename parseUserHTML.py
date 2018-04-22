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
  userTemplate = {"username" : "", "pro" : "", "location" : "", "followers" : "", "tracks" : ""}
  #print(line)
  #parse to find account username
  line = f.readline()
  if re.match("  <h2 class=\"userItem__title\">", line):
    #new user matched
    line = f.readline()
    #find username (after previous regex, form of href="/[str]" )
    userTemplate[""] = re.match("",line) #TODO: find 
    #the rest are optional

    while !(pro || location || followers || tracks):
      #if new section, break
      if re.match("<div class=\"sc-media-content\">"):
        #update userList
        break
      #location (3 lines after   <h3 class="userItem__details sc-type-light">)
      
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
