# Filename:     views.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last updated: 16/01/2020
# Description:  Contains the views for the website.

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils.translation import gettext as _
from django.views import View, generic 

from tellings.forms import *
from tellings.page_extras import random_quotes

import random
from datetime import datetime, date, timedelta, timezone

# #########################################################################################
# SHARED FUNCTIONS ------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

def get_random_quote():
    """ Used to get a random quote from the random_quotes list.
       
    :returns: A random quote from the random_quotes list.
    """
    secure_random = random.SystemRandom()
    random_quote = secure_random.choice(random_quotes)
    return _(random_quote)

def user_has_posted_today(request):
    """ Used to determine if the user has posted an update today.
    
    :param request: A dictionary-like object containing the HTTP POST parameters, 
                    sent by a site user.     
    :returns: True if the user has posted an update today,
              otherwise false.
    """
    current_userID = request.user.id
    yesterday = date.today() - timedelta(1)
    return UserPost.objects.filter(user=current_userID).filter(dateOfPost__gt=yesterday).exists()

def user_login(request):
    """ Handles user authentication.

    :param request: A dictionary-like object containing all HTTP POST parameters, 
                    sent by a site user. 
    :returns: A redirect to a HTML page.
    """
    username = request.POST['username']
    password = request.POST['pwd']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/loginpage/')


# #########################################################################################
# PAGE VIEWS ------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

class ChangeUserDetailsPage(LoginRequiredMixin, View):
    """ Creates the change user details page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Change User Details page.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """  
        quote = get_random_quote()
        form = ChangeUserDetailsForm(instance=request.user)
        return render(request, 'tellings/changeUserDetails.html', {'form': form, 'quote': quote})

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
            messages.error(request, _('Please correct the error below.'))
            return render(request, 'tellings/changeUserDetails.html', {'form': form, 'quote': quote})

    def changeDetails(self, request, form):
        """ Handles changing the user's details.

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
                      {'message': _('Your details have been updated'), 'form': form, 'quote': quote})


class ChangePasswordPage(LoginRequiredMixin, View):
    """ Creates the change password page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Change Password page.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        quote = get_random_quote()
        form = PasswordChangeForm(request.user)
        return render(request, 'tellings/changePassword.html', {'form': form, 'quote': quote})

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
                      {'message': _('Your password was successfully updated!'), 'form': form, 'quote': quote})


class SignUpPage(View):
    """ Creates the sign up page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Sign Up page.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        quote = get_random_quote()
        form = NewUserCreationForm()
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
            return user_login(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def signUp(self, request):
        """ Handles account creation.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            quote = get_random_quote()
            messages.error(request, _('Please correct the error below.'))
            return render(request, 'tellings/signup.html', {'form': form, 'quote': quote})


class IndexPage(View):
    """ Creates the home page for the website."""
    http_method_names = ['get', 'post']

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
            return user_login(request)
        else:
            quote = get_random_quote()
            return render(request, 'tellings/index.html', {'quote': quote})


class ErrorPage(View):
    """ Creates the Error page for the website."""
    http_method_names = ['get', 'post']

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
            return user_login(request)
        else:
            quote = get_random_quote()
            return render(request, 'tellings/errorPage.html', {'quote': quote})


