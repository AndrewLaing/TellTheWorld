# Filename:     views.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last updated: 15/03/2020
# Description:  Contains the views for the website.

import django.utils.timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.views import View, generic 

from tellings.forms import *
from tellings.page_extras import banned_words

from datetime import timedelta, timezone
import enum

# #########################################################################################
# SHARED ENUMS, FUNCTIONS AND VARIABLES ---------------------------------------------------
# -----------------------------------------------------------------------------------------

class StatusCode(enum.Enum):
    """ Enum containing the status codes returned in the response dictionaries"""
    ERROR = 0
    SUCCESS = 1
    CENSORED = 2
    INVALIDPASSWORD = 3


adminNameList = ['admin']
maxPostsPerDay = 4

def contains_banned_word(text):
    """ Tests if a text contains a banned word.
    
    :param text: A string to test for banned words.
    :returns: True if the text contains a banned word, otherwise false.
    """
    text = text.lower()
    for banned_word in banned_words:
        if banned_word in text:
            return True
    return False


def has_exceeded_max_posts(request): 
    """ Used to determine if the user has exceeded the max number of allowed posts.
    
    :param request: A dictionary-like object containing the HTTP POST parameters, 
                    sent by a site visitor. Note that admins can make as many posts
                    as they need to!
    :returns: True if the user has exceeded the max number of allowed posts, otherwise false.
    """
    if request.user.username in adminNameList:
        return False

    current_userID = request.user.id
    startofday = django.utils.timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) 
    startofday = startofday.replace(tzinfo=timezone.utc)

    numberOfPostsToday = UserPost.objects.filter(user=current_userID, dateOfPost__gt=startofday).count()

    return numberOfPostsToday >= maxPostsPerDay

def user_login(request):
    """ Handles user authentication.

    :param request: A dictionary-like object containing all HTTP POST parameters 
                    sent by a site visitor. 
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

class AboutPage(View):
    """ Creates the About us page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the About us page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/about.html')

    def post(self, request):
        """ Handles POST requests for the About us page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return user_login(request)
        else:
            return render(request, 'tellings/about.html')


class AcceptableUsagePage(View):
    """ Creates the Acceptable Usage Policy page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Acceptable Usage Policy page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/acceptableusage.html')

    def post(self, request):
        """ Handles POST requests for the Acceptable Usage Policy page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return user_login(request)
        else:
            return render(request, 'tellings/acceptableusage.html')


class AccountDeletedPage(LoginRequiredMixin, View):
    """ Creates the Account Deleted page for the website, and handles user account deletion """
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests for the Error page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if ('reason' in request.POST):
            return self.deleteAccount(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def deleteAccount(self, request):
        """ Handles deleting the user's account.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page if the account was deleted, otherwise
                  a redirect to the error page.
        """
        current_user = request.user
        now = django.utils.timezone.now()
        now = now.replace(tzinfo=timezone.utc)
        deleted_date = now
        date_joined = current_user.date_joined
        membership_length = deleted_date - date_joined

        data = {
            'deleted_reason': request.POST.get('reason', 'noreasongiven'),
            'deleted_date': deleted_date,
            'membership_length': membership_length.days,
        }

        form = DeleteAccountForm(data)

        if form.is_valid():
            form.save()
            logout(request)
            current_user.delete()
            return render(request, 'tellings/accountDeleted.html')            
        else:
            return HttpResponseRedirect('/errorpage/')


class BlockedUserListView(LoginRequiredMixin, generic.ListView):
    """ Creates the BlockedUser page for the website."""
    model = BlockedUser
    template_name = "tellings/blockeduser_list.html"
    paginate_by = 20
    http_method_names = ['get']
 
    def get_queryset(self):
      current_user = self.request.user
      return BlockedUser.objects.filter(blockedBy=current_user).order_by('blockedUser__username')


class ChangePasswordPage(LoginRequiredMixin, View):
    """ Creates the change password page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Change Password page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        form = PasswordChangeForm(request.user)
        return render(request, 'tellings/changePassword.html', {'form': form})

    def post(self, request):
        """ Handles POST requests for the Change Password page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if 'old_password' in self.request.POST and 'new_password1' in self.request.POST:
            return self.changePassword(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def changePassword(self, request):
        """ Handles changing the user's password.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor.
        :param form: A Django form object.
        :returns: A HTML page.
        """
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return render(request, 'tellings/changePassword.html', 
                        {'message': _('Your password was successfully updated!'), 'form': form})
        else:
            return render(request, 'tellings/changePassword.html', {'form': form})


class ChangeUserDetailsPage(LoginRequiredMixin, View):
    """ Creates the change user details page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Change User Details page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """  
        form = ChangeUserDetailsForm(instance=request.user)
        return render(request, 'tellings/changeUserDetails.html', {'form': form})

    def post(self, request):
        """ Handles POST requests for the Change User Details page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        required_fields = ['first_name', 'last_name', 'email']

        for field in required_fields:
            if field not in self.request.POST:
                return HttpResponseRedirect('/errorpage/')

        return self.changeDetails(request)


    def changeDetails(self, request):
        """ Handles changing the user's details.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor.  
        :returns: A HTML page.
        """
        form = ChangeUserDetailsForm(request.POST)

        if form.is_valid():
            current_user = request.user
            current_user.first_name = request.POST['first_name']
            current_user.last_name = request.POST['last_name']
            current_user.email = request.POST['email']
            current_user.save()
            return render(request, 'tellings/changeUserDetails.html', 
                        {'message': _('Your details have been updated'), 'form': form})
        else:
            messages.error(request, _('Please correct the errors below.'))
            return render(request, 'tellings/changeUserDetails.html', {'form': form})


