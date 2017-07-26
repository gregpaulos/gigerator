
#### This is a less 'request expensive' way of querying Google Places API than the text search
#### but it's less accurate


import requests
import json

from allsetlists2017 import allsetlists as allsetlists


print(len(allsetlists), "setlists from setlists.fm")

### create a dictionary of every unique venue from the setlist dump from setlists.fm

fmvenues={}

wrongcount = 0

for show in allsetlists:
	try:
		name = show['venue']['@name']
		setlistid = show['venue']['@id']
		city = show['venue']['city']['@name']
		state = show['venue']['city']['@state']
		fmlat = show['venue']['city']['coords']['@lat']
		fmlong = show['venue']['city']['coords']['@long']

		fmvenues[setlistid] = {}

		fmvenues[setlistid]['name'] = name
		fmvenues[setlistid]['city'] = city
		fmvenues[setlistid]['state'] = state
		fmvenues[setlistid]['lat'] = fmlat
		fmvenues[setlistid]['long'] = fmlong


	except:
		wrongcount += 1
		continue


print(len(fmvenues), "venues to seach in Google API")



venues={}


for setlistid in fmvenues:
	try:
		name = fmvenues[setlistid]['name']
		city = fmvenues[setlistid]['city']
		state = fmvenues[setlistid]['state']
		fmlat = fmvenues[setlistid]['lat']
		fmlong = fmvenues[setlistid]['long']


		finalname=name.replace(' ', '+')

		query=finalname+'+'+city+'+'+state


		base='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='

		API = 'GET_YOUR_OWN'

		call=base+fmlat+','+fmlong+'&radius=50000&keyword='+finalname+API



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


filename = 'allgooglelatlongresults.py'

handle = open(filename, 'w')

handle.write("allgooglelatlongresults=")

strvenues = str(venues)

handle.write(strvenues)

handle.close
