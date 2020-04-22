#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:50:05 2020
@author: roncavallo
See README for usage instructions
"""
import requests
import json
from creds import *


# This collects all of the information about the server instance and api endpoint you want to work with and formats the url properly.
# This is the only place that the apiendpoint or the url should be manipulated or it breaks the rest of the routines that depend upon it.
def CollectApiInfo():
    global apiendpoint
    global instanceurl
    apiendpoint = raw_input("Enter the api endpoint for your instance in following format EG. ""cities"". It is very important that you spell this endpoint correctly. Please refer to the api documents E.G https://cprime.agilecraft.com/api-docs/public/ for the apiendpoints available : ")
    instanceurl = raw_input("Enter the url for your instance in following format EG. ""https://cprime.agilecraft.com"" : ")
    ChkInput = raw_input("Is this your correct instance and endpoint you want to work with?  " + instanceurl + " : " + apiendpoint + "  ")
    if (ChkInput == "N") or (ChkInput == "n"):
       CollectApiInfo()
    else:
        instanceurl = instanceurl + "/api" ##### Mess with these couple of lines, and break all of the other defs! 
        apiendpoint = "/" + apiendpoint.lower()
        return apiendpoint, instanceurl
        
#reuse this function to check if the user sees that they entered information correctly after reviewing it
def ChkInput(Input):
    while True:
        if (Input == 'N') or (Input == 'n'):
            return input
        else:
            break

#this function will retrieve JA data necessary for creating items in JA and put that information into arrays for later use.
            
def CollectUsrMenuItems():
# GET REGIONS
    print instanceurl+apiendpoint
    global regArr
    regArr = []
    regions = requests.get(instanceurl + "/regions", auth=(username, jatoken))
    dataReg = regions.json()
    for eachReg in dataReg['Results']:
        region = eachReg['Region']
        regionid = eachReg['ID']
        regArr.append("Region Name: " + region + " " + " / Region ID: " + str(regionid))
    #print regArr
    
#GET CITIES
    global citArr
    citArr = []
    cities= requests.get(instanceurl + "/cities",  auth=(username, jatoken))
    dataCit = cities.json()
    for eachCit in dataCit['Results']:
        cityID = eachCit['ID']
        cityN = eachCit['Name']
        citArr.append("City Name: " + cityN + " " + " / City ID: " + str(cityID))
    
#GET ENTERPRISE HIERARCHY   
    global orgArr
    orgArr = []
    enterpriseH = requests.get(instanceurl + "/organizationStructures",  auth=(username, jatoken))
    entData = enterpriseH.json()
    for eachOrg in entData['Results']:
        orgID = eachOrg['OrganizationStructureID']
        orgName = eachOrg['OrganizationStructureName']
        orgArr.append("Organization Name: " + orgName + " " + " / Organization ID: " + str(orgID))
        
#GET COST CENTERS
    global costArr
    costArr = []
    CostCenters = requests.get(instanceurl + "/costcenters",  auth=(username, jatoken))
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
    UsrFN = raw_input("Please enter the full first name of the new user [eg: Jimeny]")
    if not UsrFN:
        UsrFN = raw_input("You must enter the first name the user [eg: Jimeny]")
    global UsrLN
    UsrLN = raw_input("Please enter the last name of the new user [eg: Cricket]")
    if not UsrLN:
        UsrFN = raw_input("You must enter the last name the user [eg: Cricket]")
    return UsrEmail,UsrFN,UsrLN
    


#function to go through user data to get user ID, email address, and Team Name memberships
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

#These functions create objects as per their name using POST commands 

def CreateUser(UsrE, UsrF, UsrL):
    UsrData = { "email" : UsrE, "FirstName" : UsrF, "LastName" : UsrL, "RoleID": "6", "Title": "CRM+ User", "EnterpirseHierarchy" : "16", "RegionID" : "1","CityID" : "14","CostCenterID" : "1" }
    #header = {"content-type": "application/json"}
    header = {"content-type": "appilcation/json", "Accept": "text/plain"}
    NewUser = requests.post(url = instanceurl+apiendpoint,data=json.dumps(UsrData), headers=header, verify=False, auth=(username, jatoken))

# This function creates a city with a post. Contrary to API documentation, these are the only two fields required to create a field
def CreateCity(newName, existingRegionID):
    paramData = {"Name" : newName, "RegionID" : existingRegionID}
    header = {"Content-Type": "application/json"}
    newCityPost = requests.post(url = instanceurl+apiendpoint, data=json.dumps(paramData), headers=header, verify=True, auth=(username, jatoken))
    print (newCityPost.status_code)

# This function creates an organization with a post. You only need to specify the name of the new org the ID will be automatically generated
def CreateOrg(newName):
    paramData = {"Name" : newName}
    header = {"Content-Type": "application/json"}
    newOrgPost = requests.post(url = instanceurl+apiendpoint, data=json.dumps(paramData), headers=header, verify=True, auth=(username, jatoken))
    print (newOrgPost.status_code)



    
####################################################################################################################################################################################
# MAIN
# This is where we direct the user towards working code againsy their chosen api endpoint

#Collect api server and endpoint. Also collect all of the instance json infomation we need into arrays with CollectUsrMenuItems
CollectApiInfo()
CollectUsrMenuItems()


#build a query to the specified server and endpoint. Remember, the credential variables below should be defined in the creds.py that the README shows you how to build
responseReq = requests.get(instanceurl + apiendpoint, auth=(username, jatoken))

#break out into handing each endpoint differently as they will go through iteration in subsequent versions of API
#CITIES Endpoint
if "cities" in apiendpoint:
    addCity = raw_input("Do you want to create a new City in your Jira Align instance? [Y/N]:"+'\n')
    if (addCity == "Y") or (addCity == "y"):
        print "You must specify a NEW CITY NAME, and an EXISTING REGION ID NUMBER in order to add a new City. Here is a list of all Cities with City ID's and Regions with Region ID's in Jira Align from your instance \n"
        for cit in citArr:
            print cit
        for reg in regArr:
            print reg
        existRegionID = raw_input("Please enter the ID NUMBER of the EXISTING Region you would like to add your new City to [eg: US]")
        existRegionID = int(existRegionID)
        newCityName = raw_input("Please enter the name of the new City you would like to create [eg: Atlanta]")
        CreateCity(newCityName,existRegionID)
    else:
        print "Here is a list of all cities and thier IDs in Jira Align from your instance \n"
        for cit in citArr:
            print cit

#USERS endpoint
if "users" in apiendpoint:
    addUsr = raw_input("Do you want to create a new user? [Y/N]:"+'\n') or "N"
    if (addUsr == "Y") or (addUsr == "y"):
        CollectUsrMenuItems()
        MenuChooser('What Region would you like to put your user into? \n', regArr)
        MenuChooser('What City do you want to assign to your user? \n', citArr)
        MenuChooser('What Organization do you want to assign to your user? \n', orgArr)
        CollectUserInfo()
        #CreateUser(UsrEmail,UsrFN,UsrLN)
    else:
        print "Here is a list of all users in your Jira Align instance \n"
        ParseUsers(responseReq)

#ORGANIZATIONSTRUCTURES endpoint
if "organizationstructures" in apiendpoint:
    addOrg = raw_input("Do you want to create a new Organization in your instance? If 'No' we will just output a list of the exsiting organizations [Y/N]:"+'\n')
    if (addOrg== "Y") or (addOrg == "y"):
        print "Here is a list of all Organizations and thier IDs in Jira Align from your instance \n"
        for org in orgArr:
            print org
        newOrg = raw_input("Please enter the name of the new Organization you would like to create [eg: HR]")
        CreateOrg(newOrg)
    else:
        print "Here is a list of all cities and thier IDs in Jira Align from your instance \n"
        for org in orgArr:
            print org
        
    
