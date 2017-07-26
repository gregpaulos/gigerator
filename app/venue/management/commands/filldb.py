### This creates a Django command to fill the PostgreSQL db
### with data from the sqlite.db that I scraped from the web

import sqlite3
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from venue.models import Venue, Review, Band, GoogleReview, Profile, Show 
import datetime

class Command(BaseCommand):
    help = 'filling the db'

    def handle(self, *args, **options):
 
        with sqlite3.connect('db.sqlite3') as connection:
            c = connection.cursor()

            for row in c.execute("SELECT * FROM venue_venue"):
                print(row)

                v = Venue(name = row[1],
                    city = row[2],
                    state = row[3],
                    statecode = row[4],
                    setlistfmwebsite = row[5],
                    setlistfmidcode = row[6],
                    fmlat = row[7],
                    fmlong = row[8],
                    googleid = row[9],
                    googlename= row[10],
                    googleaddress = row[11],
                    googlephone = row[12],
                    googlewebsite= row[13],
                    googlehours = row[14])

                v.save()



            for row in c.execute("SELECT * FROM venue_googlereview"):
                print(row)


                v = Venue.objects.get(id=row[3])

                g = GoogleReview(review = row[1],
                    rating = row[2],
                    venue = v)

                g.save()

            for row in c.execute("SELECT * FROM venue_band"):
                print(row)


                
                b = Band(name = row[1],
                musicbrainid = row[2],
                setlistfmwebsite = row[3])

                b.save()


            count=0
            for row in c.execute("SELECT * FROM venue_show"):
                print(row)

                try:
                    b = Band.objects.get(id=row[1])
                except:
                    print ('couldnt do', row)
                try:
                    v = Venue.objects.get(id=row[2])
                except:
                    print ('couldnt do', row)

                showdate = row[3]
                try:
                    realdate = datetime.datetime.strptime(showdate, "%Y-%m-%d").date()
                except:
                    try:
                        realdate = datetime.datetime.strptime(showdate, "%m-%d-%Y").date()
                    except:
                        try:
                            realdate = datetime.datetime.strptime(showdate, "%d-%m-%Y").date()       
                        except:
                            continue
 
                sh = Show(band=b, venue=v, showdate = realdate)
              
                sh.save()

            print(count)





