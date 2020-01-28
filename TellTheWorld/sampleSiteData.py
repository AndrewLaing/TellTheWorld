from django.contrib.auth.models import User


def addUser(username, email, password):
    user=User.objects.create_user(username, email, password)
    user.is_superuser=False
    user.is_staff=False
    user.save()


addUser('jackie', 'user@test.com', '4uniquep@55w0rd')
addUser('scott', 'user@test.com', '4uniquep@55w0rd')
addUser('toxi', 'user@test.com', '4uniquep@55w0rd')
addUser('refi', 'user@test.com', '4uniquep@55w0rd')
addUser('john', 'user@test.com', '4uniquep@55w0rd')
addUser('jane', 'user@test.com', '4uniquep@55w0rd')
addUser('joe', 'user@test.com', '4uniquep@55w0rd')
addUser('justine', 'user@test.com', '4uniquep@55w0rd')
addUser('janice', 'user@test.com', '4uniquep@55w0rd')
addUser('jello', 'user@test.com', '4uniquep@55w0rd')
addUser('tody', 'user@test.com', '4uniquep@55w0rd')
addUser('tom', 'user@test.com', '4uniquep@55w0rd')
addUser('tristan', 'user@test.com', '4uniquep@55w0rd')
addUser('chloe', 'user@test.com', '4uniquep@55w0rd')
addUser('clarissa', 'user@test.com', '4uniquep@55w0rd')
addUser('chelovek', 'user@test.com', '4uniquep@55w0rd')
addUser('paula', 'user@test.com', '4uniquep@55w0rd')
addUser('pierrot', 'user@test.com', '4uniquep@55w0rd')
addUser('jeanne', 'user@test.com', '4uniquep@55w0rd')
addUser('louise', 'user@test.com', '4uniquep@55w0rd')
addUser('maribelle', 'user@test.com', '4uniquep@55w0rd')
addUser('tony', 'user@test.com', '4uniquep@55w0rd')
addUser('antonio', 'user@test.com', '4uniquep@55w0rd')
addUser('jeff', 'user@test.com', '4uniquep@55w0rd')
addUser('monica', 'user@test.com', '4uniquep@55w0rd')


from tellings.models import Tag

def addTag(name):
    tag = Tag(tagName=name)
    tag.save()
    
    
addTag('admin')
addTag('call me jello')
addTag('cheesy')
addTag('common')
addTag('coffee')
addTag('discussion')
addTag('edges')
addTag('factor')
addTag('first post')
addTag('freegate')
addTag('games')
addTag('hands in da air')
addTag('holiday')
addTag('i was there')
addTag('jackie')
addTag('jane')
addTag('janice')
addTag('jello')
addTag('joe')
addTag('john')
addTag('jquery')
addTag('library')
addTag('living')
addTag('lol')
addTag('lucky')
addTag('mom story')
addTag('morning')
addTag('mycode')
addTag('naughty')
addTag('need suggestion')
addTag('new')
addTag('new features')
addTag('newyork')
addTag('poetry')
addTag('post')
addTag('refi')
addTag('scotty')
addTag('setsumi')
addTag('so kawaii')
addTag('talk')
addTag('test')
addTag('thanks')
addTag('this is a test')
addTag('toxi')
addTag('treehouse')


from tellings.models import UserPost


def addPost(in_userID, in_dateOfPost, in_postTitle, in_postText):
    post = UserPost(user_id=in_userID, dateOfPost=in_dateOfPost, postTitle=in_postTitle, postText=in_postText)
    post.save()



