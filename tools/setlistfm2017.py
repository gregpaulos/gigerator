import requests
import json
import math


# this gets every setlist in 2017 from the website setlist.fm, which can parse by venue and band and setlist:


getrequest = 'http://api.setlist.fm/rest/0.1/search/setlists.json?year=2017&countryCode=US'

page = requests.get(getrequest)

jpage = page.json()


print(jpage)

#to get the number of pages of venues for setlist.fm response 
numpages = float()

numpages = int(jpage['setlists']['@total'])/20

#rounds up to an integer
numpages = math.ceil(numpages)



#create a list to put the venues in
mysetlist = list()

print(numpages)


# will iterate thru all pages on stelistfm
for count in range(1, numpages+1):
	newgetrequest = getrequest+'&p='+str(count)
	print(newgetrequest)

	page = requests.get(newgetrequest)

	try:
		jpage = page.json()

		# putting the venues into a list to save
		for setlist in jpage['setlists']['setlist']:
			mysetlist.append(setlist)

	except:
		continue


# save the list in a file

filename = 'allsetlists2017.py'

handle = open(filename, 'w')

handle.write("allsetlists=")

strsetlist = str(mysetlist)

handle.write(strsetlist)

handle.close
