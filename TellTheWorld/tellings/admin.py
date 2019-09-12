from django.contrib import admin
from .models import Posts, Tags, Tagmap


class PostsAdmin(admin.ModelAdmin):
    fields = ['user', 'dateOfPost','postTitle','postText']


class TagsAdmin(admin.ModelAdmin):
    fields = ['tagName']


class TagmapAdmin(admin.ModelAdmin):
    fields = ['postID','tagID']
    list_display = ('postID', 'tagID')
    list_filter = ['postID', 'tagID']


admin.site.register(Posts, PostsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Tagmap, TagmapAdmin)