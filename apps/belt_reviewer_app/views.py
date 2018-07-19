#import needed django modules
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib import auth
from django.db import connection

#import bcrypt
import bcrypt

#  import our db(s)
from .models import *

#This is our index page and contains login and registration forms
def loginandreg(request):
    return render(request,'belt_reviewer_app/loginandreg.html')

#Processes information from the registration form
def process_register(request, methods=['POST']):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator(request.POST)
    # check if the errors object has anything in it
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
            print("WEVE HIT AN ERROR")
        # redirect the user back to the form to fix the errors
        return redirect('/', id)
    else:
        # if the errors object is empty, that means there were no errors!
        # add our new record to the table , push what we need to session,
        # and redirect to /success to render our final page
        User.objects.create(first_name=request.POST['input_first_name'], last_name=request.POST['input_last_name'], email=request.POST['input_email'], password=bcrypt.hashpw(request.POST['input_password'].encode('utf8'), bcrypt.gensalt()))
        query = User.objects.filter(email=request.POST['input_email']).values('id', 'email')
        for row in query:
            request.session['isloggedin'] = row['id']
            request.session['useremail'] = row['email']
        request.session['error'] = ""
        request.session['welcomename'] = request.POST['input_first_name']
        request.session['welcomemessage'] = 'Successfully registered!'
        return redirect('/books')

#Processes information from the login form
def process_login(request, methods=['POST']):
    # Query the data we need
    query = User.objects.all().values('id', 'email', 'first_name', 'password')
    # Iterate through query until we find user email then verify password is legit
    for row in query:
        if row['email'] == request.POST['login_email'] and bcrypt.checkpw(request.POST['login_password'].encode(), row['password'].encode()): 
            request.session['error'] = ""
            request.session['useremail'] = row['email']
            request.session['isloggedin'] =  row['id']
            request.session['welcomename'] = row['first_name']
            request.session['welcomemessage'] = 'Successfully logged in!'
            return redirect('/books')
    request.session['error'] = "• Try again"
    return redirect('/')

#This is the landing page that the user arrives at after registering or logging in
def books(request):
    # If the user has a isLoggedin session
    query = User.objects.filter(id=request.session['isloggedin']).values('id', 'email')
    if 'isloggedin' in request.session:
        for row in query:
            if request.session['isloggedin'] == row['id'] and request.session['useremail'] == row['email']:
                return render(request,'belt_reviewer_app/books.html')
    else:
        return redirect('/')

def addbook(request):
    print("IN ADDBOOK")
    return render(request, 'belt_reviewer_app/addbook.html')

def processbook(request, methods=['POST']):
    if request.POST['addauthor'] == "":
        author = request.POST['authorlist']
    else:
        author = request.POST['addauthor']
    Book.objects.create(title=request.POST['title'], author=author, review=request.POST['review'])
    id = request.session['isloggedin']
    review_id = Book.objects.latest(field_name='id')
    print("REVIEW ID ", review_id.id)
    print("ID: ", id)
    return redirect('/books')

# Clears out session / logs out the user
def logout(request):
    auth.logout(request)
    return redirect('/')