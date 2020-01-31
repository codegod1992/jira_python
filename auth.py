#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:50:05 2020
YOU MUST EDIT THE jatoken line with your own token!!!!!!!
@author: roncavallo
"""
import requests
import json
from creds import *

#prompt user for url. something like https://<company>.agilecraft.com/api is expected! dont forget get /api on the end 
# also format the apiendpoint like this : /users? or: /cities? or : blah
    global instanceurl
    instanceurl = raw_input("Enter the url for your instance in following format EG. ""https://cprime.agilecraft.com"" : ")
    global apiendpoint
    apiendpoint = raw_input("Enter the api endpoint for your instance in following format EG. ""/cities?"" : ")
    return instanceurl,apiendpoint

#function to go through city data and get ID and name of city
def ParseCities(response):
    data = response.json()
    for eachCit in data['Results']:
        print(eachCit['ID'])
        print(eachCit['Name'])

#function to go through user data to get user ID, email address, and Team Name memberships
# this code easily changed to UPDATE any user....
def ParseUsers(response):
    data = response.json()
    for eachUsr in data["Results"]:
        fn = eachUsr["FirstName"]
        ln = eachUsr["LastName"]
        print fn,ln
        for teams in eachUsr["Teams"]:
            t = teams["Name"]
            print t

#next function here...
     
            

CollectApiInfo()

print jatoken,username,instanceurl,apiendpoint

# Run a request to the instance and the apiendpoint and return results as json
# Lets get going......

#use the requests method
responseReq = requests.get(instanceurl + apiendpoint, auth=(username, jatoken))
if apiendpoint == "/cities?":
    ParseCities(responseReq)

if apiendpoint == "/users?":
     ParseUsers(responseReq)
    