addPost(1, '2019-07-18', 'Merry Christmas Jackie 2019', 'I am spending Xmas at the office alone again with my computer. Send cake and coffee quickly :)')
addPost(1, '2019-07-19', 'Living Snake', 'New the her nor case that lady paid read. Invitation friendship travelling eat everything the out two.')
addPost(1, '2019-07-20', 'The Missing Female', 'Too cultivated use solicitude frequently. Dashwood likewise up consider continue entrance ladyship ')
addPost(1, '2019-07-24', 'Truth of Secrets', 'Gay attended vicinity prepared now diverted. Esteems it ye sending reached as. Longer lively her design settle tastes advice mrs off who. ')
addPost(5, '2019-07-18', 'The Births Soul', 'Prepared do an dissuade be so whatever steepest. Yet her beyond looked either day wished nay.')
addPost(5, '2019-07-19', 'The Door of the Wave', 'Collected preserved are middleton dependent residence but him how. Handsome weddings yet mrs you has carriage packages. ')
addPost(5, '2019-07-24', 'Moon in the Fire', 'Spot to many it four bred soon well to. Or am promotion in no departure abilities. Whatever landlord yourself at by pleasure of children be. ')
addPost(3, '2019-07-19', 'Thorns of Spark', 'Amongst moments do in arrived at my replied. Fat weddings servants but man believed prospect. ')
addPost(3, '2019-07-20', 'The Edge of the Son', 'Seems folly if in given scale. Sex contented dependent conveying advantage can use.')
addPost(3, '2019-07-24', 'Slave of Willow', 'Pas vit bravoure trouvent une couleurs. Pourquoi collines jeunesse continue il susciter on. ')
addPost(6, '2019-07-25', 'Millican', 'Just a word')
addPost(7, '2019-07-25', 'Effervesent elements', 'Then there was another one just like cheese')
addPost(8, '2019-07-25', 'lolalot', 'How does this work?')
addPost(9, '2019-07-25', 'Hello World', 'Was this my first post')
addPost(11, '2019-07-25', 'Holiday in Cambodia', 'What you guys need!')
addPost(5, '2019-07-25', 'Refi in da house', 'put ur hands in the air')
addPost(3, '2019-07-28', 'It was morning', 'I woke up played vidya then went to the library')
addPost(4, '2019-07-28', 'This is it', 'I have removed all of the vanilla JS and replaced it with JQuery')
addPost(3, '2019-07-30', 'Today I talked to Setsumi', 'Setsumi was very interested in me today, and we had a great discussion on metaphysics :)')
addPost(4, '2019-07-30', 'Nice coffee', 'Three cups of coffee for my breakfast, I guess I don\'t have a power nap until tonight :P')
addPost(5, '2019-07-30', 'Refi is da man', 'Hey just wanted to let you guys know that my new album is available in iTunes. So just buy it already.')
addPost(6, '2019-07-30', 'john', 'lol I took another great title')
addPost(7, '2019-07-30', 'Cats are so kawaii.', 'I just love cats don\'t you.\nPlease visit my site at http;//youtube.com')
addPost(8, '2019-07-30', '<script>alert(\'XSStest\');</script>', 'Just testing Mr Admin. Please don\'t ban me.')
addPost(9, '2019-07-30', 'I\'m a friend of Joe :P', '<script>alert(\'XSS-ed you ;P\');</script>\n<strong>Please don\'t ban me I\'m only Joe-king</strong>')
addPost(10, '2019-07-30', 'Naughty Joe', 'Joe has been making naughty updates. How about adding a report user functionality?')
addPost(11, '2019-07-30', 'First post', 'This is my first post and ... yes my mother really did call me Jello. (Don\'t ask!)')
addPost(1, '2019-07-30', 'Thanks Admin', 'Thank you for resetting my password. I have been unable to login for two days now and I have so much to tell you guys ... I guess you will have to wait until tomorrow to find out :P')
addPost(1, '2019-08-02', 'Breakfast', 'Today I had cheese on toast with beans for my breakfast. It was very cheesy.')


from tellings.models import Tagmap


def addTagmap(in_postID, in_tagID):
    tm = Tagmap( postID_id=in_postID, tagID_id=in_tagID)
    tm.save()



addTagmap(1, 18)
addTagmap(1, 14)
addTagmap(2, 15)
addTagmap(3, 16)
addTagmap(4, 17)
addTagmap(4, 18)
addTagmap(4, 10)
addTagmap(5, 12)
addTagmap(5, 15)
addTagmap(6, 17)
addTagmap(6, 19)
addTagmap(7, 14)
addTagmap(8, 16)
addTagmap(8, 18)
addTagmap(9, 13)
addTagmap(10, 16)
addTagmap(11, 17)
addTagmap(11, 10)
addTagmap(12, 11)
addTagmap(12, 12)
addTagmap(13, 13)
addTagmap(14, 11)
addTagmap(14, 14)
addTagmap(14, 12)
addTagmap(15, 15)
addTagmap(15, 16)
addTagmap(16, 17)
addTagmap(17, 18)
addTagmap(18, 19)
addTagmap(19, 20)
addTagmap(19, 21)
addTagmap(20, 22)
addTagmap(20, 23)
addTagmap(20, 24)
addTagmap(21, 25)
addTagmap(21, 26)
addTagmap(21, 27)
addTagmap(21, 28)
addTagmap(21, 29)
addTagmap(22, 30)
addTagmap(22, 31)
addTagmap(22, 32)
addTagmap(22, 33)
addTagmap(23, 34)
addTagmap(23, 25)
addTagmap(23, 35)
addTagmap(23, 36)
addTagmap(24, 30)
addTagmap(24, 37)
addTagmap(24, 38)
addTagmap(25, 22)
addTagmap(25, 39)
addTagmap(25, 40)
addTagmap(25, 41)
addTagmap(26, 13)
addTagmap(26, 42)
addTagmap(26, 15)
addTagmap(27, 43)
addTagmap(27, 44)
addTagmap(27, 45)
addTagmap(28, 2)
addTagmap(28, 4)
addTagmap(28, 5)
addTagmap(29, 9)
addTagmap(29, 15)
addTagmap(29, 16)
addTagmap(29, 17)
