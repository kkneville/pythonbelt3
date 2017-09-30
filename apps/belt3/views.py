from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from models import *
import random, re, datetime
from datetime import datetime
from django.db import models
from ..login.models import Member


def current_member(request):
    id = request.session['id']
    member = Member.objects.get(id=id)
    return member

def logout(request):
    request.session.pop('id')
    return redirect(reverse('index'))

def dashboard(request):
    member = current_member(request)

    my_trips = list(Trip.objects.filter(planned_by__id=member.id))
    joined_trips = list(Trip.objects.filter(joined_by__id=member.id))
    my_trips.extend(joined_trips)
    
    other_trips = list(Trip.objects.exclude(planned_by__id=member.id).exclude(joined_by__id=member.id))
    context = {
    	"member": member,
        "my_trips": my_trips,
        "other_trips": other_trips,
    }
    return render(request, "belt3/dashboard.html", context)

def add(request):
    member = current_member(request)
    if "errors" in request.session :
        errors = request.session['errors']
        request.session.pop('errors')
    else:
        errors = []
    context = {
        "member": member,
        "errors": errors,
    }
    return render(request, "belt3/add.html", context)

def addtrip(request):
    member = current_member(request)
    memberid = member.id
    
    if request.method == "POST": 
        errors = Trip.objects.validate_trip(request.POST)
        if len(errors) > 0 :
            request.session['errors'] = errors
            return redirect(reverse("add"))
        else :
            errors = Trip.objects.validate_dates(request.POST)
            if len(errors) > 0 :
                request.session['errors'] = errors
                return redirect(reverse("add"))
            else :
                trip = Trip.objects.create_trip(request.POST, memberid)
                return redirect(reverse("dashboard"))        


# Please note: for simplicity due to time constraints I used a form post to pass values. In the assignment is doesn't specify how these method are to be accomplished so hopefully this is acceptable.

def showtrip(request):
    trip = Trip.objects.get(id=request.POST['id'])
    coming = trip.joined_by.all()
    context = {
		"trip": trip,
        "coming": coming,
	}
    return render(request, "belt3/showtrip.html", context)

def jointrip(request):
    member = current_member(request)
    trip = Trip.objects.get(id=request.POST['id'])
    trip.joined_by.add(member)
    trip.save()
    return redirect(reverse("dashboard")) 