class AccountDeletedPage(LoginRequiredMixin, View):
    """ Creates the Account Deleted page for the website. """
    http_method_names = ['post']

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
        """ Handles deleting the user's account.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        try:
            quote = get_random_quote()
            u = request.user

            # Create a DeletedAccount record
            deleted_date = datetime.now(timezone.utc)
            date_joined = u.date_joined
            membership_length = deleted_date - date_joined

            data = {
                'deleted_reason': request.POST.get('reason', 'mydefaultvalue'),
                'deleted_date': deleted_date,
                'membership_length': membership_length.days,
            }

            form = DeleteAccountForm(data)

            if form.is_valid():
                form.save()

            # Logout and delete the user's account
            logout(request)
            u.delete()
            return render(request, 'tellings/accountDeleted.html', {'quote': quote})
        except:
            return HttpResponseRedirect('/errorpage/')


class TagListView(LoginRequiredMixin, generic.ListView):
    """ Creates the Tags page for the website."""
    model = Tag
    paginate_by = 20
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)  
        quote = get_random_quote()
        context['quote'] = quote
        return context


class MyUpdatesListView(LoginRequiredMixin, generic.ListView):
    """ Creates the My Updates page for the website."""
    model = UserPost
    template_name = "tellings/myupdates_list.html"
    paginate_by = 10
    http_method_names = ['get', 'post']

    def get_queryset(self):
        user_id = self.request.user.id
        tagName_val = False
        qs = super().get_queryset()
        
        if self.request.method == 'GET' and 'tagName' in self.request.GET:
            tagName_val = self.request.GET.get('tagName', False)
                
        if tagName_val:  # get posts for current user filtered by tagname
            try:
                tagID = Tag.objects.get(tagName=tagName_val).tagID
                tagmaps = Tagmap.objects.filter(tagID=tagID)
                postList = [tm.postID.postID for tm in tagmaps]
                qs = qs.filter(postID__in=postList).filter(user=user_id).order_by('-dateOfPost') 
            except:
                # If the user tries to search for a non existing tag, return all posts instead
                qs = qs.filter(user=user_id).order_by('-dateOfPost')
        else:            # get all posts for current user
            qs = qs.filter(user=user_id).order_by('-dateOfPost')

        return qs

    def get_context_data(self, **kwargs):
        context = super(MyUpdatesListView, self).get_context_data(**kwargs)  
        current_username = user_id = self.request.user.username
        quote = get_random_quote()

        if self.request.method == 'GET' and 'tagName' in self.request.GET:
            context['tagName'] = self.request.GET.get('tagName', '')

        context['current_username'] = current_username
        context['quote'] = quote
        return context


class NewUpdatesListView(LoginRequiredMixin, generic.ListView):
    """ Creates the New Updates page for the website."""
    model = UserPost
    template_name = "tellings/newupdates_list.html"
    paginate_by = 10
    http_method_names = ['get', 'post']

    def get_queryset(self):
        tagName_val = False
        username_val = False

        if self.request.method == 'GET':
            if 'tagName' in self.request.GET:
                tagName_val = self.request.GET.get('tagName', False) 
            if 'userName' in self.request.GET:
                username_val = self.request.GET.get('userName', False)
                user_id = User.objects.get(username=username_val).id
                
        if tagName_val:  # get posts for current user filtered by tagname
            tagID = Tag.objects.get(tagName=tagName_val).tagID
            tagmaps = Tagmap.objects.filter(tagID=tagID)
            postList = [tm.postID.postID for tm in tagmaps]        
        
            if username_val:
                new_context = UserPost.objects.filter(postID__in=postList).filter(user=user_id).order_by('-dateOfPost') 
            else:
                new_context = UserPost.objects.filter(postID__in=postList).order_by('-dateOfPost') 
        elif username_val:
            new_context = UserPost.objects.filter(user=user_id).order_by('-dateOfPost') 
        else:            # get all posts
            new_context = UserPost.objects.all().order_by('-dateOfPost')
        
        return new_context

    def get_context_data(self, **kwargs):
        context = super(NewUpdatesListView, self).get_context_data(**kwargs)  
        current_username = self.request.user.username
        quote = get_random_quote()

        if self.request.method == 'GET':
            if 'tagName' in self.request.GET:
                context['tagName'] = self.request.GET.get('tagName', '')
            if 'userName' in self.request.GET:
                context['userName'] = self.request.GET.get('userName', '')

        context['current_username'] = current_username
        context['quote'] = quote
        return context



# #########################################################################################
# AJAX HANDLERS ---------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

class HasPostedToday(LoginRequiredMixin, View):
    """ An AJAX handler used to check whether the currently logged in
        user has posted an update today or not."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the user has already posted an update today,
                  otherwise 'False'.
        """
        if user_has_posted_today(request):
            return HttpResponse('True')
        else:
            return HttpResponse('False')

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        if user_has_posted_today(request):
            return HttpResponse('True')
        else:
            return HttpResponse('False')


class TitleExists(LoginRequiredMixin, View):
    """ An AJAX handler used to check if a post title already
        exists within the UserPost table or not."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the title already exists in the UserPost table,
                  otherwise 'False'.
        """
        if ('title' in request.POST):
            return self.titleExists(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def titleExists(self, request):
        """ Checks whether an update title already exists within the UserPost table or not.
            This function can only be used by authenticated users.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the title already exists in the UserPost table,
                  otherwise 'False'.
        """
        in_postTitle = request.POST['title']

        if UserPost.objects.filter(postTitle=in_postTitle).exists():
            return HttpResponse('True')
        else:
            return HttpResponse('False')


class AddNewUpdate(LoginRequiredMixin, View):
    """ An AJAX handler used to add a new user update to the database."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the title already exists in the UserPost table,
                  otherwise a redirect to the error page.
        """
        if user_has_posted_today(request):
            return HttpResponseRedirect('/errorpage/')

        if ('postTitle' in request.POST) and ('postText' in request.POST) and ('postTags' in request.POST): 
            # make a copy of POST to add user to as this is not supplied by the form       
            request.POST = request.POST.copy()
            request.POST['user'] = request.user.id
            request.POST['dateOfPost'] = date.today()

            form = UserPostForm(request.POST)
            if form.is_valid():
                userpost = form.save()
                return HttpResponse('True')
            else:
                return HttpResponseRedirect('/errorpage/')
        else:
            return HttpResponseRedirect('/errorpage/')
    
        
class CheckUserPassword(LoginRequiredMixin, View):
    """ An AJAX handler used to check a user's password.
        Used by the Delete Account modal. """

    http_method_names = ['post']

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


class DeleteUserPost(LoginRequiredMixin, View):
    """ An AJAX handler used to delete posts for the current user.
    """
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the password is valid, otherwise 'False'.
        """
        if ('postID' in request.POST):
            postID = request.POST.get('postID')
            username = self.getUsernameForPostID(postID)
            # Check that the post was made by the user deleting it
            if( username == request.user.username ):
                if self.deletePost(postID):
                    return HttpResponse("True")
                else:
                    return HttpResponse(_("Something went wrong. We were unable to delete your post."))
            else:
                return HttpResponse(_("YOU CANNOT DELETE OTHER USERS POSTS!!!"))
        else:
            return HttpResponseRedirect('/errorpage/')

    def getUsernameForPostID(self, in_postID):
        """ Returns the name of the user who made the post.
        """
        try:
            post = UserPost.objects.get(postID=in_postID)
            username = post.user.username
            return username
        except:
            return None

    def deletePost(self, in_postID):
        """ Handles deleting a userPost.
        """
        try:
            post = UserPost.objects.get(postID=in_postID)
            post.delete()
            return True
        except:
            return False


