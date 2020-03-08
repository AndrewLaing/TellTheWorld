from django.contrib.auth.models import User
from datetime import datetime, timezone

def addUser(username, email, password):
    user=User.objects.create_user(username, email, password)
    user.is_superuser=False
    user.is_staff=False
    user.save()
    return user



user1 = addUser('jackie', 'user@test.com', '4uniquep@55w0rd')
user2 = addUser('scott', 'user@test.com', '4uniquep@55w0rd')
user3 = addUser('toxi', 'user@test.com', '4uniquep@55w0rd')
user4 = addUser('refi', 'user@test.com', '4uniquep@55w0rd')
user5 = addUser('john', 'user@test.com', '4uniquep@55w0rd')
user6 = addUser('jane', 'user@test.com', '4uniquep@55w0rd')
user7 = addUser('joe', 'user@test.com', '4uniquep@55w0rd')
user8 = addUser('justine', 'user@test.com', '4uniquep@55w0rd')
user9 = addUser('janice', 'user@test.com', '4uniquep@55w0rd')
user10 = addUser('jello', 'user@test.com', '4uniquep@55w0rd')
user11 = addUser('tody', 'user@test.com', '4uniquep@55w0rd')
user12 = addUser('tom', 'user@test.com', '4uniquep@55w0rd')
user13 = addUser('tristan', 'user@test.com', '4uniquep@55w0rd')
user14 = addUser('chloe', 'user@test.com', '4uniquep@55w0rd')
user15 = addUser('clarissa', 'user@test.com', '4uniquep@55w0rd')
user16 = addUser('chelovek', 'user@test.com', '4uniquep@55w0rd')
user17 = addUser('paula', 'user@test.com', '4uniquep@55w0rd')
user18 = addUser('pierrot', 'user@test.com', '4uniquep@55w0rd')
user19 = addUser('jeanne', 'user@test.com', '4uniquep@55w0rd')
user20 = addUser('louise', 'user@test.com', '4uniquep@55w0rd')
user21 = addUser('maribelle', 'user@test.com', '4uniquep@55w0rd')
user22 = addUser('tony', 'user@test.com', '4uniquep@55w0rd')
user23 = addUser('antonio', 'user@test.com', '4uniquep@55w0rd')
user24 = addUser('jeff', 'user@test.com', '4uniquep@55w0rd')
user25 = addUser('monica', 'user@test.com', '4uniquep@55w0rd')
user25 = addUser('angelica', 'user@test.com', '4uniquep@55w0rd')



from tellings.models import Tag

def addTag(name):
    tag = Tag(tagName=name)
    tag.save()
    return tag

    
    
tag1 = addTag('admin')
tag2 = addTag('call me jello')
tag3 = addTag('cheesy')
tag4 = addTag('common')
tag5 = addTag('coffee')
tag6 = addTag('discussion')
tag7 = addTag('edges')
tag8 = addTag('factor')
tag9 = addTag('first post')
tag10 = addTag('freegate')
tag11 = addTag('games')
tag12 = addTag('hands in da air')
tag13 = addTag('holiday')
tag14 = addTag('i was there')
tag15 = addTag('jackie')
tag16 = addTag('jane')
tag17 = addTag('janice')
tag18 = addTag('jello')
tag19 = addTag('joe')
tag20 = addTag('john')
tag21 = addTag('jquery')
tag22 = addTag('library')
tag23 = addTag('living')
tag24 = addTag('lol')
tag25 = addTag('lucky')
tag26 = addTag('mom story')
tag27 = addTag('morning')
tag28 = addTag('mycode')
tag29 = addTag('naughty')
tag30 = addTag('need suggestion')
tag31 = addTag('new')
tag32 = addTag('new features')
tag33 = addTag('newyork')
tag34 = addTag('poetry')
tag35 = addTag('post')
tag36 = addTag('refi')
tag37 = addTag('scotty')
tag38 = addTag('setsumi')
tag39 = addTag('so kawaii')
tag40 = addTag('talk')
tag41 = addTag('test')
tag42 = addTag('thanks')
tag43 = addTag('this is a test')
tag44 = addTag('toxi')
tag45 = addTag('treehouse')



from tellings.models import UserPost


def addPost(in_userID, in_dateOfPost, in_postTitle, in_postText):
    post = UserPost(user_id=in_userID, dateOfPost=in_dateOfPost, postTitle=in_postTitle, postText=in_postText)
    post.save()
    return post



