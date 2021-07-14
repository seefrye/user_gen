#!/usr/bin/env python3
#Script to generate n number of random users, where n is a command line argument
#Intended use case: python user_gen.py 100 > FakeUsers.csv

import requests
import argparse
#from pprint import pprint #to help read API response
from decouple import config

#Passing arg int from command line to query limit
parser = argparse.ArgumentParser()
parser.add_argument("number", type=int)
args = parser.parse_args()
querystring = {"count":str(args.number)}

url = "https://fake-data-person.p.rapidapi.com/api/Persons/GetList"

headers = {
    'x-rapidapi-key': config("NAME_API_KEY"), #stored in .env
    'x-rapidapi-host': "fake-data-person.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
#print(querystring) #testing query string arg passthrough

names = response.json()
dCount = 1 #dept gen shenanigans
print("ID,LastName,FirstName,Email,UserName,JobTitle,Dept,Active,Password,")
for n in names:
    #Setting string vars
    id=str(n['id'])
    lName=n['lastName']
    fName=n['firstName']
    email=fName+"."+lName+id+"@example.com"+","
    username =fName+"."+lName+id+","
    active = "1," #Setting all to active for this use case
    pw = "1234," #password not actually set, just need non-null value
    #Generating relevant job titles from .env. (Weighted JOB1->JOB2->JOB3 for my needs)
    if n['id']%2 == 0:
        job = config("JOB1")+","
    elif n['id']%3 == 0:
        job = config("JOB2")+","
    else:
        job = config("JOB3")+","

    #Generating departments from .env
    if dCount < 5:
        dept = config('DEPT1')+","
        dCount= dCount+1
    else:
        dept = config('DEPT2')+","
        dCount = 1
    print(id+","+lName+","+fName+","+email+username+job+dept+active+pw)
#pprint(names) #pretty print of full API response
#print(response.text) #non-formatted full API response
exit