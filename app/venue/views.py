from django.shortcuts import render, redirect
from django.db.models import Avg
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from watson import search as watson

from venue.models import Venue, Review, Band, GoogleReview, Profile, Show 
from venue.forms import VenueForm, ReviewForm


### page for sign-up

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('bandsearchform')
	else:
		form = UserCreationForm()
	return render(request, 'signup.html', {'form': form})




### page where signed-in user sees their recent gigs

#@login_required
def mygigs(request):

	username = None
	userid = None
	if request.user.is_authenticated():
		username = request.user.username
		userid = request.user.id


		try:

			# grab this users profile
			profile = Profile.objects.get(user_id=request.user.id)
			
			# from the profile, grabs the band(s) their in
			bands = profile.band.all()

			# creates a dictionary to the shows for this users bands:
			venuesdic = {}

			# loop through each band they're in
			for band in bands:
				venuesdic[band.name] = {}
				#grab all shows for this band and order by date
				bandshows = Show.objects.filter(band_id=band.id).order_by('-showdate')

				# loop through each show and put the info in the dictionary, except leaving dates an empty dic for now:
				for show in bandshows:
					venuesdic[band.name][show.venue.name] = {}
					venuesdic[band.name][show.venue.name]['id'] = show.venue.id
					venuesdic[band.name][show.venue.name]['city'] = show.venue.city
					venuesdic[band.name][show.venue.name]['state'] = show.venue.state
					venuesdic[band.name][show.venue.name]['dates'] = {}


				# loop through each show again, and if dates exist for the show, add all the show dates to the nested dictionary
				for show in bandshows:
					if show.showdate == None:
						continue 
					else:
						venuesdic[band.name][show.venue.name]['dates'][show.showdate] = venuesdic.get(show.showdate, 0) + 1



		except:
			venuesdic = {}
			bands={}



		return render(request, 'mygigs.html', {'userid': userid, 'bands': bands, 'venuesdic': venuesdic, 'nbar':'mygigs'})

	else:
		return render(request, 'mygigsnotsignedin.html', {'nbar':'mygigs'})



# page to display details of a specific venue
def venue(request, venueID):

	venue = Venue.objects.get(id=venueID)

	bands = venue.band_set.all()

	bandsdic={}

	for band in bands:
		bandsdic[band.name] = bandsdic.get(band.name, 0) + 1


	reviews = Review.objects.filter(venue_id=venueID)

	avgreview = Review.objects.filter(venue_id=venueID).aggregate(Avg('overall_rating'))

	googlereviews = GoogleReview.objects.filter(venue_id=venueID)

	return render(request, 'venue.html', {'venue': venue, 'reviews': reviews, 
		'bands': bandsdic, 'googlereviews': googlereviews, 'avgreview': avgreview,
		})




### page to display details of a specific review
def reviewdetails(request, reviewID):

	reviewID = int(reviewID)

	review = Review.objects.get(id=reviewID)

	# creates a dictionary out of the items in the review
	reviewdic = review.__dict__

	# cleaning it up for display	
	reviewdicclean= {}

	# replaces underscore (django's default) with space for cleaner display in page
	for key, item in reviewdic.items():
		newkey = key.replace('_', ' ')
		reviewdicclean[newkey]=item


	# grab the venue info for this review
	venueID = review.venue_id

	venue = Venue.objects.get(id=venueID)

	return render(request, 'reviewdetail.html', {'venue': venue, 'review': reviewdic, 'cleanreview':reviewdicclean})



### page which allows user to submit a review of a venue
def reviewform(request, venueID):

	venueID=venueID

	venue = Venue.objects.get(id=venueID)



	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			
			data = form.cleaned_data

			r = Review(overall_rating = data['overall_rating'],
				comments = data['comments'],
				did_the_promoter_pay_as_agreed = data['how_well_was_the_show_advertised'],
				how_well_was_the_show_advertised = data['how_well_was_the_show_advertised'],
				manager_and_staff= data['manager_and_staff'],
				sound = data['sound'],
				lights = data['lights'],
				audience = data['audience'],
				green_room = data['green_room'],
				how_well_did_they_follow_the_rider = data['how_well_did_they_follow_the_rider'],
				parking = data['parking'],
				neighborhood = data['neighborhood'], 
				venue_id=venueID)


			r.save()


			return render(request, 'thanksreview.html', {'venue': venue})


		else:
			print(form.errors)

	else:
		form= ReviewForm()


	return render(request, 'reviewform.html', {'form': form, 'venue': venue})



### page which allows user to add a venue
def venueform(request):

	if request.method == 'POST':
		form = VenueForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data

			name = data['name']
			city = data['city']
			state = data['state']


			newvenue = Venue(name=name, city=city, state=state)
			newvenue.save()


			#### CREATE THANKS VENUE REROUTE HERE

			venue=Venue.objects.get(name=name)

			# reviews=[]

			# return render(request, 'venue.html', {'venue': venue, 'reviews': reviews})

			return render(request, 'thanksvenue.html', {'venue': venue})

		else:
			print(form.errors)

	else:
		form= VenueForm()

	return render(request, 'venueform.html', {'form': form})



### Page to allow user to search for venues
def venuesearchform(request):
	return render(request, 'venuesearchform.html', {'nbar':'search'})


### Page which returns search results
def venuesearch(request):
	errors=[]
	venues=[]

	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			errors.append('Enter a search term')
		else:
			
			search_results = watson.filter(Venue, q)
			
			for result in search_results:
				v = Venue.objects.get(id=result.id)
				if v.name == "":
					continue
				else:
					venues.append(v)


	return render(request, 'venuesearch.html', {'venues': venues, 'errors':errors, 'nbar':'search'})



### Page to allow user to search for bands
@login_required
def bandsearchform(request):
	return render(request, 'bandsearchform.html')


### Page which returns search results for bands
@login_required
def bandsearch(request):
	errors=[]
	bands=[]

	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			errors.append('Enter a search term')
		else:
			
			search_results = watson.filter(Band, q)
			
			for result in search_results:
				b = Band.objects.get(id=result.id)
				if b.name == "":
					continue
				else:
					bands.append(b)



	return render(request, 'bandsearch.html', {'bands': bands, 'errors':errors})


### page for a registered user to add a band to his/her profile:

@login_required
def bandadd(request, bandID):

	bandID=bandID

	band = Band.objects.get(id=bandID)


	if request.method == 'POST':

		username = None
		userid = None
		if request.user.is_authenticated():
			username = request.user.username
			userid = request.user.id

			band = Band.objects.get(id=bandID)


			try:
				# grab this users profile
				p = Profile.objects.get(user_id=userid)
				p.band.add(band)
				p.save()

			except:
				# if user doesn't have a pre-existing profile

				u = User.objects.get(id=userid)
				p = Profile(user=u)
				p.save()


				p.band.add(band)
				p.save()


			return redirect('mygigs')
	

	return render(request, 'bandadd.html', {'band': band})



### Page about the site
def about(request):
	return render(request, 'about.html', {'nbar':'gigerator'})



