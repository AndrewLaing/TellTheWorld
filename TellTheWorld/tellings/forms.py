from django import forms
from django.conf import settings as djangoSettings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

from tellings.models import *

from datetime import datetime
import json


class ChangeUserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]


class NewUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,
            label = _('Email Address'),
            error_messages={'exists': _('Sorry. An account attached to this email address already exists.')},
            help_text = _('A valid email address'))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")        

    def save(self, commit=True):
        user = super(NewUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


class DeleteAccountForm(forms.ModelForm):
    class Meta:
        model = DeletedAccount
        fields = ['deleted_date', 'deleted_reason', 'membership_length' ]   


class UserPostForm(forms.ModelForm):
    
    postTitle = forms.CharField(required=True,
                max_length=UserPost._meta.get_field('postTitle').max_length, 
                label = _('Post Title'),
                help_text = _('A unique title post'))
    postText =  forms.CharField(required=True,
                max_length=UserPost._meta.get_field('postText').max_length,
                label = _('Post Text'),
                help_text = _('Your post text.'))


    def __init__(self, *args, **kwargs):
        self.tagList = False
        
        # pop post tags because this is not used to create a postRecord
        if len(args) > 0:
            postTags = args[0].pop('postTags')
            self.tagList = json.loads(postTags[0])

        super(UserPostForm, self).__init__(*args, **kwargs)


    class Meta:
        model = UserPost
        fields = ['user', 'dateOfPost','postTitle', 'postText']  
        labels = {
            'postText': _('Post Text'),
            'postTitle': _('Post Title')
        }
        help_texts = {
            'postText': _('The text for your post'),
            'postTitle': _('A unique post title')
        }
        error_messages = {
            'postText': {
                'max_length': _("The text you have entered is too long."),
                'already_exists': _("The Post title you have entered has already been used."),
            },
            'name': {
                'max_length': _("The title of your post is too long."),
            },
        }        

    def save(self, commit=True):
        """ Used to save the UserPost record and create its Tagmap records.
        """
        post = super(UserPostForm, self).save(commit=False)

        if commit:
            post.save()

        postID = post.postID

        # add the Tag and Tagmap records attached to the post
        if self.tagList:
            self.add_tag_and_tagmap_records(postID) 

        return post
        
    def add_tag_and_tagmap_records(self, postID):
        """ Used to add any new tags created with the post,
            and create Tagmaps for the post.
        """
        for tagName in self.tagList:
            tagRecords = Tag.objects.filter(tagName=tagName)

            if len(tagRecords) > 0:
                tagID = tagRecords[0].tagID
            else:
                tag = Tag(tagName=tagName)
                tag.save()
                tagID = tag.tagID

            if not Tagmap.objects.filter(postID_id=postID, tagID_id=tagID).exists():
                tm = Tagmap(postID_id=postID, tagID_id=tagID)
                tm.save()  
        
        # Update the tagNames.json file used for tag completion
        self.update_tagnames_JSON_file()
       
    def update_tagnames_JSON_file(self): 
        """ Used to update the JSON file used for tag completion. """    
        updatedTags = list(Tag.objects.values_list('tagName', flat=True))

        with open(djangoSettings.TELLINGS_ROOT+'/static/tellings/data/tagNames.json', 'w') as f:
            json.dump(updatedTags, f)

    def clean_postTitle(self):
        postTitle = self.cleaned_data['postTitle']
        if UserPost.objects.filter(postTitle=postTitle).exists():
            raise forms.ValidationError("already_exists")
        return postTitle
