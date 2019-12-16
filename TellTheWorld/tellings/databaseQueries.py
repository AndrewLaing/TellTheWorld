# Filename:     databaseQueries.html
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last updated: 28/11/2019.
# Description:  Contains the query and insert functions used in tellings/views.py.

from django.conf import settings as djangoSettings
from tellings.models import Posts, Tags, Tagmap
from datetime import datetime, date, timedelta 
import json, re

MAX_POST_TITLE_LEN = Posts._meta.get_field('postTitle').max_length
MAX_POST_TEXT_LEN = Posts._meta.get_field('postText').max_length
MAX_POST_TAG_LEN = Tags._meta.get_field('tagName').max_length


def sanitiseString(user_str):
    """ Removes characters which could be used to create
        HTML tags and entities from a string.

    :param user_str: A text string to be sanitised.
    :returns: A sanitised string.
    """
    unwanted = "[\<\>\&]"
    user_str = re.sub(unwanted, '', user_str)
    return user_str


def getAllTagNames():
    """ Gets a list of all tagnames in the Tags table.

    :returns: A list of all tagnames.
    """
    tagList = list(Tags.objects.values_list('tagName', flat=True))
    return tagList


def getTagNamesByPostID(in_postID):
    """ Gets a list of all tagnames attached to a user update.

    :param postID: A post ID number. (e.g., 42)
    :returns: A list of tagnames.
    """
    tagmaps = Tagmap.objects.filter(postID=in_postID)
    tagList = sorted([tag.tagID.tagName for tag in tagmaps])
    return tagList


def getAllPostDetails():
    """ Gets a list of all user updates from the Posts table.

    :returns: A list of all user updates. (e.g., [ [postID, dateOfPost, username, postTitle, postText], [postID, ...])
    """
    posts = Posts.objects.all().order_by('-dateOfPost')
    postDetails = [[post.postID, post.dateOfPost.strftime("%d %B %Y"), 
                    post.user.username, post.postTitle, post.postText] for post in posts]
    return postDetails  


def getAllPostsByUserID(in_userID):
    """ Gets a list of all updates for a specified user from the Posts table.

    :param in_userID: A user ID number (e.g., 42) 
    :returns: A list of user updates. (e.g., [ [postID, dateOfPost, username, postTitle, postText], [postID, ...])
    """
    posts = Posts.objects.filter(user=in_userID).order_by('-dateOfPost')
    postDetails = [[post.postID, post.dateOfPost.strftime("%d %B %Y"), post.user.username, post.postTitle, post.postText] for post in posts]
    return postDetails  


def getAllPostsByTagname(in_TagName):
    """ Gets a list of all user updates tagged with a specified tag from the Posts table.

    :param in_TagName: A tag name (e.g., 'fantastic') 
    :returns: A list of user updates. (e.g., [ [postID, dateOfPost, username, postTitle, postText], [postID, ...])
    """
    postDetails = []
    sql  = "SELECT * FROM tellings_posts"
    sql += " INNER JOIN tellings_tagmap ON (tellings_posts.postID=tellings_tagmap.postID)"
    sql += " INNER JOIN tellings_tags ON (tellings_tags.tagID=tellings_tagmap.tagID)"
    sql += " WHERE tellings_tags.tagName=%s ORDER BY dateOfPost DESC;"
    posts_obj = Posts.objects.raw(sql, (in_TagName,))
    for post in posts_obj:
        dateOfPost = post.dateOfPost.strftime("%d %B %Y")
        postDetails.append([post.postID, dateOfPost, post.user.username, post.postTitle, post.postText])
    return postDetails  


def getAllPostsByTagnameForUserID(in_TagName, in_userID):
    """ Gets a list of user updates tagged with a specified tag for a specified user ID 
        from the Posts table.

    :param in_TagName: A tag name (e.g., 'fantastic') 
    :param in_userID: A user ID number (e.g., 42) 
    :returns: A list of user updates. (e.g., [ [postID, dateOfPost, username, postTitle, postText], [postID, ...])
    """
    postDetails = []
    sql  = "SELECT * FROM tellings_posts"
    sql += " INNER JOIN tellings_tagmap ON (tellings_posts.postID=tellings_tagmap.postID)"
    sql += " INNER JOIN tellings_tags ON (tellings_tags.tagID=tellings_tagmap.tagID)"
    sql += " WHERE tellings_tags.tagName=%s AND tellings_posts.user=%s ORDER BY dateOfPost DESC;"
    posts_obj = Posts.objects.raw(sql, (in_TagName, in_userID,))
    for post in posts_obj:
        dateOfPost = post.dateOfPost.strftime("%d %B %Y")
        postDetails.append([post.postID, dateOfPost, post.user.username, post.postTitle, post.postText])
    return postDetails 


