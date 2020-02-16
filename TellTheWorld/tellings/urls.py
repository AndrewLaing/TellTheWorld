from django.urls import path
from django.contrib.auth.views import LoginView
from tellings.views import *

app_name = 'tellings'
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('about/', AboutPage.as_view(), name='about'),
    path('acceptableusage/', AcceptableUsagePage.as_view(), name='acceptableusage'),
    path('accountdeleted/', AccountDeletedPage.as_view(), name='accountdeleted'),   
    path('addnewupdate/', AddNewUpdate.as_view(), name='addnewupdate'),
    path('addupdatemodal/', AddUpdateModal.as_view(), name='addupdatemodal'),
    path('addusercomment/', AddUserComment.as_view(), name='addusercomment'), 
    path('censortext/', CensorText.as_view(), name='censortext'),
    path('changepassword/', ChangePasswordPage.as_view(), name='changepassword'),
    path('changeuserdetails/', ChangeUserDetailsPage.as_view(), name='changeuserdetails'),
    path('checkuserpassword/', CheckUserPassword.as_view(), name='checkuserpassword'),
    path('deleteaccountmodal/', DeleteAccountModal.as_view(), name='deleteaccountmodal'),
    path('deleteusercomment/', DeleteUserComment.as_view(), name='deleteusercomment'),
    path('deleteuserpost/', DeleteUserPost.as_view(), name='deleteuserpost'),
    path('editusercomment/', EditUserComment.as_view(), name='editusercomment'),
    path('editusercomment/<int:pk>', EditUserComment.as_view(), name='editusercomment'),
    path('edituserpost/', EditUserPost.as_view(), name='edituserpost'),
    path('edituserpost/<int:pk>', EditUserPost.as_view(), name='edituserpost'),
    path('errorpage/', ErrorPage.as_view(), name='errorpage'),
    path('haspostedtoday/', HasPostedToday.as_view(), name='haspostedtoday'),
    path('loginmodal/', LoginModal.as_view(), name='loginmodal'),
    path('loginpage/', LoginView.as_view(template_name='tellings/loginpage.html'), name='loginpage'),
    path('missionstatement/', MissionStatementPage.as_view(), name='missionstatement'),
    path('myupdates/', MyUpdatesListView.as_view(), name='myupdates'),
    path('newupdates/', NewUpdatesListView.as_view(), name='newupdates'),
    path('privacypolicy/', PrivacyPolicyPage.as_view(), name='privacypolicy'),
    path('signup/', SignUpPage.as_view(), name='signup'), 
    path('tags/', TagListView.as_view(), name='tags'), 
    path('termsandconditions/', TermsAndConditionsPage.as_view(), name='termsandconditions'),
    path('titleexists/', TitleExists.as_view(), name='titleexists'),
    path('usercomments/', UserCommentListView.as_view(), name='usercomments'),    
]
