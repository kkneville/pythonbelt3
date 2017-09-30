from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from models import *
import random, re, datetime
from datetime import datetime, date
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt
from django.db import models
from ..login.models import Member



class TripManager(models.Manager):
    def validate_trip(self, formdata):
        errors = []

        if len(formdata['departure_date']) < 1 :
            errors.append("Departure date required.")  
        if len(formdata['return_date']) < 1 :
            errors.append("Return date required.")          
        if len(formdata['destination']) < 1 :
            errors.append("Destination is required.")    
        if len(formdata['description']) < 1 :
            errors.append("Description is required.")  
        return errors

    def validate_dates(self, formdata):
        errors = []
        departure_date = datetime.strptime(formdata['departure_date'],'%Y-%m-%d')
        return_date = datetime.strptime(formdata['return_date'], '%Y-%m-%d')    
        if departure_date < datetime.now() :
            errors.append("Departure dates must be in the future.")
        if return_date < departure_date:
            errors.append("Return date must be after departure date.")
        return errors        

    def create_trip(self, formdata, memberid):
        member = Member.objects.get(id=memberid)
        trip = self.create (
            destination = formdata['destination'],
            description = formdata['description'],
            departure_date = formdata['departure_date'],
            return_date = formdata['return_date'],
            planned_by = member,
        )
        return trip
      
class Trip(models.Model):
    destination = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    planned_by = models.ForeignKey(Member, related_name="planned_trips")
    joined_by = models.ManyToManyField(Member, related_name="joined_trips")
    departure_date = models.DateTimeField(default=datetime.now())
    return_date = models.DateTimeField(default=datetime.now())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()
