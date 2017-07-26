
#### Takes the googleID you've gotten from the previous Google Places API text search
#### and re-query Google Places API to get more info

import requests
import json

from allgoogletextresults import allgoogletextresults as allgoogleresults



#create a dictionary to store the new results from google
venues={}

# loop through the old google results to grab the googleID 
# and use it to query Google Places API for more info
for setlistid in allgoogleresults:
	try:
		googleid = allgoogleresults[setlistid]['place_id']

		print(googleid)

		base='https://maps.googleapis.com/maps/api/place/details/json?placeid='

		API = 'GET_YOUR_OWN'

		call=base+googleid+API


		print(call)
		print("********")


		page = requests.get(call)

		jpage = page.json()

		best=jpage['result']

		print(best)

		# putting the venues into a list to save
		venues[setlistid]=best


		
	except:
		continue

			


filename = 'allgoogledetailsresults.py'

handle = open(filename, 'w')

handle.write("allgoogledetails=")

strvenues = str(venues)

handle.write(strvenues)

handle.close




