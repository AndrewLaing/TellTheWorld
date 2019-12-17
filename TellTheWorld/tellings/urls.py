from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from tellings.views import *

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
    path('deleteuserpost/', DeleteUserPost.as_view(), name='deleteuserpost'),
    path('edituserpost/', EditUserPost.as_view(), name='edituserpost'),
    path('loginmodal/', LoginModal.as_view(), name='loginmodal'),
    path('deleteaccountmodal/', DeleteAccountModal.as_view(), name='deleteaccountmodal'),
    path('addupdatemodal/', AddUpdateModal.as_view(), name='addupdatemodal'),
]
