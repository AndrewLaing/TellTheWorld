# Filename:     views.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last updated: 05/09/2019
# Description:  Contains the views for the website.

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required # @login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views import View

import tellings.createTagLinksHTML as CTH
import tellings.createUpdatesHTML as CUH
import tellings.databaseQueries as DBQ
from tellings.forms import ChangeUserDetailsForm
from tellings.models import Posts, Tags, Tagmap

from tellings.page_extras import random_quotes
import random

# #########################################################################################
# SHARED FUNCTIONS ------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

def get_random_quote():
    secure_random = random.SystemRandom()
    return secure_random.choice(random_quotes)


# #########################################################################################
# PAGE VIEWS ------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

class ChangeUserDetailsPage(View):
    """ Creates the change password page for the website."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests for the Change User Details page.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        
        quote = get_random_quote()
        form = ChangeUserDetailsForm(instance=request.user)
        return render(request, 'tellings/changeUserDetails.html', {'form': form, 'quote': quote})

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests for the Change User Details page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        form = ChangeUserDetailsForm(request.POST)
        if form.is_valid():
            return self.changeDetails(request, form)
        else:
            quote = get_random_quote()
            messages.error(request, 'Please correct the error below.')
            return render(request, 'tellings/changeUserDetails.html', {'form': form, 'quote': quote})

    def changeDetails(self, request, form):
        """ Handles changing the users details.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        u = request.user
        u.first_name = request.POST['first_name']
        u.last_name = request.POST['last_name']
        u.email = request.POST['email']
        u.save()
        quote = get_random_quote()
        return render(request, 'tellings/changeUserDetails.html', 
                                {'message':'Your details have been updated', 'form': form, 'quote': quote})


class ChangePasswordPage(View):
    """ Creates the change password page for the website."""
    
    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests for the Change Password page.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        quote = get_random_quote()
        form = PasswordChangeForm(request.user)
        return render(request, 'tellings/changePassword.html', {'form': form, 'quote': quote})

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests for the Change Password page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            return self.changePassword(request, form)
        else:
            quote = get_random_quote()
            return render(request, 'tellings/changePassword.html', {'form': form, 'quote': quote})

    def changePassword(self, request, form):
        """ Handles changing the user's password.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user.
        :param form: A Django form object.
        :returns: A HTML page.
        """
        form.save()
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        quote = get_random_quote()
        return render(request, 'tellings/changePassword.html', 
                      {'message':'Your password was successfully updated!', 'form': form, 'quote': quote})


