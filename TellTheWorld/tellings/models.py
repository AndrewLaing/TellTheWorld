from django.db import models
from django.conf import settings

class UserPost(models.Model):
    postID = models.AutoField(primary_key=True, db_column='postID')
    # db_column forces the use of this name (otherwise Django names it user_Id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             db_column='user')
    dateOfPost = models.DateTimeField()
    postTitle = models.CharField(max_length=35)
    postText = models.CharField(max_length=255)
    dateOfEdit = models.DateTimeField(null=True, blank=True)

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


class UserComment(models.Model):
    commentID = models.AutoField(primary_key=True, db_column='commentID')
    postID = models.ForeignKey(UserPost, on_delete=models.CASCADE, db_column='postID')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             db_column='user')
    dateOfComment = models.DateTimeField()
    commentText = models.CharField(max_length=255)
    dateOfEdit = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.commentText

    class Meta: 
        verbose_name = "UserComment"
        verbose_name_plural = "UserComments"


class DeletedAccount(models.Model):
    deleted_date = models.DateTimeField()
    deleted_reason = models.CharField(max_length=15)
    membership_length = models.PositiveIntegerField(default=0)  # in days

    class Meta: 
        verbose_name = "DeletedAccount"
        verbose_name_plural = "DeletedAccounts"


class BlockedUser(models.Model):
    blockedUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='blockeduser_blockeduser_set',
                             db_column='blockedUser')
    blockedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='blockedby_blockeduser_set',
                             db_column='blockedBy')

    def __str__(self):
        return self.blockedUser.username

    class Meta:
        verbose_name = "BlockedUser"
        verbose_name_plural = "BlockedUsers"


class HiddenPost(models.Model):
    postID = models.ForeignKey(UserPost, on_delete=models.CASCADE, db_column='postID')
    hideFrom = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             db_column='hideFrom')

    def __str__(self):
        return self.postID.postTitle

    class Meta:
        verbose_name = "HiddenPost"
        verbose_name_plural = "HiddenPosts"



