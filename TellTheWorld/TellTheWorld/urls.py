# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('tellings.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls)
]