post1 = addPost(user1.id, datetime(2019, 7, 18, 0,0,0).replace(tzinfo=timezone.utc), 'Merry Christmas Jackie 2019', 'I am spending Xmas at the office alone again with my computer. Send cake and coffee quickly :)')
post2 = addPost(user1.id, datetime(2019, 7, 19, 0,0,0).replace(tzinfo=timezone.utc), 'Living Snake', 'New the her nor case that lady paid read. Invitation friendship travelling eat everything the out two.')
post3 = addPost(user1.id, datetime(2019, 7, 20, 0,0,0).replace(tzinfo=timezone.utc), 'The Missing Female', 'Too cultivated use solicitude frequently. Dashwood likewise up consider continue entrance ladyship ')
post4 = addPost(user1.id, datetime(2019, 7, 24, 0,0,0).replace(tzinfo=timezone.utc), 'Truth of Secrets', 'Gay attended vicinity prepared now diverted. Esteems it ye sending reached as. Longer lively her design settle tastes advice mrs off who. ')
post5 = addPost(user5.id, datetime(2019, 7, 18, 0,0,0).replace(tzinfo=timezone.utc), 'The Births Soul', 'Prepared do an dissuade be so whatever steepest. Yet her beyond looked either day wished nay.')
post6 = addPost(user5.id, datetime(2019, 7, 19, 0,0,0).replace(tzinfo=timezone.utc), 'The Door of the Wave', 'Collected preserved are middleton dependent residence but him how. Handsome weddings yet mrs you has carriage packages. ')
post7 = addPost(user5.id, datetime(2019, 7, 24, 0,0,0).replace(tzinfo=timezone.utc), 'Moon in the Fire', 'Spot to many it four bred soon well to. Or am promotion in no departure abilities. Whatever landlord yourself at by pleasure of children be. ')
post8 = addPost(user3.id, datetime(2019, 7, 19, 0,0,0).replace(tzinfo=timezone.utc), 'Thorns of Spark', 'Amongst moments do in arrived at my replied. Fat weddings servants but man believed prospect. ')
post9 = addPost(user3.id, datetime(2019, 7, 20, 0,0,0).replace(tzinfo=timezone.utc), 'The Edge of the Son', 'Seems folly if in given scale. Sex contented dependent conveying advantage can use.')
post10 = addPost(user3.id, datetime(2019, 7, 24, 0,0,0).replace(tzinfo=timezone.utc), 'Slave of Willow', 'Pas vit bravoure trouvent une couleurs. Pourquoi collines jeunesse continue il susciter on. ')
post11 = addPost(user6.id, datetime(2019, 7, 25, 0,0,0).replace(tzinfo=timezone.utc), 'Millican', 'Just a word')
post12 = addPost(user7.id, datetime(2019, 7, 25, 0,0,0).replace(tzinfo=timezone.utc), 'Effervesent elements', 'Then there was another one just like cheese')
post13 = addPost(user8.id, datetime(2019, 7, 25, 0,0,0).replace(tzinfo=timezone.utc), 'lolalot', 'How does this work?')
post14 = addPost(user9.id, datetime(2019, 7, 25, 0,0,0).replace(tzinfo=timezone.utc), 'Hello World', 'Was this my first post')
post15 = addPost(user11.id, datetime(2019, 7, 25, 0,0,0).replace(tzinfo=timezone.utc), 'Holiday in Cambodia', 'What you guys need!')
post16 = addPost(user5.id, datetime(2019, 7, 25, 0,0,0).replace(tzinfo=timezone.utc), 'Refi in da house', 'put ur hands in the air')
post17 = addPost(user3.id, datetime(2019, 7, 28, 0,0,0).replace(tzinfo=timezone.utc), 'It was morning', 'I woke up played vidya then went to the library')
post18 = addPost(user4.id, datetime(2019, 7, 28, 0,0,0).replace(tzinfo=timezone.utc), 'This is it', 'I have removed all of the vanilla JS and replaced it with JQuery')
post19 = addPost(user3.id, datetime(2019, 7, 30,0,0, 0).replace(tzinfo=timezone.utc), 'Today I talked to Setsumi', 'Setsumi was very interested in me today, and we had a great discussion on metaphysics :)')
post20 = addPost(user4.id, datetime(2019, 7, 30,0,0, 0).replace(tzinfo=timezone.utc), 'Nice coffee', 'Three cups of coffee for my breakfast, I guess I don\'t have a power nap until tonight :P')
post21 = addPost(user5.id, datetime(2019, 7, 30,0,0, 0).replace(tzinfo=timezone.utc), 'Refi is da man', 'Hey just wanted to let you guys know that my new album is available in iTunes. So just buy it already.')
post22 = addPost(user6.id, datetime(2019, 7, 30,0,0, 0).replace(tzinfo=timezone.utc), 'john', 'lol I took another great title')
post23 = addPost(user7.id, datetime(2019, 7, 30,0,0, 0).replace(tzinfo=timezone.utc), 'Cats are so kawaii.', 'I just love cats don\'t you.\nPlease visit my site at http;//youtube.com')
post24 = addPost(user8.id, datetime(2019, 7, 30,0,0, 0).replace(tzinfo=timezone.utc), '<script>alert(\'XSStest\');</script>', 'Just testing Mr Admin. Please don\'t ban me.')
post25 = addPost(user9.id, datetime(2019, 7, 30,0,0, 0).replace(tzinfo=timezone.utc), 'I\'m a friend of Joe :P', '<script>alert(\'XSS-ed you ;P\');</script>\n<strong>Please don\'t ban me I\'m only Joe-king</strong>')
post26 = addPost(user10.id, datetime(2019,7, 30,0,0, 0).replace(tzinfo=timezone.utc), 'Naughty Joe', 'Joe has been making naughty updates. How about adding a report user functionality?')
post27 = addPost(user11.id, datetime(2019, 7, 30,0,0, 0).replace(tzinfo=timezone.utc), 'First post', 'This is my first post and ... yes my mother really did call me Jello. (Don\'t ask!)')
post28 = addPost(user1.id, datetime(2019, 7, 30,0,0,0).replace(tzinfo=timezone.utc), 'Thanks Admin', 'Thank you for resetting my password. I have been unable to login for two days now and I have so much to tell you guys ... I guess you will have to wait until tomorrow to find out :P')
post29 = addPost(user1.id, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 'Breakfast', 'Today I had cheese on toast with beans for my breakfast. It was very cheesy.')
post30 = addPost(user1.id, datetime(2019, 8, 3, 0,0,0).replace(tzinfo=timezone.utc), 'More Breakfast', 'Today I had cheese on toast with beans again for my breakfast. It was very cheesy.')