class HiddenPostListView(LoginRequiredMixin, generic.ListView):
    """ Creates the HiddenPost page for the website.
        Note: Posts by blocked users, or by users who have blocked the
              currently logged in user will be excluded.
    """
    model = HiddenPost
    template_name = "tellings/hiddenpost_list.html"
    paginate_by = 20
    http_method_names = ['get']

    def get_queryset(self):
      current_user = self.request.user
      blockedPosts = self.get_blockedPosts_list()  

      if self.request.method == 'GET' and 'username' in self.request.GET:
          username_val = self.request.GET.get('username')
          userToBlock = get_object_or_404(User, username=username_val)
          return HiddenPost.objects.filter(postID__user=userToBlock, hideFrom=current_user).exclude(postID__in=blockedPosts).order_by('-postID__dateOfPost')
      else:
          return HiddenPost.objects.filter(hideFrom=current_user).exclude(postID__in=blockedPosts).order_by('-postID__dateOfPost')

    def blockedUsers(self):
        """ Returns a list of the users blocked by the currently loggedin user. 

            :returns: A list of User objects.   
        """
        current_user = self.request.user
        blockedUsers = BlockedUser.objects.filter(blockedBy=current_user)
        return [blocked.blockedUser for blocked in blockedUsers]   

    def hiddenUsers(self):
        """ Returns a list of the users blocked by the currently loggedin user. 

            :returns: A list of User objects.   
        """
        current_user = self.request.user
        hiddenUsers = HiddenUser.objects.filter(hiddenBy=current_user)
        return [hidden.hiddenUser for hidden in hiddenUsers]   

    def userBlockedBy(self):
        """ Returns a list of the users who have blocked the currently loggedin user. 

            :returns: A list of User objects.   
        """
        current_user = self.request.user
        blockedBy = BlockedUser.objects.filter(blockedUser=current_user)
        return [blocked.blockedBy for blocked in blockedBy]   

    def get_blockedPosts_list(self):
        """ Returns a list of all UserPosts from users 
            blocked by the currently logged in user, and posts by users who
            have blocked the logged in user.

            :returns: A list of UserPosts.
        """
        blockedUsers = self.blockedUsers()
        blockedBy = self.userBlockedBy()
        blockedList = list(set().union(blockedUsers, blockedBy)) 
        blockedPosts = []
        
        if blockedList:
            posts =  UserPost.objects.filter(user__in=blockedList)
            blockedPosts = [post for post in posts]

        return blockedPosts


class IndexPage(View):
    """ Creates the home page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the home page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/index.html')

    def post(self, request):
        """ Handles POST requests for the home page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return user_login(request)
        else:
            return render(request, 'tellings/index.html')


class ErrorPage(View):
    """ Creates the Error page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Error page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/errorPage.html')

    def post(self, request):
        """ Handles POST requests for the Error page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return user_login(request)
        else:
            return render(request, 'tellings/errorPage.html')


