# Filename:     createUpdatesHTML.html
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last updated: 11/11/2019.
# Description:  Contains functions used to create the content HTML for
#               the user updates shown on tags.html, myupdates.html 
#               and newupdates.html.

from tellings.models import Posts, Tags, Tagmap
import tellings.databaseQueries as DBQ
import re


def sanitiseString(user_str):
    """ Removes characters which could be used to create
        HTML tags and entities from a string.

    :param user_str: A text string to be sanitised.
    :returns: A sanitised string.
    """
    unwanted = "[\<\>\&]"
    user_str = re.sub(unwanted, '', user_str)
    return user_str


def createInnerHTML(postDetails, username):
    """ Creates the content HTML for the user updates shown on 
        tags.html, myupdates.html and newupdates.html

    :param postDetails: A 2D list of user update details. (e.g., [ [29, '02 August 2019', 'admin', 'posttitle', 'postText.'],[30, ...]])
    :returns: A string containing HTML.
    """
    innerHTML = ''
    isFirstPost = True
    count = 1
    for updateDetails in postDetails:
        if isFirstPost:
            previousDate = updateDetails[1]

        postID = updateDetails[0]

        innerHTML += createUpdateHTML(previousDate, isFirstPost, updateDetails, count, username)

        if isFirstPost:
            isFirstPost = False

        previousDate = updateDetails[1]

        tagList = DBQ.getTagNamesByPostID(postID)
        innerHTML += createTagsHTML(tagList)

        count+=1
    if len(postDetails)==0:
        innerHTML = createNoResultsHTML()
    else:
        innerHTML += createDivClosingHTML()

    return innerHTML


def createNoResultsHTML():
    """ Creates the content HTML for the user updates shown on tags.html, 
        myupdates.html and newupdates.html when no results are found

    :returns: A string containing HTML.
    """
    innerHTML = '''
<div class="row">
  <h1>No results found!</h1>
</div>'''
    return innerHTML


def createUpdateHTML(previousDate, isFirstPost, updateDetails, count, username):
    """ Creates the HTML for a user update panel.

    :param previousDate: The date of the previous post (e.g., '02 August 2019')
    :param isFirstPost: True if this is the first post to be added to the HTML, otherwise false.
    :param updateDetails: A list of user update details. (e.g., [29, '02 August 2019', 'admin', 'posttitle', 'postText.'])
    :param count: A number used to make all update panels uniquely collapsable.
    :returns: A string containing HTML.
    """

    innerHTML = ''
    postID = updateDetails[0]
    dateOfPost = updateDetails[1]

    if isFirstPost:
        innerHTML += createFirstRowHeaderHTML(postID, dateOfPost)
    elif dateOfPost != previousDate:
        innerHTML += createNewRowHeaderHTML(postID, dateOfPost)
    else:
        innerHTML += createNewUpdatePanelHeader(postID)
           
    
    # Allow users to edit their own posts
    postUsername = updateDetails[2]

    if(postUsername==username):
        innerHTML += createUpdatePanelContentsForCurrentUser(updateDetails, count)
    else:
        innerHTML += createUpdatePanelContents(updateDetails, count)

    return innerHTML


def createTagsHTML(tagList):
    """ Creates the HTML for the tag links in a user update panel.

    :param tagList: A list of tags. (e.g., ['tag1','tag2','tag3'] )
    :returns: A string containing HTML.
    """
    innerHTML = '''
  <div class="panel-footer align-panel-text-right">'''

    for tag in tagList:
        #sanitise tag here
        tag = sanitiseString(tag)
        innerHTML += '''  
    <a href="#" class="tagName" name="{tagname}" onclick="return false;">{tagname}</a>
    &nbsp;&nbsp;|&nbsp;&nbsp;'''.format(tagname=tag)

    innerHTML += '''
  </div>
</div>
<!-- End of Update Panel -->'''
    return innerHTML


