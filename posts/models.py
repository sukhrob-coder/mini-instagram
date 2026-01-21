import uuid

from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

from common.models import BaseModel

User = settings.AUTH_USER_MODEL


class Post(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    title = models.CharField(max_length=255, validators=[MinLengthValidator(5)])
    image = models.ImageField(upload_to="post/photos")
    content = models.TextField(validators=[MaxLengthValidator(10000)])

    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class PostComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    content = models.TextField(validators=[MaxLengthValidator(2000)])
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="child", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class PostLike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "post"], name="unique_user_post_like"
            )
        ]
        db_table = "post_likes"
        verbose_name = "Like by user"
        verbose_name_plural = "Post likes by users"


class CommentLike(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name="comment_likes"
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=["author", "comment"], name="unique_comment_likes")
        ]
        db_table = "comment_likes"
        verbose_name = "Like by user"
        verbose_name_plural = "Comment likes by users"
