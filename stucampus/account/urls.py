from django.conf.urls import patterns, url

from stucampus.account.views import SignIn, SignOut, SignUp, Profile
from stucampus.account.views import ProfileEdit, Password

urlpatterns = patterns(
    '',
    url(r'^signup$', SignUp.as_view()),
    url(r'^signin$', SignIn.as_view()),
    url(r'^signout$', SignOut.as_view()),
    url(r'^profile$', Profile.as_view()),
    url(r'^profile/edit$', ProfileEdit.as_view()),
    url(r'^profile/password$', Password.as_view()),
)
