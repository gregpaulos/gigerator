
from django import forms
from venue.models import Review

class VenueForm(forms.Form):
	name = forms.CharField(max_length=100)
	city = forms.CharField(max_length=100)
	state = forms.CharField(max_length=100)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('overall_rating', 'how_well_was_the_show_advertised', 'did_the_promoter_pay_as_agreed', 'manager_and_staff', 'sound', 'lights', 
        	'audience', 'green_room', 'how_well_did_they_follow_the_rider', 'parking', 
        	'neighborhood', 'comments')