from __future__ import unicode_literals
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import random, re
import bcrypt
import datetime


class MemberManager(models.Manager):
    def validate_reg(self, formdata):
        errors = []
        if len(formdata['firstname']) < 3 :
            errors.append("First name is required.")
        if len(formdata['username']) < 3 :
            errors.append("Username is required.")
        if len(formdata['password'])  < 8 :
            errors.append("Passwords must be at least 8 characters long.")
        if formdata['password'] != formdata['passwordconfirm'] :
            errors.append("Passwords must match.")
        return errors

    def validate_login(self, formdata):
        errors = []
        if len(formdata["username"]) < 1 :
            errors.append("Username is required.")
        if len(formdata['password']) < 1 :
            errors.append("Password is required.")
        member = Member.objects.filter(username=formdata['username']).first()
        if member:
            if not bcrypt.checkpw(formdata['password'].encode(), member.password.encode()) :
                errors.append("Username and password do not match.")
        else :
            errors.append("Username and password do not match.")
        result = {
            "errors": errors,
            "member": member,
        }
        return result

    def create_member(self, formdata):
        password = str(formdata['password'])
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        member = self.create (
            firstname = formdata['firstname'],
            username = formdata['username'],
            password = hashedpw,
        )
        return member


class Member(models.Model):
    firstname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MemberManager()
