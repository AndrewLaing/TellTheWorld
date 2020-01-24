from django.urls import path
from django.contrib.auth.views import LoginView
from tellings.views import *

app_name = 'tellings'
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('acceptableusage/', AcceptableUsagePage.as_view(), name='acceptableusage'),
    path('accountdeleted/', AccountDeletedPage.as_view(), name='accountdeleted'),
    path('addnewupdate/', AddNewUpdate.as_view(), name='addnewupdate'),
    path('addupdatemodal/', AddUpdateModal.as_view(), name='addupdatemodal'),
    path('changepassword/', ChangePasswordPage.as_view(), name='changepassword'),
    path('changeuserdetails/', ChangeUserDetailsPage.as_view(), name='changeuserdetails'),
    path('checkuserpassword/', CheckUserPassword.as_view(), name='checkuserpassword'),
    path('deleteaccountmodal/', DeleteAccountModal.as_view(), name='deleteaccountmodal'),
    path('deleteuserpost/', DeleteUserPost.as_view(), name='deleteuserpost'),
    path('edituserpost/', EditUserPost.as_view(), name='edituserpost'),
    path('edituserpost/<int:pk>', EditUserPost.as_view(), name='edituserpost'),
    path('errorpage/', ErrorPage.as_view(), name='errorpage'),
    path('haspostedtoday/', HasPostedToday.as_view(), name='haspostedtoday'),
    path('loginmodal/', LoginModal.as_view(), name='loginmodal'),
    path('loginpage/', LoginView.as_view(template_name='tellings/loginpage.html'), name='loginpage'),
    path('myupdates/', MyUpdatesListView.as_view(), name='myupdates'),
    path('newupdates/', NewUpdatesListView.as_view(), name='newupdates'),
    path('privacypolicy/', PrivacyPolicyPage.as_view(), name='privacypolicy'),
    path('signup/', SignUpPage.as_view(), name='signup'), 
    path('tags/', TagListView.as_view(), name='tags'), 
    path('termsandconditions/', TermsAndConditionsPage.as_view(), name='termsandconditions'),
    path('titleexists/', TitleExists.as_view(), name='titleexists'),
]