from tellings.models import Tagmap


def addTagmap(in_postID, in_tagID):
    tm = Tagmap( postID_id=in_postID, tagID_id=in_tagID)
    tm.save()

# addTagmap(post1.postID, tag1.tagID)

addTagmap(post1.postID, tag18.tagID)
addTagmap(post1.postID, tag14.tagID)
addTagmap(post2.postID, tag15.tagID)
addTagmap(post3.postID, tag16.tagID)
addTagmap(post4.postID, tag17.tagID)
addTagmap(post4.postID, tag18.tagID)
addTagmap(post4.postID, tag10.tagID)
addTagmap(post5.postID, tag12.tagID)
addTagmap(post5.postID, tag6.tagID)
addTagmap(post5.postID, tag15.tagID)
addTagmap(post6.postID, tag17.tagID)
addTagmap(post6.postID, tag19.tagID)
addTagmap(post7.postID, tag14.tagID)
addTagmap(post8.postID, tag16.tagID)
addTagmap(post8.postID, tag18.tagID)
addTagmap(post9.postID, tag13.tagID)
addTagmap(post10.postID, tag16.tagID)
addTagmap(post11.postID, tag17.tagID)
addTagmap(post11.postID, tag1.tagID)
addTagmap(post11.postID, tag10.tagID)
addTagmap(post12.postID, tag11.tagID)
addTagmap(post12.postID, tag12.tagID)
addTagmap(post13.postID, tag13.tagID)
addTagmap(post14.postID, tag11.tagID)
addTagmap(post14.postID, tag14.tagID)
addTagmap(post14.postID, tag12.tagID)
addTagmap(post15.postID, tag15.tagID)
addTagmap(post15.postID, tag16.tagID)
addTagmap(post16.postID, tag17.tagID)
addTagmap(post17.postID, tag18.tagID)
addTagmap(post18.postID, tag19.tagID)
addTagmap(post19.postID, tag20.tagID)
addTagmap(post19.postID, tag21.tagID)
addTagmap(post20.postID, tag22.tagID)
addTagmap(post20.postID, tag23.tagID)
addTagmap(post20.postID, tag24.tagID)
addTagmap(post21.postID, tag25.tagID)
addTagmap(post21.postID, tag26.tagID)
addTagmap(post21.postID, tag27.tagID)
addTagmap(post21.postID, tag28.tagID)
addTagmap(post21.postID, tag29.tagID)
addTagmap(post22.postID, tag30.tagID)
addTagmap(post22.postID, tag31.tagID)
addTagmap(post22.postID, tag32.tagID)
addTagmap(post22.postID, tag33.tagID)
addTagmap(post23.postID, tag34.tagID)
addTagmap(post23.postID, tag25.tagID)
addTagmap(post23.postID, tag35.tagID)
addTagmap(post23.postID, tag36.tagID)
addTagmap(post24.postID, tag30.tagID)
addTagmap(post24.postID, tag37.tagID)
addTagmap(post24.postID, tag38.tagID)
addTagmap(post25.postID, tag22.tagID)
addTagmap(post25.postID, tag39.tagID)
addTagmap(post25.postID, tag40.tagID)
addTagmap(post25.postID, tag41.tagID)
addTagmap(post26.postID, tag13.tagID)
addTagmap(post26.postID, tag42.tagID)
addTagmap(post26.postID, tag7.tagID)
addTagmap(post26.postID, tag15.tagID)
addTagmap(post27.postID, tag43.tagID)
addTagmap(post27.postID, tag44.tagID)
addTagmap(post27.postID, tag45.tagID)
addTagmap(post28.postID, tag2.tagID)
addTagmap(post28.postID, tag4.tagID)
addTagmap(post28.postID, tag5.tagID)
addTagmap(post29.postID, tag3.tagID)
addTagmap(post30.postID, tag3.tagID)
addTagmap(post30.postID, tag8.tagID)
addTagmap(post30.postID, tag9.tagID)



