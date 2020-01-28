from django.contrib import admin
from .models import *


class UserPostsAdmin(admin.ModelAdmin):
    fields = ['user', 'dateOfPost','postTitle','postText','isEdited', 'dateOfEdit']


class TagAdmin(admin.ModelAdmin):
    fields = ['tagName']


class TagmapAdmin(admin.ModelAdmin):
    fields = ['postID','tagID']
    list_display = ('postID', 'tagID')
    list_filter = ['postID', 'tagID']


class DeletedAccountAdmin(admin.ModelAdmin):
    fields = ['deleted_date', 'deleted_reason', 'membership_length' ] 
    list_display = ('deleted_date', 'deleted_reason', 'membership_length')
    list_filter = ['deleted_date', 'deleted_reason', 'membership_length' ]
        


admin.site.register(UserPost, UserPostsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Tagmap, TagmapAdmin)
admin.site.register(DeletedAccount, DeletedAccountAdmin)