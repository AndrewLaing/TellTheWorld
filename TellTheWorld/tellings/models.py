from django.db import models
from django.conf import settings

class UserPost(models.Model):
    postID = models.AutoField(primary_key=True, db_column='postID')
    # db_column forces the use of this name (otherwise Django names it user_Id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             db_column='user')
    dateOfPost = models.DateField()
    postTitle = models.CharField(max_length=35, unique=True)
    postText = models.CharField(max_length=255)
    dateOfEdit = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.postTitle

    @property
    def post_tags(self):
        "Returns a list of tagNames attached to the UserPost object."
        tagmaps = Tagmap.objects.filter(postID=self.postID)
        tagList = sorted([tag.tagID.tagName for tag in tagmaps])
        return tagList

    class Meta: 
        verbose_name = "UserPost"
        verbose_name_plural = "UserPosts"


class Tag(models.Model):
    tagID = models.AutoField(primary_key=True, db_column='tagID')
    tagName = models.CharField(max_length=15)

    def __str__(self):
        return self.tagName

    @property
    def first_char(self):
        "Returns the first character of the tag. Used for grouping in the listview"
        return self.tagName[0]

    class Meta: 
        ordering = ['tagName']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Tagmap(models.Model):
    tagmapID = models.AutoField(primary_key=True, db_column='tagmapID')
    postID = models.ForeignKey(UserPost, on_delete=models.CASCADE, db_column='postID')
    tagID = models.ForeignKey(Tag, on_delete=models.CASCADE, db_column='tagID')

    class Meta: 
        verbose_name = "Tagmap"
        verbose_name_plural = "Tagmaps"


class DeletedAccount(models.Model):
    deleted_date = models.DateField()
    deleted_reason = models.CharField(max_length=15)
    membership_length = models.PositiveIntegerField(default=0)  # in days

    class Meta: 
        verbose_name = "DeletedAccount"
        verbose_name_plural = "DeletedAccounts"
        
