#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:50:05 2020
YOU MUST EDIT THE jatoken line with your own token!!!!!!!
@author: roncavallo
"""
import requests
import json

instanceurl = "https://cprime.agilecraft.com/api"
apiendpoint = "/users?"

# Edit the below to include YOUR token number
def getauth():
    global jatoken
    jatoken = "a5Z||0=4NWo9N+i)4H87KFsy#P~Ra+h9^QHRIbSO"
    global username
    username = "apitoken"
    return jatoken,username
    


#CollectApiInfo - Get the url of the instance and the api endpoint

def CollectApiInfo():
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
def ParseUsers(response):
    data = response.json()
    for eachUsr in data["Results"]:
        fn = eachUsr["FirstName"]
        ln = eachUsr["LastName"]
        print fn,ln
        for teams in eachUsr["Teams"]:
            t = teams["Name"]
            print t
        
#                if value == "Teams":
#                    print value
#    for eachUsr in data["Results"]:
#        print(eachUsr["ID"])
#        print(eachUsr["FirstName"])
#        print(eachUsr["LastName"])
        
     
            
            
#Authorize your access
getauth()
#CollectApiInfo()

print jatoken,username,instanceurl,apiendpoint

# Run a request to the instance and the apiendpoint and return results as json

responseReq = requests.get(instanceurl + apiendpoint, auth=(username, jatoken))
if apiendpoint == "/cities?":
    ParseCities(responseReq)

if apiendpoint == "/users?":
     ParseUsers(responseReq)
    

