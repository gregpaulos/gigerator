
import os
import sqlite3
import requests
import json
import math
import datetime

from allsetlists2017 import allsetlists as allsetlists
from allgoogledetailsresults import allgoogledetails




bands = {}



with sqlite3.connect('db.sqlite3') as connection:
	c = connection.cursor()

	### populate venues

	# first create a dictionary of unique bands (so aren't populating the same band twice)

	fmvenues={}

	for show in allsetlists:
		name = show['venue']['@name']
		setlistid = show['venue']['@id']
		city = show['venue']['city']['@name']
		try:
			state = show['venue']['city']['@state']
		except:
			state = 'NOTHING'
		try:
			statecode = show['venue']['city']['@stateCode']
		except:
			statecode = 'NOTHING'
		setlistfmwebsite = show['venue']['url']
		try:
			fmlat = show['venue']['city']['coords']['@lat']
		except:
			fmlat = 'NOTHING'
		try:
			fmlong = show['venue']['city']['coords']['@long']
		except:
			fmlong= 'NOTHING'


		fmvenues[setlistid] = {}

		fmvenues[setlistid]['name'] = name
		fmvenues[setlistid]['city'] = city
		fmvenues[setlistid]['state'] = state
		fmvenues[setlistid]['statecode'] = statecode
		fmvenues[setlistid]['fmlat'] = fmlat
		fmvenues[setlistid]['fmlong'] = fmlong
		fmvenues[setlistid]['setlistfmwebsite'] = setlistfmwebsite


	#this populates the DB with a venues table:

	c.execute("DROP TABLE IF EXISTS venue_venue") 
	c.execute("""CREATE TABLE venue_venue (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, 
		city TEXT, state TEXT, statecode TEXT, setlistfmwebsite TEXT, setlistfmidcode TEXT, 
		fmlat TEXT, fmlong TEXT, googleid TEXT, googlename TEXT, googleaddress TEXT,
		googlephone TEXT, googlewebsite TEXT, googlehours TEXT)""")

	for setlistid in fmvenues:
		name = fmvenues[setlistid]['name'] 
		city = fmvenues[setlistid]['city'] 
		state = fmvenues[setlistid]['state'] 
		statecode = fmvenues[setlistid]['statecode']
		fmlat = fmvenues[setlistid]['fmlat'] 
		fmlong = fmvenues[setlistid]['fmlong'] 
		setlistfmwebsite = fmvenues[setlistid]['setlistfmwebsite'] 

		try:
			googleid = allgoogledetails[setlistid]['place_id']
			print(googleid)
		except:
			googleid = 'NOTHING'
			print('NO GOOGLE ID')
			#print(show)

		try:
			googlename = allgoogledetails[setlistid]['name']
			print(googlename)
		except:
			googlename = 'NOTHING'

		try:
			googleaddress = allgoogledetails[setlistid]['formatted_address']
		except:
			googleaddress = 'NOTHING'

		try:
			googlephone = allgoogledetails[setlistid]['formatted_phone_number']
		except:
			googlephone = 'NOTHING'

		try:
			googlewebsite = allgoogledetails[setlistid]['website']
		except:
			googlewebsite = 'NOTHING'

		try:
			googlehours = str(allgoogledetails[setlistid]['opening_hours']['weekday_text'])
		except:
			googlehours = 'NOTHING'


		id=None

		data = [id, name, city, state, statecode, setlistfmwebsite, setlistid, fmlat, 
			fmlong, googleid, googlename, googleaddress, googlephone, googlewebsite, googlehours]

		
		c.execute("INSERT INTO venue_venue VALUES(?,?,?,?,?,?,?,?,?, ?, ?, ?, ?, ?, ?)", data)





	### populates bands:

	# first create a dictionary of unique bands (so aren't populating the same band twice)
	for show in allsetlists:
		name = show['artist']['@name']
		musicbrainid = show['artist']['@mbid']
		setlistfmwebsite = show['artist']['url']

		bands[musicbrainid] = {'musicbrainid' : musicbrainid, 'name' : name, 'setlistfmwebsite' : setlistfmwebsite}

		print(name)

	# then use it to populate DB:

	c.execute("DROP TABLE IF EXISTS venue_band") 
	c.execute("""CREATE TABLE venue_band (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, 
		musicbrainid TEXT, setlistfmwebsite TEXT)""")

	for band in bands:

		id = None

		data = [id, bands[band]['name'], bands[band]['musicbrainid'], bands[band]['setlistfmwebsite']]

		print(data[1])

		c.execute("INSERT INTO venue_band VALUES(?,?,?,?)", data)	




	### these create relationship tables between venues and bands:

	c.execute("DROP TABLE IF EXISTS venue_show") 
	c.execute("""CREATE TABLE venue_show (id INTEGER PRIMARY KEY AUTOINCREMENT, band_id INTEGER, 
		venue_id INTEGER, showdate DATE)""")

	for show in allsetlists:
		fmvenue = show['venue']['@id']
		fmband = show['artist']['@mbid']
		showdate = show['@eventDate']
		realdate = datetime.datetime.strptime(showdate, "%d-%m-%Y").date()


		# need to use the (fmvenue,) format or it will complain about bindings, essentially because it wants a tuple as the argument there
		for row in c.execute("SELECT id FROM venue_venue WHERE setlistfmidcode = (?)", (fmvenue,)): 
			myvenue = (row[0])



		for row in c.execute("SELECT id FROM venue_band WHERE musicbrainid = (?)", (fmband,)): 
			myband = (row[0])


		id = None

		data = [id, myband, myvenue, realdate]

		print(data[1])

		c.execute("INSERT INTO venue_show VALUES(?,?,?, ?)", data)

		

	### this is for the google reviews:

	c.execute("DROP TABLE IF EXISTS venue_googlereview") 
	c.execute("""CREATE TABLE venue_googlereview (id INTEGER PRIMARY KEY AUTOINCREMENT, review TEXT, rating INTEGER, 
		venue_ID INTEGER)""")


	for fmid, result in allgoogledetails.items():

		try:
			for review in result['reviews']:
				googlereview = review['text'] 
				rating = review['rating']

				# need to use the (fmvenue,) format or it will complain about bindings, essentially because it wants a tuple as the argument there
				for row in c.execute("SELECT id FROM venue_venue WHERE setlistfmidcode = (?)", (fmid,)): 
					myvenue = (row[0])

				id = None

				data = [id, googlereview, rating, myvenue]

				print(data[3])

				c.execute("INSERT INTO venue_googlereview VALUES(?,?,?, ?)", data)

		except:
			continue