class MissionStatementPage(View):
    """ Creates the Mission Statement page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the About us page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/missionstatement.html')

    def post(self, request):
        """ Handles POST requests for the Mission Statement page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return user_login(request)
        else:
            return render(request, 'tellings/missionstatement.html')


class MyUpdatesListView(LoginRequiredMixin, generic.ListView):
    """ Creates the My Updates page for the website."""
    model = UserPost
    template_name = "tellings/myupdates_list.html"
    paginate_by = 10
    http_method_names = ['get']

    def get_queryset(self):
        """ Returns a queryset. This will be filtered if the user passes either a tagName
            or a username. Note that if the user tries to pass a value not in the database, then
            an unfiltered set will be returned instead.

            :returns: A queryset of the currently logged in user's UserPosts.
        """
        user_id = self.request.user.id
        tagName_val = False
        qs = super().get_queryset()
        
        if 'tagName' in self.request.GET:
            tagName_val = self.request.GET.get('tagName')

            # If the user tries to search for a non existing tag, return all posts instead
            if not Tag.objects.filter(tagName=tagName_val).exists():
                return qs.filter(user=user_id).order_by('-dateOfPost')

        if tagName_val:
            tag = Tag.objects.get(tagName=tagName_val)
            tagmaps = Tagmap.objects.filter(tagID=tag)
            postList = [tm.postID.postID for tm in tagmaps]
            qs = qs.filter(postID__in=postList, user=user_id).order_by('-dateOfPost') 
        else:
            qs = qs.filter(user=user_id).order_by('-dateOfPost')

        return qs

    def get_context_data(self, **kwargs):
        context = super(MyUpdatesListView, self).get_context_data(**kwargs)  
        current_username = user_id = self.request.user.username

        if 'tagName' in self.request.GET:
            context['tagName'] = self.request.GET.get('tagName')

        context['current_username'] = current_username
        return context


class NewUpdatesListView(LoginRequiredMixin, generic.ListView):
    """ Creates the New Updates page for the website."""
    model = UserPost
    template_name = "tellings/newupdates_list.html"
    paginate_by = 10
    http_method_names = ['get']

    def blockedUsers(self):
        """ Returns a list of the users blocked by the currently loggedin user. 

            :returns: A list of User objects.   
        """
        current_user = self.request.user
        blockedUsers = BlockedUser.objects.filter(blockedBy=current_user)
        return [blocked.blockedUser for blocked in blockedUsers]   

    def userBlockedBy(self):
        """ Returns a list of the users who have blocked the currently loggedin user. 

            :returns: A list of User objects.   
        """
        current_user = self.request.user
        blockedBy = BlockedUser.objects.filter(blockedUser=current_user)
        return [blocked.blockedBy for blocked in blockedBy]   

    def hiddenPosts(self):
        current_user = self.request.user
        hiddenPosts = HiddenPost.objects.filter(hideFrom=current_user)
        return [hidden.postID.postID for hidden in hiddenPosts]   

    def posts_filtered_by_blocked(self):
        """ Returns a queryset of all UserPosts excluding those from users 
            blocked by the currently logged in user, and posts by users who
            have blocked the logged in user.

            :returns: A filtered queryset of UserPosts.
        """
        blockedUsers = self.blockedUsers()
        blockedBy = self.userBlockedBy()
        blockedList = list(set().union(blockedUsers, blockedBy))

        hiddenPosts = self.hiddenPosts()

        if blockedList:
            return UserPost.objects.exclude(user__in=blockedList).exclude(postID__in=hiddenPosts).order_by('-dateOfPost')
        else:
            return UserPost.objects.exclude(postID__in=hiddenPosts).order_by('-dateOfPost')

    def get_queryset(self):
        """ Returns a queryset. This will be filtered if the user passes either a tagName
            or a username. Note that if the user tries to pass a value not in the database, then
            an unfiltered set will be returned instead.

            :returns: A queryset of UserPosts.
        """
        tagName_val = False
        username_val = False

        if 'tagName' in self.request.GET:
            tagName_val = self.request.GET.get('tagName', False) 
            if not Tag.objects.filter(tagName=tagName_val).exists():
                return self.posts_filtered_by_blocked()

        if 'userName' in self.request.GET:
            username_val = self.request.GET.get('userName', False)
            if not User.objects.filter(username=username_val).exists():
                return self.posts_filtered_by_blocked()

            user_id = User.objects.get(username=username_val)

            # Ensure the user is not trying to access posts by a user blocking them
            if BlockedUser.objects.filter(blockedUser=self.request.user, blockedBy=user_id).exists():
                return UserPost.objects.none()

        if tagName_val: 
            tag = Tag.objects.get(tagName=tagName_val)
            tagmaps = Tagmap.objects.filter(tagID=tag)
            postList = [tm.postID.postID for tm in tagmaps]  
            filteredPosts = self.posts_filtered_by_blocked()  

            if username_val:
                return filteredPosts.filter(postID__in=postList, user=user_id).order_by('-dateOfPost') 
            else:
                return filteredPosts.filter(postID__in=postList).order_by('-dateOfPost') 
        elif username_val:
            hiddenPosts = self.hiddenPosts()
            return UserPost.objects.filter(user=user_id).exclude(postID__in=hiddenPosts).order_by('-dateOfPost')
        else: 
            return self.posts_filtered_by_blocked()

    def get_context_data(self, **kwargs):
        context = super(NewUpdatesListView, self).get_context_data(**kwargs)  
        current_username = self.request.user.username

        if 'tagName' in self.request.GET:
            context['tagName'] = self.request.GET.get('tagName', '')
        if 'userName' in self.request.GET:
            context['userName'] = self.request.GET.get('userName', '')

        context['current_username'] = current_username
        return context


