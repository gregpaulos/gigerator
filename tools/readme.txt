GIGERATOR DATA COLLECTION

To get the initial data for the gigerator web app:

1. use setlistfm2017.py to scrape setlists.fm for all shows they have which occurred in the US in 2017 and save the resulting info in a local file. This gives us a lot of good raw data about venues, bands and their shows, but we’re going to get some more accurate info about each venue by using this to query Google Places API in next couple of steps

2. use googletextsearch.py to query Google Places API using their ‘text search’ feature. This will save the resulting info from google in a local file. Because Google Place API counts text search as 10x requests for each query this eats a lot of your daily quota but if you have tons of query to play with, this most accurate way (if not, use googlelatlongsearch.py to query the Google Places API ‘nearby search’ feature with the longitude and latitude).
The most important piece of info that was returned in this initial query to google was the googleID of the venue. We’re going to use that googleID to re-query google and get even more information about the venue

3. use  googledetails.py to query Google Places API again using the googleID for each venue to get more info about that venue. Saves info in a local file

4. put the information into a database
first can put in sqlitedb using putintosqlitedb.py 
then can migrate to postgreSQL db using command filldb