def createUpdatePanelContents(updateDetails, count):
    """ Creates the HTML for a user update panel.

    :param updateDetails: A list of user update details. (e.g., [29, '02 August 2019', 'admin', 'posttitle', 'postText.'])
    :param count: A number used to make all update panels uniquely collapsable.
    :returns: A string containing HTML.
    """
    postID = updateDetails[0]
    username  = sanitiseString(updateDetails[2])
    postTitle = sanitiseString(updateDetails[3])
    postText  = sanitiseString(updateDetails[4])
    innerHTML = '''
  <div class="col-sm-8 panel-postTitle">
    <p><a href="#" class="posterName" name="{user}" onclick="return false;">
    {user} says</a> ... {title}</p>
  </div>
  <div class="col-sm-4 align-panel-text-right">
      <button class="btn btn-info" data-toggle="collapse" data-target="#collapse{cnt}">View Update</button>

      <!-- Edit post -->
      <div class="btn-group">
          <button type="button" class="btn dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <span class = "caret"></span>
          </button>
          <div class="dropdown-menu">
          <a class="dropdown-item" id="hide_post_{id}" onclick="$.hide_post({id});">Hide Post</a>
          </div>
      </div>  
  </div>         
</div> <!-- End of Panel header -->
<div id="collapse{cnt}" class="panel-collapse collapse">
  <div class="panel-body">
    <p id="text_post_{id}">{text}</p>
  </div>
</div>'''.format(id=postID, user=username, title=postTitle, text=postText, cnt=count)
    return innerHTML


def createUpdatePanelContentsForCurrentUser(updateDetails, count):
    """ Creates the HTML for a user update panel.

    :param updateDetails: A list of user update details. (e.g., [29, '02 August 2019', 'admin', 'posttitle', 'postText.'])
    :param count: A number used to make all update panels uniquely collapsable.
    :returns: A string containing HTML.
    """
    postID = updateDetails[0]
    username  = sanitiseString(updateDetails[2])
    postTitle = sanitiseString(updateDetails[3])
    postText  = sanitiseString(updateDetails[4])
    innerHTML = '''
  <div class="col-sm-8 panel-postTitle">
    <p><a href="#" class="posterName" name="{user}" onclick="return false;">
    {user} says</a> ... {title}</p>
  </div>
  <div class="col-sm-4 align-panel-text-right">
    <!-- View Update button -->
    <button class="btn btn-info" data-toggle="collapse" data-target="#collapse{cnt}">View Update</button>

    <!-- Edit post -->
    <div class="btn-group">
        <button type="button" class="btn dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        <span class = "caret"></span>
        </button>
        <div class="dropdown-menu">
        <a class="dropdown-item" id="hide_post_{id}" onclick="$.hide_post({id});">Hide Post</a><br /><br />
        <a class="dropdown-item" id="edit_post_{id}" onclick="$.edit_post({id});">Edit Post</a><br />
        <a class="dropdown-item" id="delete_post_{id}" onclick="$.delete_post({id});">Delete Post</a>
        </div>
    </div>    
  </div>         
</div> <!-- End of Panel header -->
<div id="collapse{cnt}" class="panel-collapse collapse">
  <div class="panel-body">
    <p id="text_post_{id}">{text}</p>
  </div>
</div>'''.format(id=postID, user=username, title=postTitle, text=postText, cnt=count)
    return innerHTML


def createFirstRowHeaderHTML(postID, dateOfPosts):
    """ Creates the HTML for the header of the first row of user update panels.

    :param dateOfPost: The date of a group of user update posts (e.g., '02 August 2019')
    :returns: A string containing HTML.
    """
    innerHTML =  '''
<div class="row">
  <h1>{date}</h1>   
  <div class="panel-group">  
    <!-- Update panel --> 
    <div class="panel panel-default" id="panel_post_{id}">
      <div>  <!-- Panel header -->'''.format(date=dateOfPosts, id=postID)
    return innerHTML


def createNewRowHeaderHTML(postID, dateOfPosts):
    """ Creates the HTML for the header of a row of user update panels.

    :param dateOfPost: The date of a group of user update posts (e.g., '02 August 2019')
    :returns: A string containing HTML.
    """
    innerHTML = '''
  </div> <!-- End of Panel Group -->
</div>
<div class="row">
  <h1>{date}</h1>   
  <div class="panel-group">  
    <!-- Update panel -->   
    <div class="panel panel-default" id="panel_post_{id}">
      <div>  <!-- Panel header -->'''.format(date=dateOfPosts, id=postID)
    return innerHTML


def createNewUpdatePanelHeader(postID):
    """ Creates the HTML for the header for a user update panel.

    :returns: A string containing HTML.
    """
    innerHTML = '''
    <!-- Update panel -->
    <div class="panel panel-default" id="panel_post_{id}">
       <div>  <!-- Panel header -->'''.format(id=postID)
    return innerHTML


def createDivClosingHTML():
    """ Creates the closing HTML for the content crea6ted by createInnerHTML().

    :returns: A string containing HTML.
    """
    innerHTML = '''  </div>
</div>'''
    return innerHTML