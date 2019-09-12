# Filename:     createTagLinksHTML.html
# Author:       Andrew Laing
# Email:        parisianconnections@gmail.com
# Last updated: 19/08/2019.
# Description:  Contains functions used to create the content HTML
#               for tags.html.

def createInnerHTML(tagNames):
    """ Creates the content HTML for tags.html.

    :param tagNames: A list of tagnames (e.g, ['tag1','tag2'])
    :returns: A string containing HTML.
    """
    strList = []
    strList.append('<div class="row tagDetails"><br />')
    strList.append('  <div class="panel-footer">')
    headerLetter = ""

    if len(tagNames)==0:
        innerHTML = createNoResultsHTML()
    else:
        for tagName in tagNames:
            firstLetter = tagName[0]
            if firstLetter != headerLetter:
                headerLetter = firstLetter
                strList.append("<h1>" + headerLetter + "</h1>")
            strList.append(createTagLinkHTML(tagName))

        strList.append('  </div>')   
        strList.append('</div><br /><br />')
        innerHTML = ''.join(strList)
    return innerHTML

def createTagLinkHTML(tagName):
    """ Creates the HTML for a tag link.

    :param tagName: The name of a tag (e.g., 'fantastic')
    :returns: A string containing HTML.
    """
    innerHTML = '''<p>
  <a href="#" class="tagName" name="{tag}" onclick="return false;">{tag}</a>
</p>'''.format(tag=tagName)
    return innerHTML


def createNoResultsHTML():
    """ Creates the content HTML for the tag links shown on tags.html, 
        when no results are found

    :returns: A string containing HTML.
    """
    innerHTML = '''
<div class="row">
  <h1>No results found!</h1>
</div>'''
    return innerHTML