class SignUpPage(View):
    """ Creates the sign up page for the website."""

    def get(self, request):
        """ Handles GET requests for the Sign Up page.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        quote = get_random_quote()
        form = UserCreationForm()
        return render(request, 'tellings/signup.html', {'form': form, 'quote': quote})

    def post(self, request):
        """ Handles POST requests for the Sign Up page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('password1' in request.POST):
            return self.signUp(request)
        elif ('username' in request.POST) and ('pwd' in request.POST):
            return self.login(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def signUp(self, request):
        """ Handles account creation.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            quote = get_random_quote()
            return render(request, 'tellings/index.html', {'quote': quote})
        else:
            quote = get_random_quote()
            messages.error(request, 'Please correct the error below.')
            return render(request, 'tellings/signup.html', {'form': form, 'quote': quote})

    def login(self, request):
        """ Handles user authentication.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        username = request.POST['username']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/loginpage/')


class IndexPage(View):
    """ Creates the home page for the website."""

    def get(self, request):
        """ Handles GET requests for the home page.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        quote = get_random_quote()
        return render(request, 'tellings/index.html', {'quote': quote})

    def post(self, request):
        """ Handles POST requests for the home page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return self.login(request)
        else:
            quote = get_random_quote()
            return render(request, 'tellings/index.html', {'quote': quote})

    def login(self, request):
        """ Handles user authentication.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        username = request.POST['username']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'tellings/index.html')
        else:
            return HttpResponseRedirect('/loginpage/')


class NewUpdatesPage(View):
    """ Creates the New Updates page for the website."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests for the New Updates page.
            This page's inner contents will only be visible to authenticated users.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return self.newUpdatesPage(request)

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests for the New Updates page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return self.newUpdatesPage(request)

    def newUpdatesPage(self, request):
        """ Creates and returns the New Updates page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        quote = get_random_quote()
        postDetails = DBQ.getAllPostDetails()
        username = request.user.username
        contents = CUH.createInnerHTML(postDetails, username)

        return render(request, 'tellings/newupdates.html', {'contents': contents, 'quote': quote})


class TagsPage(View):
    """ Creates the Tags page for the website."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests for the Tags page.
            This page's inner contents will only be visible to authenticated users.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return self.tagsPage(request)

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests for the Tags page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return self.login(request)
        else:
            return self.tagsPage(request)

    def login(self, request):
        """ Handles user authentication.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        username = request.POST['username']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/loginpage/')

    def tagsPage(self, request):
        """ Creates and returns the Tags page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        quote = get_random_quote()
        tagNames = DBQ.getAllTagNames()
        contents = CTH.createInnerHTML(tagNames)
        return render(request, 'tellings/tags.html', {'contents': contents, 'quote': quote})


class MyUpdatesPage(View):
    """ Creates the New Updates page for the website."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests for the My Updates page.
            This page's inner contents will only be visible to authenticated users.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return self.myUpdatesPage(request)

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests for the My Updates page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return self.myUpdatesPage(request)

    def myUpdatesPage(self, request):
        """ Creates and returns the My Updates page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        quote = get_random_quote()
        current_user_id = request.user.id
        postDetails = DBQ.getAllPostsByUserID(current_user_id)
        username = request.user.username
        contents = CUH.createInnerHTML(postDetails, username)
        return render(request, 'tellings/myupdates.html', {'contents': contents, 'quote': quote})


class ErrorPage(View):
    """ Creates the New Updates page for the website."""

    def get(self, request):
        """ Handles GET requests for the Error page.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        quote = get_random_quote()
        return render(request, 'tellings/errorPage.html', {'quote': quote})

    def post(self, request):
        """ Handles POST requests for the Error page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return self.login(request)
        else:
            quote = get_random_quote()
            return render(request, 'tellings/errorPage.html', {'quote': quote})

    def login(self, request):
        """ Handles user authentication.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        username = request.POST['username']
        password = request.POST['pwd']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/loginpage/')


class AccountDeletedPage(View):
    """ Creates the Account Deleted page for the website."""
    
    def get(self, request):
        """ Handles GET requests for the Error page.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return HttpResponseRedirect('/')

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests for the Error page.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        if ('reason' in request.POST):
            return self.deleteAccount(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def deleteAccount(self, request):
        """ Handles user authentication.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        try:
            quote = get_random_quote()
            u = request.user;
            logout(request);
            u.delete();
            return render(request, 'tellings/accountDeleted.html', {'quote': quote})
        except:
            return HttpResponseRedirect('/errorpage/')


# #########################################################################################
# AJAX HANDLERS ---------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

class HasPostedToday(View):
    """ An AJAX handler used to check whether the currently logged in
        user has posted an update today or not."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the user has already posted an update today,
                  otherwise 'False'.
        """
        return self.userHasPostedToday(request)

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return self.userHasPostedToday(request)

    def userHasPostedToday(self, request):
        """ Checks whether the currently logged in user has posted an update today or not.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the user has already posted an update today,
                  otherwise 'False'.
        """
        current_user_id = request.user.id
        if DBQ.userHasPostedToday(current_user_id):
            return HttpResponse('True')
        else:
            return HttpResponse('False')


class TitleExists(View):
    """ An AJAX handler used to check whether an update title already
        exists within the Posts table or not."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return HttpResponseRedirect('/errorpage/')

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the title already exists in the Posts table,
                  otherwise 'False'.
        """
        if ('title' in request.POST):
            return self.titleExists(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def titleExists(self, request):
        """ Checks whether an update title already exists within the Posts table or not.
            This function can only be used by authenticated users.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the title already exists in the Posts table,
                  otherwise 'False'.
        """
        postTitle = request.POST['title']

        if DBQ.postTitleExists(postTitle):
            return HttpResponse('True')
        else:
            return HttpResponse('False')


class AddNewUpdate(View):
    """ An AJAX handler used to add a new user update to the database."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return HttpResponseRedirect('/errorpage/')

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the title already exists in the Posts table,
                  otherwise 'False'.
        """
        if ('postTitle' in request.POST) and ('postText' in request.POST) and ('postTags' in request.POST):
            return self.addNewUpdate(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def addNewUpdate(self, request):
        """ Adds a new update to the database.
            This function can only be used by authenticated users.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the title already exists in the Posts table,
                  otherwise 'False'.
        """
        current_user_id = request.user.id
        postTitle = request.POST['postTitle']

        # Validate user input again because data can be modified before posting
        if DBQ.postTitleExists(postTitle):
            return HttpResponseRedirect('/errorpage/')

        if DBQ.userHasPostedToday(current_user_id):
            return HttpResponseRedirect('/errorpage/')

        DBQ.addNewPostUpdateRecords(request)

        return HttpResponse('True')
    

class AddUpdatesForTag(View):
    """ An AJAX handler used to add all updates filtered by tag to the contents of a page
        when a tag link is clicked within a user update panel."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return HttpResponseRedirect('/errorpage/')

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A string containing HTML.
        """
        if ('postTag' in request.POST):
            return self.addUpdates(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def addUpdates(self, request):
        """ Used to create inner HTML of updates filtered by tag.
            Any other POST requests will result in an error page being shown.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A string containing HTML.
        """
        tagName = request.POST['postTag']
        postDetails = DBQ.getAllPostsByTagname(tagName)
        username = request.user.username
        contents = CUH.createInnerHTML(postDetails, username)

        return HttpResponse(contents)
        

class AddUpdatesForTagByLoggedInUser(View):
    """ An AJAX handler used to add updates filtered by tag to the contents of a page for
        the currently logged in user when a tag link is clicked within a user update panel."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return HttpResponseRedirect('/errorpage/')

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A string containing HTML.
        """
        if ('postTag' in request.POST):
            return self.addUpdates(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def addUpdates(self, request):
        """ Used to create inner HTML of updates filtered by tag for the
            currently logged in user.
            Any other POST requests will result in an error page being shown.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A string containing HTML.
        """
        tagName = request.POST['postTag']
        current_user_id = request.user.id
        postDetails = DBQ.getAllPostsByTagnameForUserID(tagName, current_user_id)
        username = request.user.username
        contents = CUH.createInnerHTML(postDetails, username)

        return HttpResponse(contents)


class AddUpdatesForUsername(View):
    """ An AJAX handler used to add updates filtered by username to the contents of a page for
        when a username link is clicked within a user update panel."""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return HttpResponseRedirect('/errorpage/')

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A string containing HTML.
        """
        if ('username' in request.POST):
            return self.addUpdates(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def addUpdates(self, request):
        """ Used to create inner HTML of updates filtered by username.
            Any other POST requests will result in an error page being shown.
            This function can only be used by authenticated users.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A string containing HTML.
        """
        uname = request.POST['username']
            
        try:
            userID = User.objects.get(username=uname).id
            postDetails = DBQ.getAllPostsByUserID(userID)
            username = request.user.username
            contents = CUH.createInnerHTML(postDetails, username)
        except User.DoesNotExist:
            contents = CUH.createNoResultsHTML()

        return HttpResponse(contents)


class CheckUserPassword(View):
    """ An AJAX handler used to check a user's password.
        Used in the Delete Account modal"""

    @method_decorator(login_required)
    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return HttpResponseRedirect('/errorpage/')

    @method_decorator(login_required)
    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the password is valid, otherwise 'False'.
        """
        if ('pwd' in request.POST):
            return self.isValidPassword(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def isValidPassword(self, request):
        """ Checks whether the user has entered their password correctly.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the password is valid, otherwise 'False'.
        """
        current_password = request.user.password #user's password
        entered_password = request.POST['pwd']   #posted password
  
        passwords_match = check_password(entered_password, current_password)
        
        if passwords_match:
            return HttpResponse('True')
        else:
            return HttpResponse('False')