class PrivacyPolicyPage(View):
    """ Creates the Privacy Policy page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Privacy Policy page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/privacypolicy.html')

    def post(self, request):
        """ Handles POST requests for the Privacy Policy page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return user_login(request)
        else:
            return render(request, 'tellings/privacypolicy.html')


class SignUpPage(View):
    """ Creates the sign up page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Sign Up page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        form = NewUserCreationForm()
        return render(request, 'tellings/signup.html', {'form': form})

    def post(self, request):
        """ Handles POST requests for the Sign Up page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
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

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, _('Please correct the error below.'))
            return render(request, 'tellings/signup.html', {'form': form})


class TagListView(LoginRequiredMixin, generic.ListView):
    """ Creates the Tags page for the website."""
    model = Tag
    paginate_by = 20
    http_method_names = ['get', 'post']


class TermsAndConditionsPage(View):
    """ Creates the Terms and Conditions page for the website."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests for the Terms and Conditions page.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/termsandconditions.html')

    def post(self, request):
        """ Handles POST requests for the Terms and Conditions page.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if ('username' in request.POST) and ('pwd' in request.POST):
            return user_login(request)
        else:
            return render(request, 'tellings/termsandconditions.html')


class UserCommentListView(LoginRequiredMixin, generic.ListView):
    """ Creates the User Comments html for the updates pages."""
    model = UserComment
    template_name = "tellings/usercomment_list.html"
    http_method_names = ['get']

    def get_queryset(self):
        postID_val = False
        new_context = False

        if 'postID' in self.request.GET:
            postID_val = self.request.GET.get('postID', False) 

            if UserPost.objects.filter(postID=postID_val).exists():
                current_user = self.request.user
                blockedUsers = BlockedUser.objects.filter(blockedBy=current_user)
                blockedList = [blocked.blockedUser for blocked in blockedUsers]
                new_context = UserComment.objects.filter(postID=postID_val).exclude(user__in=blockedList).order_by('-dateOfComment')

        return new_context

    def get_context_data(self, **kwargs):
        """ Adds the current logged in user's name to the context data, to allow
            comment editing/deleting only on their own posts. """
        context = super(UserCommentListView, self).get_context_data(**kwargs)  
        current_username = self.request.user.username
        context['current_username'] = current_username

        if 'postID' in self.request.GET:
            postID_val = self.request.GET.get('postID', False) 
            
            if UserPost.objects.filter(postID=postID_val).exists():
                post = UserPost.objects.get(postID=postID_val)
                author_of_post = post.user.username
                context['author_of_post'] = author_of_post

        return context


# #########################################################################################
# AJAX HANDLERS ---------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

