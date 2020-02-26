#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:50:05 2020
@author: roncavallo
See README for usage instructions
"""
import requests
import json
import sys
from creds import *


#prompt user for url. something like https://<company>.agilecraft.com/api is expected! dont forget get /api on the end 
# also format the apiendpoint like this : /users? or: /cities? or : blah
def CollectApiInfo():
     global instanceurl
     checkInput = ""
     while True:
         instanceurl = raw_input("Enter the url for your instance in following format EG. ""https://cprime.agilecraft.com"" : ")
         checkInput = raw_input("Is this your correct Jira Align instance you want to work with?  " + instanceurl + "  ")
         checkInput = str(checkInput)
         if (checkInput == 'N') or (checkInput == 'n'):
             print "Please enter your INSTANCE name again:  "
         else:
             break  
     instanceurl = instanceurl + "/api/"
     checkInput = ""
     global apiendpoint
     while True:
         apiendpoint = raw_input("Enter the api endpoint for your instance in following format EG. ""cities"" : ")
         checkInput = raw_input("Is this your correct API endpoint you want to work with?  " + apiendpoint + "  ")
         checkInput = str(checkInput)
         if (checkInput == 'N') or (checkInput == 'n'):
             print "Please enter your API endpoint again:  "
         else:
             break  
     return instanceurl,apiendpoint

#this function will retrieve JA data necessary for creating items in JA and put that information into arrays for later use.
def CollectUsrMenuItems():

# GET REGIONS    
    global regArr
    regArr = []
    regions = requests.get(instanceurl + "/regions", auth=("apitoken", "a5Z||0=4NWo9N+i)4H87KFsy#P~Ra+h9^QHRIbSO"))
    dataReg = regions.json()
    for eachReg in dataReg['Results']:
        region = eachReg['Region']
        regionid = eachReg['ID']
        regArr.append("Region Name: " + region + " " + " / Region ID: " + str(regionid))
    #print regArr
    
#GET CITIES
    global citArr
    citArr = []
    cities= requests.get(instanceurl + "/cities",  auth=("apitoken", "a5Z||0=4NWo9N+i)4H87KFsy#P~Ra+h9^QHRIbSO"))
    dataCit = cities.json()
    for eachCit in dataCit['Results']:
        cityID = eachCit['ID']
        cityN = eachCit['Name']
        citArr.append("City Name: " + cityN + " " + " / City ID: " + str(cityID))
    
#GET ENTERPRISE HIERARCHY   
    global orgArr
    orgArr = []
    enterpriseH = requests.get(instanceurl + "/" + "/organizationStructures",  auth=("apitoken", "a5Z||0=4NWo9N+i)4H87KFsy#P~Ra+h9^QHRIbSO"))
    entData = enterpriseH.json()
    for eachOrg in entData['Results']:
        orgID = eachOrg['OrganizationStructureID']
        orgName = eachOrg['OrganizationStructureName']
        orgArr.append("Organization Name: " + orgName + " " + " / Organization ID: " + str(orgID))
        
#GET COST CENTERS
    global costArr
    costArr = []
    CostCenters = requests.get(instanceurl + "/" + "/costCenters",  auth=("apitoken", "a5Z||0=4NWo9N+i)4H87KFsy#P~Ra+h9^QHRIbSO"))
    costData = CostCenters.json()
    for costCen in costData['Results']:
        costCentID = costCen['ID']
        costCentName = costCen['Name']
        costArr.append("Costcenter Name: " + costCentName + " " + " / Costcenter ID: " + str(costCentID))
    
#Return all of the arrays that have been built in this function
    return regArr,citArr,orgArr,costArr

#This function is meant to take the arrays created by GetMenuItems and format them into menus that the user can pick from to send to JA in other functions that POST data.

def MenuChooser(message, arr):
    print message+'\n'
    count = 0
    choice = ""
    listlen = len(arr)
    for number in range(0,listlen):
        count = count + 1
        print str(count) + ":  "
        print arr[number] + " \n"
    choice = raw_input("Please type the menu number preceeding the ':' of your choice  eg: 1 2 or 3 etc: \n")
    choice = int(choice) 
    choice = (choice - 1) # Since I start the menu with the number 1, but the element number in the array starts at 0, make them match
    for menuitems in range(0, listlen):
        if menuitems is choice:
            print "Choice made: " + arr[choice] + " \n"
                
            
# This fuction is for collecting unique user-specific information for creating users such as email address etc. 
def CollectUserInfo():
    global UsrEmail
    UsrEmail = raw_input("Please enter the full email address of the user [eg: ron.cavallo@cprime.com]")
    if not UsrEmail:
        UsrEmail = raw_input("You must enter the full email address of the user [eg: ron.cavallo@cprime.com]")##This needs better checking 
    global UsrFN
    UsrFN = raw_input("Please enter the full first name of the new user [eg: Ron]")
    if not UsrFN:
        UsrFN = raw_input("You must enter the first name the user [eg: Ron]")
    global UsrLN
    UsrLN = raw_input("Please enter the last name of the new user [eg: Cavallo]")
    if not UsrLN:
        UsrFN = raw_input("You must enter the last name the user [eg: Cavallo]")
    return UsrEmail,UsrFN,UsrLN
    

#function to go through city data and get ID and name of city
def ParseCities(response):
    data = response.json()
    for eachCit in data['Results']:
        print(eachCit['ID']),(eachCit['Name'])

#function to go through user data to get user ID, email address, and Team Name memberships
# this code easily changed to UPDATE any user....
def ParseUsers(response):
    data = response.json()
    for eachUsr in data["Results"]:
        fn = eachUsr["FirstName"]
        ln = eachUsr["LastName"]
        print fn,ln
        for teams in eachUsr["Teams"]:
            s = teams["Name"] #hack to remove duplication in json for teams due to bug opened 2/3/20 by Ron C.
            t = teams["Name"]
            if t != s:
                print t

#This function does what is says it does. Duh.

def CreateUser(UsrE, UsrF, UsrL):
    UsrData = { "email" : UsrE, "FirstName" : UsrF, "LastName" : UsrL, "RoleID": "6", "Title": "CRM+ User", "EnterpirseHierarchy" : "16", "RegionID" : "1","CityID" : "14","CostCenterID" : "1" }
    header = {"content-type": "application/json"}
    NewUser = requests.post(url = instanceurl+apiendpoint,data=json.dumps(UsrData), headers=header, verify=False, auth=(username, jatoken))
    print NewUser.status_code
    
# This function creates a region if you specify you want to create one

#def CreateRegion():
    
####################################################################################################################################################################################
# MAIN
# First get the instance url that we are going to hit
# Determine if we are just grabbing information and exporting or if we are going to create user(s) with team assignements etc.
#

CollectApiInfo()
#print jatoken,username,instanceurl+apiendpoint,AddUsr

responseReq = requests.get(instanceurl + apiendpoint, auth=(username, jatoken))
print responseReq

if apiendpoint == "/cities?" or "cities":
    addCity = raw_input("Do you want to create a new City in your instance? [Y/N]:"+'\n') or "N"
    if addCity == "Y" or "y":
        print "Here is a list of all cities in your instance \n"
        ParseCities(responseReq)
        
       

if apiendpoint == "/users?" or "/users" or "user" or "users":
    addUsr = raw_input("Do you want to create a new user? [Y/N]:"+'\n') or "N"
    if addUsr == "Y" or "y":
        CollectUsrMenuItems()
        MenuChooser('What Region would you like to put your user into? \n', regArr)
        MenuChooser('What City do you want to assign to your user? \n', citArr)
        MenuChooser('What Organization do you want to assign to your user? \n', orgArr)
        CollectUserInfo()
        #CreateUser(UsrEmail,UsrFN,UsrLN)
    else:
        print "Here is a list of all users in your instance"
        ParseUsers(responseReq)

#if apiendpoint == "/regions?" or "/regions" or "/region":
#    if addReg == "Y" or "y":
        
    
    
    
