# Filename:     views.py
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last updated: 25/02/2020
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

# #########################################################################################
# SHARED FUNCTIONS ------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


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


def user_has_posted_today(request):
    """ Used to determine if the user has already posted an update today.
    
    :param request: A dictionary-like object containing the HTTP POST parameters, 
                    sent by a site visitor.     
    :returns: True if the user has posted an update today, otherwise false.
    """
    current_userID = request.user.id
    yesterday = django.utils.timezone.now() - timedelta(1)
    return UserPost.objects.filter(user=current_userID).filter(dateOfPost__gt=yesterday).exists()

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
        :returns: A HTML page.
        """
        try:
            u = request.user

            # Create a DeletedAccount record
            deleted_date = django.utils.timezone.now()
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
            return render(request, 'tellings/accountDeleted.html')
        except:
            return HttpResponseRedirect('/errorpage/')


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
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            return self.changePassword(request, form)
        else:
            return render(request, 'tellings/changePassword.html', {'form': form})

    def changePassword(self, request, form):
        """ Handles changing the user's password.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor.
        :param form: A Django form object.
        :returns: A HTML page.
        """
        form.save()
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        return render(request, 'tellings/changePassword.html', 
                      {'message': _('Your password was successfully updated!'), 'form': form})


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
        form = ChangeUserDetailsForm(request.POST)
        if form.is_valid():
            return self.changeDetails(request, form)
        else:
            messages.error(request, _('Please correct the error below.'))
            return render(request, 'tellings/changeUserDetails.html', {'form': form})

    def changeDetails(self, request, form):
        """ Handles changing the user's details.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor.  
        :returns: A HTML page.
        """
        u = request.user
        u.first_name = request.POST['first_name']
        u.last_name = request.POST['last_name']
        u.email = request.POST['email']
        u.save()
        return render(request, 'tellings/changeUserDetails.html', 
                      {'message': _('Your details have been updated'), 'form': form})


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
        else:   # get all posts for current user
            qs = qs.filter(user=user_id).order_by('-dateOfPost')

        return qs

    def get_context_data(self, **kwargs):
        context = super(MyUpdatesListView, self).get_context_data(**kwargs)  
        current_username = user_id = self.request.user.username

        if self.request.method == 'GET' and 'tagName' in self.request.GET:
            context['tagName'] = self.request.GET.get('tagName', '')

        context['current_username'] = current_username
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

        if self.request.method == 'GET':
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

        if self.request.method == 'GET':
            if 'postID' in self.request.GET:
                postID_val = self.request.GET.get('postID', False) 
       
        if postID_val:
            new_context = UserComment.objects.filter(postID=postID_val).order_by('-dateOfComment') 
        
        return new_context

    def get_context_data(self, **kwargs):
        """ Adds the current logged in user's name to the context data, to allow
            comment editing/deleting only on their posts. """
        context = super(UserCommentListView, self).get_context_data(**kwargs)  
        current_username = user_id = self.request.user.username
        context['current_username'] = current_username

        if self.request.method == 'GET':
            if 'postID' in self.request.GET:
                postID_val = self.request.GET.get('postID', False) 
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
        :returns: A string 'true' if the title already exists in the UserPost table,
                  otherwise a redirect to the error page.
        """
        if user_has_posted_today(request):
            return HttpResponseRedirect('/errorpage/')

        if ('postTitle' in request.POST) and ('postText' in request.POST) and ('postTags' in request.POST):

            postTitle = request.POST['postTitle']   
            postText = request.POST['postText']   
            postTags = request.POST['postTags']   

            if contains_banned_word(postTitle):
                return HttpResponse('censored')  
            elif contains_banned_word(postText):
                return HttpResponse('censored')  
            elif contains_banned_word(postTags):
                return HttpResponse('censored')  
            

            # make a copy of POST to add user to as this is not supplied by the form       
            request.POST = request.POST.copy()
            request.POST['user'] = request.user.id
            request.POST['dateOfPost'] = django.utils.timezone.now()

            form = UserPostForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('true')
            else:
                return HttpResponseRedirect('/errorpage/')
        else:
            return HttpResponseRedirect('/errorpage/')


class AddUpdateModal(LoginRequiredMixin, View):
    """ An AJAX handler used to add the login modal to pages.
    """
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        # Ensure that the user has not posted today
        if user_has_posted_today(request):
            return HttpResponse('false')

        return render(request, 'tellings/includes/addUpdate_modal.html')

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        # Ensure that the user has not posted today
        current_user_id = request.user.id
        if user_has_posted_today(request):
            return HttpResponse('false')

        return render(request, 'tellings/includes/addUpdate_modal.html')


