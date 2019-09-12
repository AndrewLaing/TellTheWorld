from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from tellings.views import IndexPage, TagsPage, MyUpdatesPage, NewUpdatesPage, ErrorPage, AccountDeletedPage
from tellings.views import SignUpPage, ChangePasswordPage, ChangeUserDetailsPage
from tellings.views import HasPostedToday, TitleExists, AddNewUpdate, AddUpdatesForTag
from tellings.views import AddUpdatesForTagByLoggedInUser, AddUpdatesForUsername, CheckUserPassword

app_name = 'tellings'
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('newupdates/', NewUpdatesPage.as_view(), name='newupdates'),
    path('tags/', TagsPage.as_view(), name='tags'),
    path('myupdates/', MyUpdatesPage.as_view(), name='myupdates'),
    path('errorpage/', ErrorPage.as_view(), name='errorpage'),
    path('accountdeleted/', AccountDeletedPage.as_view(), name='accountdeleted'),
    path('haspostedtoday/', HasPostedToday.as_view(), name='haspostedtoday'),
    path('titleexists/', TitleExists.as_view(), name='titleexists'),
    path('addnewupdate/', AddNewUpdate.as_view(), name='addnewupdate'),
    path('addupdatesfortag/', AddUpdatesForTag.as_view(), name='addupdatesfortag'),
    path('addupdatesfortagbyloggedinuser/', AddUpdatesForTagByLoggedInUser.as_view(), name='addupdatesfortagbyloggedinuser'),
    path('addupdatesforusername/', AddUpdatesForUsername.as_view(), name='addupdatesforusername'),
    path('signup/', SignUpPage.as_view(), name='signup'),
    path('changepassword/', ChangePasswordPage.as_view(), name='changepassword'),
    path('changeuserdetails/', ChangeUserDetailsPage.as_view(), name='changeuserdetails'),
    path('checkuserpassword/', CheckUserPassword.as_view(), name='checkuserpassword'),
    path('loginpage/', LoginView.as_view(template_name='tellings/loginpage.html'), name='loginpage'),
]