from tellings.models import UserComment


def addComment(in_postID, in_userID, in_dateOfComment, in_commentText):
    comment = UserComment(postID=in_postID, user=in_userID, 
                          dateOfComment=in_dateOfComment, 
                          commentText=in_commentText)  
    comment.save()



addComment(post1, user2, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Wonderful post.')    
addComment(post1, user3, datetime(2019, 8, 3, 0,0,0).replace(tzinfo=timezone.utc), 
           'I totes agree.')    
addComment(post2, user3, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Whut.')    
addComment(post2, user5, datetime(2019, 8, 3, 0,0,0).replace(tzinfo=timezone.utc), 
           'Me too, lololol.')    
addComment(post3, user6, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Oh wow.')    
addComment(post5, user2, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Hi mom.')    
addComment(post7, user8, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Message me.')    
addComment(post7, user11, datetime(2019, 8, 4, 0,0,0).replace(tzinfo=timezone.utc), 
           'Gimme chocolate.')    
addComment(post8, user1, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'I wanna kitty.')    
addComment(post9, user3, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Mummy I wanna kitty.')    
addComment(post10, user5, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'You are so kawaii.')    
addComment(post10, user6, datetime(2019, 8, 4, 0,0,0).replace(tzinfo=timezone.utc), 
           'Be aware.')    
addComment(post10, user3, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Trust no one.')    
addComment(post11, user12, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'No troll?')    
addComment(post12, user1, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Eat my potatoes.')    
addComment(post14, user4, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Testing 123.')    
addComment(post16, user3, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Where are the admins when you need them.')    
addComment(post17, user5, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'I wanna pony.')    
addComment(post18, user7, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'I love you.')    
addComment(post18, user5, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Swarn enemies of Voltar the Horrible, smarg smarg.')    
addComment(post18, user7, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Roll the dice.')    
addComment(post18, user8, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Nonesense comments.')    
addComment(post19, user9, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Buy one get one free.')    
addComment(post20, user1, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Is this true?')    
addComment(post21, user1, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Puppies are so qt 3.14159.')    
addComment(post23, user4, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'You are rad5.')    
addComment(post25, user6, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Beam me up.')    
addComment(post26, user3, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Sworn enemies of Golgarg the Inhaler.')    
addComment(post27, user8, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'If I was a lemon, but then again I\'m not.')    
addComment(post28, user6, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'Postie postie.')    
addComment(post29, user6, datetime(2019, 8, 2, 0,0,0).replace(tzinfo=timezone.utc), 
           'How\'s it going, bestie?')



from tellings.models import BlockedUser


def addBlockedUser(in_blockedUser, in_blockedBy):
    bu = BlockedUser(blockedUser=in_blockedUser, blockedBy=in_blockedBy)  
    bu.save()


addBlockedUser(user1, user21)
addBlockedUser(user1, user2)
addBlockedUser(user1, user7)
addBlockedUser(user1, user6)



from tellings.models import HiddenPost

def addHiddenPost(in_postID, in_hideFrom):
    hp = HiddenPost(postID=in_postID, hideFrom=in_hideFrom)  
    hp.save()


addHiddenPost(post10, user15)
addHiddenPost(post11, user15)
addHiddenPost(post14, user15)
addHiddenPost(post15, user15)
addHiddenPost(post10, user6)
addHiddenPost(post10, user9)
addHiddenPost(post10, user11)
    
    
    
    
    
    
    
    