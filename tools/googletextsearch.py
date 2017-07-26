
#### Because Google Place API counts text search as 10x requests for each query
#### this eats a lot of your daily quota
#### but if you have tons of query to play with, this most accurate way

import requests
import json

from allsetlists2017 import allsetlists as allsetlists

print(len(allsetlists), "setlists from setlists.fm")

### create a dictionary of every unique venue from the setlist dump from setlists.fm

fmvenues={}

for show in allsetlists:
	try:
		name = show['venue']['@name']
		setlistid = show['venue']['@id']
		city = show['venue']['city']['@name']
		state = show['venue']['city']['@state']

		fmvenues[setlistid] = {}

		fmvenues[setlistid]['name'] = name
		fmvenues[setlistid]['city'] = city
		fmvenues[setlistid]['state'] = state


	except:
		continue


print(len(fmvenues), "venues to seach in Google API")


### loop through the dictionary and query google places

venues = {}


for setlistid in fmvenues:
	try:
		name = fmvenues[setlistid]['name']
		city = fmvenues[setlistid]['city']
		state = fmvenues[setlistid]['state']

		finalname=name.replace(' ', '+')

		query=finalname+'+'+city+'+'+state

		base="https://maps.googleapis.com/maps/api/place/textsearch/json?query="

		API = 'GET_YOUR_OWN'

		call=base+query+API


		print(call)

		page = requests.get(call)

		jpage = page.json()

		#print(jpage['results'])

		print(len(jpage['results']))

		print(jpage['results'][0])

		best=jpage['results'][0]



		# putting the venues into a dic to save, with setlistid as key
		venues[setlistid]=best

		count+=1
		
		print("********")

	except:
		continue


# saving to local file

filename = 'allgoogletextresults.py'

handle = open(filename, 'w')

handle.write("allgoogletextresults=")

strvenues = str(venues)

handle.write(strvenues)

handle.close


print(len(fmvenues), "venues searched in Google API")