class AddNewUpdate(LoginRequiredMixin, View):
    """ An AJAX handler used to add a new user update to the database."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if has_exceeded_max_posts(request):
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        elif ('postTitle' in request.POST) and ('postText' in request.POST) and ('postTags' in request.POST):
            response = self.addNewUpdate(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 

        return HttpResponse(json.dumps(response), content_type='application/json')

    def addNewUpdate(self, request): 
        """ Handles adding a new UserPost record to the database.
        
        :returns: A response dictionary.
        """
        user_text_input = [ request.POST['postTitle'],   
                            request.POST['postText'],   
                            request.POST['postTags'] ]

        for user_text in user_text_input:
            if contains_banned_word(user_text):
                response = {'status': StatusCode.CENSORED.value, 'message': _("Sorry, we cannot accept your post as it contains one or more banned words. The update has been censored. You can either now post the censored version of the update, or rewrite it with the banned words omitted.  Please refer to our acceptable usage policy for guidance!")} 
                return response

        # make a copy of POST to add user to as this is not supplied by the form       
        request.POST = request.POST.copy()
        request.POST['user'] = request.user.id
        now = django.utils.timezone.now()
        now = now.replace(tzinfo=timezone.utc)
        request.POST['dateOfPost'] = now

        form = UserPostForm(request.POST)

        if form.is_valid():
            form.save()
            response = {'status': StatusCode.SUCCESS.value, 'message': _("Your update has been added.")} 
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        
        return response


class AddUpdateModal(LoginRequiredMixin, View):
    """ An AJAX handler used to add the login modal to pages.
    """
    http_method_names = ['get']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        # Ensure that the user has not exceeded max allowed posts
        if has_exceeded_max_posts(request):
            return HttpResponse('false')

        return render(request, 'tellings/includes/addUpdate_modal.html')


class AddUserComment(LoginRequiredMixin, View):
    """ An AJAX handler used to add a new comment on a user update to the database."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if ('postID' in request.POST) and ('commentText' in request.POST): 
            response = self.addUserComment(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 

        return HttpResponse(json.dumps(response), content_type='application/json')

    def addUserComment(self, request):
        """ Adds a UserComment record to the database.  

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A response dictionary. 
        """    
        postID = request.POST.get('postID')

        if not UserPost.objects.filter(postID=postID).exists(): 
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        else:  
            commentText = request.POST['commentText']   

            if contains_banned_word(commentText):
                response = {'status': StatusCode.CENSORED.value, 'message': _("Sorry, we cannot accept your comment as it contains one or more banned words. The comment has been censored. You can either now post the censored version of the comment, or rewrite it with the banned words omitted.  Please refer to our acceptable usage policy for guidance!")}          
            else:
                request.POST = request.POST.copy()
                request.POST['user'] = request.user.id
                now = django.utils.timezone.now()
                now = now.replace(tzinfo=timezone.utc)
                request.POST['dateOfComment'] = now

                form = UserCommentForm(request.POST)
                
                if form.is_valid():
                    form.save()
                    response = {'status': StatusCode.SUCCESS.value, 'message': _("Error: Something went wrong with your request!")}
                else:
                    response = {'status': StatusCode.ERROR.value, 'message': _("Error: Invalid form data!")}   

        return response     


class BlockUser(LoginRequiredMixin, View):
    """ An AJAX handler used to add a new BlockedUser record to the database."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if ('username' in request.POST): 
            response = self.blockUser(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 

        return HttpResponse(json.dumps(response), content_type='application/json')

    def blockUser(self, request):
        """ Returns a response dictionary.
        """
        in_username = request.POST['username']   

        # Admin posts/comments cannot be blocked!!!
        if in_username in adminNameList:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot block administrators!")} 
        elif request.user.username == in_username:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot block yourself!")} 
        else:
            if not User.objects.filter(username=in_username).exists():
                response = {'status': StatusCode.ERROR.value, 'message': _("Error: The user you are trying to block does not exist!")} 
            else:
                in_blockedUser = User.objects.get(username=in_username)
                in_blockedBy = request.user
                bu = BlockedUser(blockedUser=in_blockedUser, blockedBy=in_blockedBy)
                bu.save()
                response = {'status': StatusCode.SUCCESS.value, 'message': _("You have successfully blocked the user.")} 

        return response


class CensorText(LoginRequiredMixin, View):
    """ An AJAX handler used to censor a text containing banned words. 
        Banned words are replaced with asterisks. """

    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if ('textToCensor' in request.POST):
            response = self.censorText(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 

        return HttpResponse(json.dumps(response), content_type='application/json')

    def censorText(self, request):
        """ Censors a text and returns it in a response dictionary.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A response dictionary.
        """
        textToCensor = request.POST['textToCensor'] 
        textToCensor = textToCensor.lower()

        for banned_word in banned_words:
            censoredText = textToCensor.replace(banned_word, "*" * len(banned_word))
            textToCensor = censoredText.replace(banned_word, "*" * len(banned_word))

        response = {'status': StatusCode.SUCCESS.value, 'message': censoredText} 

        return response


class CheckUserPassword(LoginRequiredMixin, View):
    """ An AJAX handler used to check a user's password.
        Used by the Delete Account modal. """

    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if ('pwd' in request.POST):
            response = self.isValidPassword(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 

        return HttpResponse(json.dumps(response), content_type='application/json')

    def isValidPassword(self, request):
        """ Checks whether the user has entered their password correctly.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A response dictionary.
        """
        current_password = request.user.password #user's password
        entered_password = request.POST['pwd']   #posted password
  
        passwords_match = check_password(entered_password, current_password)
        
        if passwords_match:
            response = {'status': StatusCode.SUCCESS.value, 'message': _("Valid password")} 
        else:
            response = {'status': StatusCode.INVALIDPASSWORD.value, 'message': _("You have entered an invalid password!")} 
        
        return response


class DeleteAccountModal(LoginRequiredMixin, View):
    """ An AJAX handler used to add the delete account modal to pages.
    """
    http_method_names = ['get']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/includes/deleteAccount_modal.html')


class DeleteUserComment(LoginRequiredMixin, View):
    """ An AJAX handler used to delete comments.
    """
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if ('commentID' in request.POST):
            response = self.deleteComment(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 

        return HttpResponse(json.dumps(response), content_type='application/json')

    def getUsernameForCommentID(self, in_commentID):
        """ Returns the name of the user who made the comment.
        """
        comment = UserComment.objects.get(commentID=in_commentID)
        username = comment.user.username
        return username

    def getUsernameOfPostAuthor(self, in_commentID):
        """ Returns the name of the user who made the post being commented upon.
        """
        comment = UserComment.objects.get(commentID=in_commentID)
        post = comment.postID
        username = post.user.username
        return username

    def deleteComment(self, request):
        """ Handles deleting a userComment.

        :returns: A response dictionary.
        """
        in_commentID = request.POST.get('commentID')

        if not UserComment.objects.filter(commentID=in_commentID).exists(): 
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        else:
            comment_username = self.getUsernameForCommentID(in_commentID)
            post_username = self.getUsernameOfPostAuthor(in_commentID)
            
            # Comments can either be deleted by the people who made them ...
            if( comment_username == request.user.username ):
                comment = UserComment.objects.get(commentID=in_commentID)
                comment.delete()
                response = {'status': StatusCode.SUCCESS.value, 'message': _("The comment has been deleted.")}  
            # ... or by the author of the post being commented upon.
            elif( post_username == request.user.username ):
                comment = UserComment.objects.get(commentID=in_commentID)
                comment.delete()
                response = {'status': StatusCode.SUCCESS.value, 'message': _("The comment has been deleted.")}                 
            else:
                response = {'status': StatusCode.ERROR.value, 'message': _("Error: You do not have the right to delete this comment!")} 

        return response


class DeleteUserPost(LoginRequiredMixin, View):
    """ An AJAX handler used to delete posts for the current user.
    """
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if ('postID' in request.POST):
            response = self.deleteUserPost(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 

        return HttpResponse(json.dumps(response), content_type='application/json')

    def getUsernameForPostID(self, in_postID):
        """ Returns the name of the user who made the post.
        """
        post = UserPost.objects.get(postID=in_postID)
        username = post.user.username
        return username

    def deleteUserPost(self, request):
        """ Handles deletiing a UserPost.

        :returns: A response dictionary.
        """
        postID = request.POST.get('postID')

        if not UserPost.objects.filter(postID=postID).exists(): 
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        else:
            username = self.getUsernameForPostID(postID)

            if( username == request.user.username ):
                post = UserPost.objects.get(postID=postID)
                post.delete()
                response = {'status': StatusCode.SUCCESS.value, 'message': _("Your post has been deleted.")} 
            else:
                response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot delete other people's posts!")} 
        
        return response


class EditUserComment(LoginRequiredMixin, generic.UpdateView):
    """ An AJAX handler used to add the edit user comment HTML to pages,
        and update UserComment records.
    """
    model = UserComment 
    template_name = "tellings/includes/editComment.html"    
    fields = ['postID', 'user', 'dateOfComment', 'dateOfEdit', 'commentText']  
    http_method_names = ['get', 'post']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.commentID
        return context

    def post(self, request):
        """ Handles POST requests.
   
        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if ('commentID' in request.POST and 'commentText' in request.POST):
            response = self.updateUserCommentRecord(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 

        return HttpResponse(json.dumps(response), content_type='application/json')
                
    def updateUserCommentRecord(self, request):
        """ Updates a UserComment record.
           
        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A response dictionary.
        """
        commentID = request.POST.get('commentID')
        if not UserComment.objects.filter(commentID=commentID).exists(): 
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        else:     
            in_commentID = request.POST.get('commentID')
            in_commentText = request.POST.get('commentText')

            if contains_banned_word(in_commentText):
                response = {'status': StatusCode.CENSORED.value, 'message': _("Sorry, we cannot accept your edit as it contains one or more banned words. The edit has been censored. You can either now post the censored version of the edit, or rewrite it with the banned words omitted. Please refer to our acceptable usage policy for guidance.")}
            else:
                userComment = UserComment.objects.get(commentID=in_commentID)

                if(userComment.user.username == request.user.username):
                    # Update the record (sql injection-safe)
                    now = django.utils.timezone.now()
                    now = now.replace(tzinfo=timezone.utc)
                    UserComment.objects.filter(commentID=in_commentID).update(commentText=in_commentText, dateOfEdit=now)
                    response = {'status': StatusCode.SUCCESS.value, 'message': _("Your comment has been updated.")} 
                else:
                    response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot edit other people's comments.")} 
        
        return response  


class EditUserPost(LoginRequiredMixin, generic.UpdateView):
    """ An AJAX handler used to add the edit user post HTML to pages,
        and update UserPost records.
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
   
        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if ('postID' in request.POST and 'postText' in request.POST):
            response = self.updateUserPostRecord(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 

        return HttpResponse(json.dumps(response), content_type='application/json')
                
    def updateUserPostRecord(self, request):
        """ Updates a UserPost record.
           
        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A response dictionary.
        """
        in_postID = request.POST.get('postID')
        in_postText = request.POST.get('postText')

        if not UserPost.objects.filter(postID=in_postID).exists(): 
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot edit a post that does not exist!")} 
        else:               
            if contains_banned_word(in_postText):
                response = {'status': StatusCode.CENSORED.value, 'message': _("Sorry, we cannot accept your edit as it contains one or more banned words. The edit has been censored. You can either now post the censored version of the edit, or rewrite it with the banned words omitted. Please refer to our acceptable usage policy for guidance.")} 
            else:
                userPost = UserPost.objects.get(postID=in_postID)

                if(userPost.user.username == request.user.username):
                    # Update the record (sql injection-safe)
                    now = django.utils.timezone.now()
                    now = now.replace(tzinfo=timezone.utc)
                    UserPost.objects.filter(postID=in_postID).update(postText=in_postText, dateOfEdit=now)
                    response = {'status': StatusCode.SUCCESS.value, 'message': _("Your post has been updated.")}
                else:
                    response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot edit other people's posts!")} 
        
        return response


class HasExceededMaxPosts(LoginRequiredMixin, View):
    """ An AJAX handler used to check if the currently logged in
        user has exceeded the max number of allowed posts."""
    http_method_names = ['get']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: True if the user has exceeded the max number of allowed posts, otherwise false.
        """
        if has_exceeded_max_posts(request): 
            response = {'status': StatusCode.ERROR.value, 'message': _("Sorry, you have already already made the maximum number of posts allowed per day!")} 
        else:
            response = {'status': StatusCode.SUCCESS.value, 'message': _("OK.")} 

        return HttpResponse(json.dumps(response), content_type='application/json')


class HidePost(LoginRequiredMixin, View):
    """ An AJAX handler used to add a new HidePost record to the database."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTTPResponse.
        """
        if ('postID' in request.POST): 
            response = self.hidePost(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        
        return HttpResponse(json.dumps(response), content_type='application/json')

    def hidePost(self, request):
        """ Returns a response dictionary.
        """
        in_postID = request.POST['postID']  

        if not UserPost.objects.filter(postID=in_postID).exists(): 
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: The post you are trying to hide does not exist!")} 
        else:
            in_post = UserPost.objects.get(postID=in_postID)
            in_hideFrom = request.user
            postername = in_post.user.username

            if postername in adminNameList:
                # AJAX does not redirect pages
                response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot hide posts by administrators!")} 
            elif HiddenPost.objects.filter(postID=in_post, hideFrom=in_hideFrom).exists():
                response = {'status': StatusCode.ERROR.value, 'message': _("Error: this post has already been hidden!")} 
            else:
                hp = HiddenPost(postID=in_post, hideFrom=in_hideFrom)
                hp.save()
                response = {'status': StatusCode.SUCCESS.value, 'message': _("The post will now be hidden from you!")} 

        return response


class LoginModal(View):
    """ An AJAX handler used to add the login modal to pages.
    """
    http_method_names = ['get']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/includes/login_modal.html')


class UnblockUser(LoginRequiredMixin, View):
    """ An AJAX handler used to delete an BlockedUser record from the database."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor.
        :returns: A HTTPResponse.
        """
        if ('username' in request.POST):
            response = self.unblockUser(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        
        return HttpResponse(json.dumps(response), content_type='application/json')

    def unblockUser(self, request):
        """ Returns a response dictionary.
        """
        in_username = request.POST['username']

        if not User.objects.filter(username=in_username).exists():
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot unblock a user that does not exist!")} 
        else:
            in_blockedUser = User.objects.get(username=in_username)
            in_blockedBy = request.user
            if not BlockedUser.objects.filter(blockedUser=in_blockedUser, blockedBy=in_blockedBy).exists():
                response = {'status': StatusCode.ERROR.value, 'message': _("Error: You have not blocked this user!")} 
            else:
                blocked = BlockedUser.objects.get(blockedUser=in_blockedUser, blockedBy=in_blockedBy)
                blocked.delete()
                response = {'status': StatusCode.SUCCESS.value, 'message': _("You have successfully unblocked the user.")} 

        return response


class UnhidePost(LoginRequiredMixin, View):
    """ An AJAX handler used to delete an HiddenPost record from the database."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor.
        :returns: A HTTPResponse.
        """
        if ('postID' in request.POST):
            response = self.unhidePost(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        
        return HttpResponse(json.dumps(response), content_type='application/json')

    def unhidePost(self, request):
        """ A response dictionary.
        """
        in_postID = request.POST['postID']

        if not UserPost.objects.filter(postID=in_postID).exists():
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot unhide a post that does not exist!")} 
        else:
            in_post = UserPost.objects.get(postID=in_postID)
            in_hideFrom = request.user

            if not HiddenPost.objects.filter(postID=in_post, hideFrom=in_hideFrom).exists():
                response = {'status': StatusCode.ERROR.value, 'message': _("Error: You have not hidden this post!")} 
            else:
                hidden = HiddenPost.objects.get(postID=in_post, hideFrom=in_hideFrom)
                hidden.delete()
                response = {'status': StatusCode.SUCCESS.value, 'message': _("You have successfully unhidden the post.")} 

        return response


class UnhideUserPosts(LoginRequiredMixin, View):
    """ An AJAX handler used to remove all HiddenPost records from the database
        by a specified user.
    """
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor.
        :returns: A HTTPResponse.
        """
        if ('user' in request.POST): 
            response = self.unhidePosts(request)
        else:
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: Something went wrong with your request!")} 
        
        return HttpResponse(json.dumps(response), content_type='application/json')

    def unhidePosts(self, request):
        """ Returns a response dictionary.
        """ 
        in_username = request.POST['user']  

        if not User.objects.filter(username=in_username).exists():
            response = {'status': StatusCode.ERROR.value, 'message': _("Error: You cannot unhide posts from a user that does not exist!")}   
        else:
            in_user = User.objects.get(username=in_username)
            postsByUser = UserPost.objects.filter(user=in_user)
            in_hideFrom = request.user

            if not HiddenPost.objects.filter(postID__in=postsByUser, hideFrom=in_hideFrom).exists():
                response = {'status': StatusCode.ERROR.value, 'message': _("Error: You have not hidden any of this user's posts!")}   
            else:
                postsToUnhide = HiddenPost.objects.filter(postID__in=postsByUser, hideFrom=in_hideFrom)

                for post in postsToUnhide:
                    post.delete()

                response = {'status': StatusCode.SUCCESS.value, 'message': _("The user's posts will now be unhidden from you.")} 
        
        return response

