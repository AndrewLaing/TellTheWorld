from django.contrib import admin
from .models import *


class UserPostsAdmin(admin.ModelAdmin):
    fields = ['user', 'dateOfPost','postTitle','postText', 'dateOfEdit']


class TagAdmin(admin.ModelAdmin):
    fields = ['tagName']


class TagmapAdmin(admin.ModelAdmin):
    fields = ['postID','tagID']
    list_display = ('postID', 'tagID')


class UserCommentAdmin(admin.ModelAdmin):
    fields = ['postID', 'user', 'dateOfComment', 'dateOfEdit', 'commentText'] 
    list_display = ('postID', 'user', 'dateOfComment', 'dateOfEdit', 'commentText')


class DeletedAccountAdmin(admin.ModelAdmin):
    fields = ['deleted_date', 'deleted_reason', 'membership_length' ] 
    list_display = ('deleted_date', 'deleted_reason', 'membership_length')
    list_filter = ['deleted_date', 'deleted_reason', 'membership_length' ]


class HiddenPostAdmin(admin.ModelAdmin):
    fields = ['postID', 'hideFrom']
    list_display = ('postID', 'hideFrom')

class BlockedUserAdmin(admin.ModelAdmin):
    fields = ['blockedUser', 'blockedBy']
    list_display = ('blockedUser', 'blockedBy')


admin.site.register(UserPost, UserPostsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Tagmap, TagmapAdmin)
admin.site.register(UserComment, UserCommentAdmin)
admin.site.register(DeletedAccount, DeletedAccountAdmin)
admin.site.register(HiddenPost, HiddenPostAdmin)
admin.site.register(BlockedUser, BlockedUserAdmin)



