from django.db import models
from django.contrib.auth.models import User

### the venues
# initially created with data from setlist.fm API
# then queried google places API to get more info
# and ensure accuracy

class Venue(models.Model):
    name = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    state = models.CharField(max_length=1000)
    statecode = models.CharField(max_length=1000)
    setlistfmwebsite = models.CharField(max_length=1000)
    setlistfmidcode = models.CharField(max_length=1000)
    fmlat = models.CharField(max_length=1000)
    fmlong = models.CharField(max_length=1000)
    googleid = models.CharField(max_length=1000)
    googlename= models.CharField(max_length=1000)
    googleaddress = models.CharField(max_length=1000)
    googlephone = models.CharField(max_length=1000)
    googlewebsite= models.CharField(max_length=1000)
    googlehours = models.CharField(max_length=1000)



### the user-generated reviews
# has one-to-one relationship with venue

class Review(models.Model):
    
    overall_rating = models.IntegerField()
    how_well_was_the_show_advertised = models.IntegerField(null=True, blank=True)
    did_the_promoter_pay_as_agreed = models.IntegerField(null=True, blank=True)
    manager_and_staff = models.IntegerField(null=True, blank=True)
    sound = models.IntegerField(null=True, blank=True)
    lights = models.IntegerField(null=True, blank=True)
    audience = models.IntegerField(null=True, blank=True)
    green_room = models.IntegerField(null=True, blank=True)
    how_well_did_they_follow_the_rider = models.IntegerField(null=True, blank=True)
    parking = models.IntegerField(null=True, blank=True)
    neighborhood = models.IntegerField(null=True, blank=True)
    comments = models.TextField(max_length=100000)
    venue = models.ForeignKey(Venue)



### reviews grabbed from google API
# has a one-to-one relationship with venue

class GoogleReview(models.Model):
    
    review = models.TextField()
    rating = models.IntegerField()
    venue = models.ForeignKey(Venue)



### Bands that have played at the venues in the db 
# From the shows listed on the setlist.fm website
# Many to many relationship with venues
# put that relationship through 'Show' model so can add date of show

class Band(models.Model):
    name = models.CharField(max_length=1000)
    musicbrainid = models.CharField(max_length=1000)
    setlistfmwebsite = models.CharField(max_length=1000)
    venue = models.ManyToManyField(Venue, through='Show')



### model that maintains many to many relationship between band and venue
# while adding the date of the show (when the band played the venue)

class Show(models.Model):
    band = models.ForeignKey(Band)
    venue = models.ForeignKey(Venue)
    showdate = models.DateField()



### a model to augment django's user model
# allows a user to have a many to many relationship with bands
# (i.e a user can be a musician in many bands, and bands have different musicians as members)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    band = models.ManyToManyField(Band)


