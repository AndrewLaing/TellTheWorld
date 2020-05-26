from django import forms
from django.conf import settings as djangoSettings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _

from tellings.models import *

from datetime import datetime
import json


class ChangeUserDetailsForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class NewUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
            max_length=254,
            required=True,
            label = _('Email Address'),
            help_text = _('Required. A valid email address'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )      

    def save(self, commit=True):
        user = super(NewUserCreationForm, self).save(commit=False)

        if commit:
            user.save()

        return user


class DeleteAccountForm(forms.ModelForm):
    class Meta:
        model = DeletedAccount
        fields = ['deleted_date', 'deleted_reason', 'membership_length' ]   


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ('postID', 'user', 'dateOfComment', 'dateOfEdit', 'commentText') 


class UserPostForm(forms.ModelForm): 
    postTitle = forms.CharField(required=True,
                max_length=UserPost._meta.get_field('postTitle').max_length)
    postText =  forms.CharField(required=True,
                max_length=UserPost._meta.get_field('postText').max_length)


    def __init__(self, *args, **kwargs):
        self.tagList = False

        # pop post tags because this is not used to create a postRecord
        if len(args) > 0:
            if 'postTags' in args[0]:
                postTags = args[0].pop('postTags')
                self.tagList = json.loads(postTags[0])

        super(UserPostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserPost
        fields = ['user', 'dateOfPost','postTitle', 'postText']  
     

    def save(self, commit=True):
        """ Used to save the UserPost record and create its Tagmap records.
        """
        post = super(UserPostForm, self).save(commit=False)

        if commit:
            post.save()

        if self.tagList:
            self.add_tag_and_tagmap_records(post) 

        return post
        
    def add_tag_and_tagmap_records(self, post):
        """ Used to add any new tags created with the post,
            and create Tagmaps for the post.
        """
        for tagName in self.tagList:
            tagName = tagName.lower()
            if Tag.objects.filter(tagName=tagName).exists():
                tag = Tag.objects.get(tagName=tagName)
            else:
                tag = Tag(tagName=tagName)
                tag.save()

            if not Tagmap.objects.filter(postID=post, tagID=tag).exists():
                tm = Tagmap(postID=post, tagID=tag)
                tm.save()  
        
        # Update the tagNames.json file used for tag completion
        self.update_tagnames_JSON_file()
       
    def update_tagnames_JSON_file(self): 
        """ Used to update the JSON file used for tag completion. """    
        updatedTags = list(Tag.objects.values_list('tagName', flat=True))

        with open(djangoSettings.TELLINGS_ROOT+'/static/tellings/data/tagNames.json', 'w') as f:
            json.dump(updatedTags, f)

