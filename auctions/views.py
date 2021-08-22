from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Bid, Listing
from .models import User
from auctions import models

from django import forms

class Createform(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.CharField()
    first_bid = forms.IntegerField()

class Bidform(forms.Form):
    new_bid = forms.IntegerField()


def index(request):
    # every on could see the index 
    #get all listings
    bids = Bid.objects.all()
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.all(),
        "bids":bids
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    #log user out
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def active_listing(request,name):
    if request.method =="POST":
        form = Bidform(request.POST)
        if form.is_valid():
            listing = Listing.objects.get(pk=name)
            curr_bid = form.cleaned_data['new_bid']
            old_bid = Listing.objects.filter(id=name).values('first_bid')
            if old_bid[0]['first_bid']>= curr_bid:
                form = Bidform()
                listing = Listing.objects.get(pk=name)
                bids = Bid.objects.filter(pk__in=[name,0])
                message =f"bid have to be higher then old this {curr_bid} "
                return render(request,"auctions/listing.html",{
                    "listing":listing,
                    "bids":bids,
                    "form":form,
                    "message":message
        
                })
            else:
                Listing.objects.filter(id=name).update(first_bid=curr_bid)
                return HttpResponseRedirect(reverse("index"))

    else:
        #get all data base entries 
        old_bid = Listing.objects.filter(id=name).values('first_bid')
        form = Bidform()
        listing = Listing.objects.get(pk=name)
        bids = Bid.objects.filter(pk__in=[name,0])
        return render(request,"auctions/listing.html",{
            "listing":listing,
            "bids":bids,
            "form":form,
            "old_bid":old_bid[0]['first_bid']
        
    })

def create(request):
    if request.method =="POST":
        form = Createform(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            first_bid = form.cleaned_data['first_bid']
            Listing.objects.create(title=title,description=description,image=image,first_bid=first_bid)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = Createform()
        return render(request,"auctions/create.html",{
            "form":form
        })