def getPostIDFromLastPostRecordAdded():
    """ Gets the postID number from the last record added to the Posts table.

    :returns: A postID number (e.g., 42)
    """
    post = Posts.objects.latest('postID')
    result = post.postID
    return result


def getTagIDFromLastTagRecordAdded():
    """ Gets the tagID number from the last record added to the Tags table.

    :returns: A tagID number (e.g., 42)
    """
    tag = Tags.objects.latest('tagID')
    result = tag.tagID
    return result


def userHasPostedToday(in_userID):
    """ Used to determine if the user has posted an update today.
    
    :param in_userID: A user ID number (e.g., 42)      
    :returns: True if the user has posted an update today,
              otherwise false
    """
    yesterday = date.today() - timedelta(1)
    posts = Posts.objects.filter(user=in_userID).filter(dateOfPost__gt=yesterday)
    return len(posts) > 0


def postTitleExists(in_postTitle):
    """ Used to determine if the user has entered a unique post title.
    
    :param in_postTitle: The title of a user update (e.g., 'Snakes are great')      
    :returns: True if the post title does exist in the Posts table,
              otherwise false.
    """
    posts = Posts.objects.filter(postTitle=in_postTitle)
    return len(posts) > 0


def addNewPostUpdateRecords(request):
    """ Used to add a new Post record, Tag record(if necessary),
        and Tagmap record to the database.
    
    :param request: A dictionary-like object containing all HTTP POST parameters, 
                    sent by a user from addUpdateModal.       
    :returns: N/A
    """
    current_user_id = request.user.id
    dateOfPost = date.today()

    # Sanitise and shorten the strings to prevent XSS and overflows
    postTitle = sanitiseString(request.POST['postTitle'])[:MAX_POST_TITLE_LEN]
    postText = sanitiseString(request.POST['postText'])[:MAX_POST_TEXT_LEN]

    postTags = request.POST['postTags']
    tagList = json.loads(postTags)

    # insert post record
    addPostRecord(current_user_id, dateOfPost, postTitle, postText)
    postID = getPostIDFromLastPostRecordAdded()

    #insert tag and tagmap records
    for tag in tagList:
        # If the tag already has a record get its ID
        tagRecords = Tags.objects.filter(tagName=tag)

        if len(tagRecords) > 0:
            tagID = tagRecords[0].tagID
        else:
            # otherwise create a tag new record and get its ID
            tag = sanitiseString(tag)[:MAX_POST_TAG_LEN]
            addTagRecord(tag)

            # recreate the taglist used for tag completion
            updatedTags = getAllTagNames()
            with open(djangoSettings.STATIC_ROOT+'/tellings/data/tagNames.json', 'w') as f:
                json.dump(updatedTags, f)

            tagID = getTagIDFromLastTagRecordAdded()

        addTagmapRecord(postID, tagID)


def updatePostsRecordPostText(in_postID, in_postText):
    """ Used to update the postText of a Posts record.
    
    :param in_postID:   A Posts record ID   
    :param in_postText: Text for a post. (e.g., 'It was a fantastic day.')       
    :returns: N/A
    """
    post = Posts.objects.get(postID=in_postID)
    postText = sanitiseString(in_postText)[:MAX_POST_TEXT_LEN]
    post.postText = postText
    post.save()


def addTagRecord(name):
    """ Used to add a new Tag record to the database.
    
    :param name: A tagname. (e.g., 'fantastic')       
    :returns: N/A
    """
    tag = Tags(tagName=name)
    tag.save()
    

def addPostRecord(in_userID, in_dateOfPost, in_postTitle, in_postText):
    """ Used to add a new Post record to the database.
    
    :param in_userID: A user ID number (e.g., 42)    
    :param in_dateOfPost: The date of the post (e.g., '02 August 2019')      
    :param in_postTitle: The title of the post (e.g., 'Snakes are great')        
    :param in_postText: The text of the post. (e.g., 'Today I went to the zoo and saw snakes.')       
    :returns: N/A
    """
    post = Posts(user_id=in_userID, dateOfPost=in_dateOfPost, postTitle=in_postTitle, postText=in_postText)
    post.save()


def addTagmapRecord(in_postID, in_tagID):
    """ Used to add a new Tagmap record to the database.
    
    :param in_postID: A post ID number (e.g., 42)    
    :param in_tagID: A tag ID number (e.g., 42)           
    :returns: N/A
    """
    tm = Tagmap( postID_id=in_postID, tagID_id=in_tagID)
    tm.save()