class LoginModal(View):
    """ An AJAX handler used to add the login modal to pages.
    """
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/includes/login_modal.html')

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/includes/login_modal.html')


class DeleteAccountModal(LoginRequiredMixin, View):
    """ An AJAX handler used to add the delete account modal to pages.
    """
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/includes/deleteAccount_modal.html')

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/includes/deleteAccount_modal.html')


class AddUpdateModal(LoginRequiredMixin, View):
    """ An AJAX handler used to add the login modal to pages.
    """
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        # Ensure that the user has not posted today
        if user_has_posted_today(request):
            return HttpResponse('False')

        return render(request, 'tellings/includes/addUpdate_modal.html')

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters, 
                        sent by a site user. 
        :returns: A HTML page.
        """
        # Ensure that the user has not posted today
        current_user_id = request.user.id
        if user_has_posted_today(request):
            return HttpResponse('False')

        return render(request, 'tellings/includes/addUpdate_modal.html')
        

class EditUserPost(LoginRequiredMixin, generic.UpdateView):
    """ An AJAX handler used to add the edit user post HTML to pages,
        and deal with updating the user post with the new details.
    """
    model = UserPost 
    template_name = "tellings/includes/editPost.html"    
    fields = ['user', 'dateOfPost','postTitle', 'postText']   
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk']=self.object.postID
        return context

    def post(self, request):
        """ Handles POST requests.
   
        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the post could be edited, otherwise an error message.
        """
        if ('postID' in request.POST and 'postText' in request.POST):
            return self.updateUserPostRecord(request)
        else:
            return HttpResponseRedirect('/errorpage/')
                
    def updateUserPostRecord(self, request):
        """ Updates a UserPost record.
           
        :param request: A dictionary-like object containing all HTTP parameters, 
                        sent by a site user. 
        :returns: A string 'True' if the post could be edited, otherwise an error message.
        """
        in_postID = request.POST.get('postID')
        in_postText = request.POST.get('postText')
        userPost = get_object_or_404(UserPost, postID=in_postID)

        if(userPost.user.username == request.user.username):
            try:
                # Update the record (sql injection-safely)
                UserPost.objects.filter(postID=in_postID).update(postText=in_postText)
                return HttpResponse("True")
            except:
                return HttpResponse(_("Unable to make changes to the post. Please contact the site administrator."))
        else:
            return HttpResponse(_("YOU CANNOT EDIT OTHER USERS POSTS!!!"))   
