from django.db import models
from django.conf import settings

class Posts(models.Model):
    postID = models.AutoField(primary_key=True, db_column='postID')
    # db_column forces the use of this name (otherwise Django names it user_Id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             db_column='user')
    dateOfPost = models.DateField()
    postTitle = models.CharField(max_length=35)
    postText = models.CharField(max_length=255)

    def __str__(self):
        return self.postTitle

    class Meta: 
        verbose_name = "Posts"
        verbose_name_plural = "Posts"


class Tags(models.Model):
    tagID = models.AutoField(primary_key=True, db_column='tagID')
    tagName = models.CharField(max_length=15)

    def __str__(self):
        return self.tagName

    class Meta: 
        verbose_name = "Tags"
        verbose_name_plural = "Tags"


class Tagmap(models.Model):
    tagmapID = models.AutoField(primary_key=True, db_column='tagmapID')
    postID = models.ForeignKey(Posts, on_delete=models.CASCADE, db_column='postID')
    tagID = models.ForeignKey(Tags, on_delete=models.CASCADE, db_column='tagID')

    class Meta: 
        verbose_name = "Tagmap"
        verbose_name_plural = "Tagmaps"