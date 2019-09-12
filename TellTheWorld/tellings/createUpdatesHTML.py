# Filename:     createUpdatesHTML.html
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last updated: 19/08/2019.
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


def createInnerHTML(postDetails):
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
        innerHTML += createUpdateHTML(previousDate, isFirstPost, updateDetails, count)

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


def createUpdateHTML(previousDate, isFirstPost, updateDetails, count):
    """ Creates the HTML for a user update panel.

    :param previousDate: The date of the previous post (e.g., '02 August 2019')
    :param isFirstPost: True if this is the first post to be added to the HTML, otherwise false.
    :param updateDetails: A list of user update details. (e.g., [29, '02 August 2019', 'admin', 'posttitle', 'postText.'])
    :param count: A number used to make all update panels uniquely collapsable.
    :returns: A string containing HTML.
    """

    innerHTML = ''
    dateOfPost = updateDetails[1]

    if isFirstPost:
        innerHTML += createFirstRowHeaderHTML(dateOfPost)
    elif dateOfPost != previousDate:
        innerHTML += createNewRowHeaderHTML(dateOfPost)
    else:
        innerHTML += createNewUpdatePanelHeader()
            
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
    username  = sanitiseString(updateDetails[2])
    postTitle = sanitiseString(updateDetails[3])
    postText  = sanitiseString(updateDetails[4])
    innerHTML = '''
  <div class="col-sm-8 panel-postTitle">
    <p><a href="#" class="posterName" name="{user}" onclick="return false;">
    {user} says</a> ... {title}</p>
  </div>
  <div class="col-sm-4">
    <p class="align-panel-text-right">
      <a data-toggle="collapse" href="#collapse{cnt}">View Update</a>
    </p>               
  </div>         
</div> <!-- End of Panel header -->
<div id="collapse{cnt}" class="panel-collapse collapse">
  <div class="panel-body">
    <p>{text}</p>
  </div>
</div>'''.format(user=username, title=postTitle, text=postText, cnt=count)
    return innerHTML


def createFirstRowHeaderHTML(dateOfPosts):
    """ Creates the HTML for the header of the first row of user update panels.

    :param dateOfPost: The date of a group of user update posts (e.g., '02 August 2019')
    :returns: A string containing HTML.
    """
    innerHTML =  '''
<div class="row">
  <h1>{date}</h1>   
  <div class="panel-group">  
    <!-- Update panel --> 
    <div class="panel panel-default">
      <div>  <!-- Panel header -->'''.format(date=dateOfPosts)
    return innerHTML


def createNewRowHeaderHTML(dateOfPosts):
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
    <div class="panel panel-default">
      <div>  <!-- Panel header -->'''.format(date=dateOfPosts)
    return innerHTML


def createNewUpdatePanelHeader():
    """ Creates the HTML for the header for a user update panel.

    :returns: A string containing HTML.
    """
    innerHTML = '''
    <!-- Update panel -->
    <div class="panel panel-default">
       <div>  <!-- Panel header -->'''
    return innerHTML


def createDivClosingHTML():
    """ Creates the closing HTML for the content crea6ted by createInnerHTML().

    :returns: A string containing HTML.
    """
    innerHTML = '''  </div>
</div>'''
    return innerHTML