class AddUserComment(LoginRequiredMixin, View):
    """ An AJAX handler used to add a new comment on a user update to the database."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A string 'true' if the comment was successfully added to UserComment table,
                  'censored' if the comment contains banned words, 'false' if the comment
                  couldn't be added, otherwise a redirect to the error page if POST data is missing.
        """
        if ('postID' in request.POST) and ('commentText' in request.POST): 
            commentText = request.POST['commentText']   

            if contains_banned_word(commentText):
                return HttpResponse('censored')           

            # make a copy of POST to add fields not supplied by the client                   
            request.POST = request.POST.copy()
            request.POST['user'] = request.user.id
            request.POST['dateOfComment'] = django.utils.timezone.now()

            form = UserCommentForm(request.POST)
            
            if form.is_valid():
                form.save()
                return HttpResponse('true')
            else:
                return HttpResponse('false')
        else:
            return HttpResponseRedirect('/errorpage/')

 
class CensorText(LoginRequiredMixin, View):
    """ An AJAX handler used to censor a text containing banned words. 
        Banned words are replaced with asterisks. """

    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A censored text string.
        """
        if ('textToCensor' in request.POST):
            return self.censorText(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def censorText(self, request):
        """ Censors a text and returns it as a HttpResponse.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A censored text string.
        """
        textToCensor = request.POST['textToCensor'] 
        textToCensor = textToCensor.lower()

        for banned_word in banned_words:
            censoredText = textToCensor.replace(banned_word, "*" * len(banned_word))
            textToCensor = censoredText.replace(banned_word, "*" * len(banned_word))

        return HttpResponse(censoredText)


class CheckUserPassword(LoginRequiredMixin, View):
    """ An AJAX handler used to check a user's password.
        Used by the Delete Account modal. """

    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A string 'true' if the password is valid, otherwise 'false'.
        """
        if ('pwd' in request.POST):
            return self.isValidPassword(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def isValidPassword(self, request):
        """ Checks whether the user has entered their password correctly.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A string 'true' if the password is valid, otherwise 'false'.
        """
        current_password = request.user.password #user's password
        entered_password = request.POST['pwd']   #posted password
  
        passwords_match = check_password(entered_password, current_password)
        
        if passwords_match:
            return HttpResponse('true')
        else:
            return HttpResponse('false')


class DeleteAccountModal(LoginRequiredMixin, View):
    """ An AJAX handler used to add the delete account modal to pages.
    """
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/includes/deleteAccount_modal.html')

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
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
        :returns: A string 'true' if the comment was deleted, otherwise an error message.
        """
        if ('commentID' in request.POST):
            commentID = request.POST.get('commentID')
            comment_username = self.getUsernameForCommentID(commentID)
            post_username = self.getUsernameOfPostAuthor(commentID)
            
            # Comments can either be deleted by the people who made them ...
            if( comment_username == request.user.username ):
                if self.deleteComment(commentID):
                    return HttpResponse("true")
                else:
                    return HttpResponse(_("Something went wrong. We were unable to delete your comment."))
            # ... or by the author of the post being commented upon.
            elif( post_username == request.user.username ):
                if self.deleteComment(commentID):
                    return HttpResponse("true")
                else:
                    return HttpResponse(_("Something went wrong. We were unable to delete this comment."))
            else:
                return HttpResponse(_("YOU CANNOT DELETE THIS COMMENT!!!"))
        else:
            return HttpResponseRedirect('/errorpage/')

    def getUsernameForCommentID(self, in_commentID):
        """ Returns the name of the user who made the comment.
        """
        try:
            comment = UserComment.objects.get(commentID=in_commentID)
            username = comment.user.username
            return username
        except:
            return None

    def getUsernameOfPostAuthor(self, in_commentID):
        """ Returns the name of the user who made the post being commented upon.
        """
        try:
            comment = UserComment.objects.get(commentID=in_commentID)
            in_postID = comment.postID.postID
            post = UserPost.objects.get(postID=in_postID)
            username = post.user.username
            return username
        except:
            return None

    def deleteComment(self, in_commentID):
        """ Handles deleting a userComment.
        """
        try:
            comment = UserComment.objects.get(commentID=in_commentID)
            comment.delete()
            return True
        except:
            return False


class DeleteUserPost(LoginRequiredMixin, View):
    """ An AJAX handler used to delete posts for the current user.
    """
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A string 'true' if the post was deleted, otherwise an error message.
        """
        if ('postID' in request.POST):
            postID = request.POST.get('postID')
            username = self.getUsernameForPostID(postID)

            # Check that the post was made by the user deleting it
            if( username == request.user.username ):
                if self.deletePost(postID):
                    return HttpResponse("true")
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
        :returns: A string 'true' if the comment could be edited, otherwise an error message.
        """
        if ('commentID' in request.POST and 'commentText' in request.POST):
            return self.updateUserCommentRecord(request)
        else:
            return HttpResponseRedirect('/errorpage/')
                
    def updateUserCommentRecord(self, request):
        """ Updates a UserComment record.
           
        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A string 'true' if the comment could be edited, 'censored' if the comment
                  contains a banned word, otherwise an error message.
        """
        in_commentID = request.POST.get('commentID')
        in_commentText = request.POST.get('commentText')

        if contains_banned_word(in_commentText):
            return HttpResponse('censored')

        userComment = get_object_or_404(UserComment, commentID=in_commentID)

        if(userComment.user.username == request.user.username):
            try:
                # Update the record (sql injection-safe)
                today = django.utils.timezone.now()
                UserComment.objects.filter(commentID=in_commentID).update(commentText=in_commentText, dateOfEdit=today)
                return HttpResponse("true")
            except:
                return HttpResponse(_("Unable to make changes to the comment. Please contact the site administrator."))
        else:
            return HttpResponse(_("YOU CANNOT EDIT OTHER USERS COMMENTS!!!"))  


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
        :returns: A string 'true' if the post could be edited, otherwise an error message.
        """
        if ('postID' in request.POST and 'postText' in request.POST):
            return self.updateUserPostRecord(request)
        else:
            return HttpResponseRedirect('/errorpage/')
                
    def updateUserPostRecord(self, request):
        """ Updates a UserPost record.
           
        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A string 'true' if the post could be edited, otherwise an error message.
        """
        in_postID = request.POST.get('postID')
        in_postText = request.POST.get('postText')

        if contains_banned_word(in_postText):
            return HttpResponse('censored')

        userPost = get_object_or_404(UserPost, postID=in_postID)

        if(userPost.user.username == request.user.username):
            try:
                # Update the record (sql injection-safe)
                today = django.utils.timezone.now()
                UserPost.objects.filter(postID=in_postID).update(postText=in_postText, dateOfEdit=today)
                return HttpResponse("true")
            except:
                return HttpResponse(_("Unable to make changes to the post. Please contact the site administrator."))
        else:
            return HttpResponse(_("YOU CANNOT EDIT OTHER USERS POSTS!!!"))   


class HasPostedToday(LoginRequiredMixin, View):
    """ An AJAX handler used to check whether the currently logged in
        user has posted an update today or not."""
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A string 'true' if the user has already posted an update today,
                  otherwise 'false'.
        """
        if user_has_posted_today(request):
            return HttpResponse('true')
        else:
            return HttpResponse('false')

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        if user_has_posted_today(request):
            return HttpResponse('true')
        else:
            return HttpResponse('false')


class LoginModal(View):
    """ An AJAX handler used to add the login modal to pages.
    """
    http_method_names = ['get', 'post']

    def get(self, request):
        """ Handles GET requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/includes/login_modal.html')

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all HTTP POST parameters 
                        sent by a site visitor. 
        :returns: A HTML page.
        """
        return render(request, 'tellings/includes/login_modal.html')


class TitleExists(LoginRequiredMixin, View):
    """ An AJAX handler used to check if a post title already
        exists within the UserPost table or not."""
    http_method_names = ['post']

    def post(self, request):
        """ Handles POST requests.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A string 'true' if the title already exists in the UserPost table,
                  otherwise 'false'.
        """
        if ('title' in request.POST):
            return self.titleExists(request)
        else:
            return HttpResponseRedirect('/errorpage/')

    def titleExists(self, request):
        """ Checks whether an update title already exists within the UserPost table or not.
            This function can only be used by authenticated users.

        :param request: A dictionary-like object containing all the HTTP parameters 
                        sent by a site visitor. 
        :returns: A string 'true' if the title already exists in the UserPost table,
                  'censored' if the title contains a banned word,
                  otherwise 'false'.
        """
        in_postTitle = request.POST['title']

        if contains_banned_word(in_postTitle):
            return HttpResponse('censored')

        if UserPost.objects.filter(postTitle=in_postTitle).exists():
            return HttpResponse('true')
        else:
            return HttpResponse('false')
            