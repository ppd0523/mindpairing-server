import os

from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.db import models

from common_utils import path_and_rename
from hashtag.models import Hashtag
from membership.models import User


BOARD_CATEGORY_CHOICES = (
    ('커뮤니티', '커뮤니티'),
    ('매거진', '매거진'),
)


class Board(models.Model):
    index = models.PositiveSmallIntegerField()
    # category = models.CharField(max_length=20, null=False, blank=False, choices=BOARD_CATEGORY_CHOICES)
    category = models.CharField(max_length=20, null=False, blank=False)
    hidden = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = 'board'
        verbose_name = 'board category'
        ordering = ('index', )

    def __str__(self):
        # return f"{self.get_category_display()}"
        return f"{self.category}"


class BoardHashtagAssoc(models.Model):
    board_id = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True, blank=True, db_column='board_id', related_name='hashtag_assoc_set', verbose_name='category')
    index = models.PositiveSmallIntegerField()
    hashtag_id = models.ForeignKey(Hashtag, on_delete=models.SET_NULL, null=True, blank=True, db_column='hashtag_id', related_name='board_assoc_set', verbose_name='topic')
    hidden = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = 'board_hashtag_assoc'
        verbose_name = 'board subTopic'
        ordering = ('index', )

    def __str__(self):
        return f"{self.board_id}-{self.hashtag_id}"


class ReportReason(models.Model):
    index = models.PositiveSmallIntegerField(null=False, blank=False)
    reason = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'report_reason'
        ordering = ('index', )

    def __str__(self):
        return f"{self.reason}"


REPORT_STATUS = (
    (0, 'Applied'),
    (1, 'Accepted'),
    (2, 'Rejected'),
)


class Report(models.Model):
    complainant_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='complainant_id', related_name='complainant_set')
    defendant_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='defendant_id', related_name='defendant_set')
    reason_id = models.ForeignKey(ReportReason, on_delete=models.SET_NULL, null=True, db_column='reason_id', related_name='report_set')
    status = models.PositiveSmallIntegerField(default=0, choices=REPORT_STATUS, null=False)

    comment = models.TextField(null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'report'
        ordering = ('-create_at', )

    def __str__(self):
        return f"{self.complainant_id} {self.reason_id} {self.get_status_display()}"


class Post(models.Model):
    board_id = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True, blank=True, db_column='board_id', related_name='post_set', verbose_name='board category')
    hashtag_id = models.ForeignKey(Hashtag, on_delete=models.SET_NULL, null=True, blank=True, db_column='hashtag_id', related_name='post_set', verbose_name='subTopic')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='user_id', related_name='post_set', verbose_name='Author')
    mbti = models.CharField(max_length=4, validators=[RegexValidator(regex=r"[IEx][SNx][TFx][PJx]", message='Not match MBTI characters')], null=False, blank=False, verbose_name='written by')
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False, blank=False, validators=[MinLengthValidator(5)])
    view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    report = models.PositiveIntegerField(default=0)
    hidden = models.BooleanField(default=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    reserve_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'post'
        ordering = ('-create_at', )

    def __str__(self):
        return f"#{self.id}({self.board_id}/{self.hashtag_id})"


class PostImage(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, db_column='post_id', related_name='image_set')
    image = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    alt = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'post_image'

    def __str__(self):
        return f"{self.post_id.title} {self.image}"


class PostReportAssoc(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, db_column='post_id', related_name='report_assoc_set')
    report_id = models.OneToOneField(Report, on_delete=models.SET_NULL, null=True, blank=True, db_column='report_id', related_name='post_assoc')

    class Meta:
        db_table = 'post_report_assoc'
        verbose_name = 'Report(Post)'

    def __str__(self):
        return f"{self.post_id} {self.report_id}"


class Message(models.Model):
    sender_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='sender_id', related_name='sent_msg_set')
    receiver_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='receiver_id', related_name='received_msg_set')
    text = models.TextField(null=False, blank=False, validators=[MaxLengthValidator(200)])
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    delete_at = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = 'user_message'
        verbose_name = 'User message'
        ordering = ('create_at', )

    def __str__(self):
        return f"[{self.create_at.strftime('%y%m%dT%H:%M:%S')}] {self.id} {self.sender_id} -> {self.receiver_id}: {self.text[:10]}"


class MessageReportAssoc(models.Model):
    msg_id = models.OneToOneField(Message, on_delete=models.SET_NULL, null=True, blank=True, db_column='msg_id', related_name='report_assoc')
    report_id = models.OneToOneField(Report, on_delete=models.SET_NULL, null=True, blank=True, db_column='report_id', related_name='msg_assoc')

    class Meta:
        db_table = 'message_report_assoc'
        verbose_name = 'Report(Message)'

    def __str__(self):
        return f"{self.msg_id} {self.report_id}"


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='user_id', related_name='comment_set')
    content = models.TextField(null=False, validators=[MaxLengthValidator(200)])
    like = models.PositiveIntegerField(default=0)
    report = models.PositiveIntegerField(default=0)
    hidden = models.BooleanField(default=False, null=False, blank=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    delete_at = models.DateTimeField(null=True, blank=True)
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, db_column='post_id', related_name='comment_set')
    parent_comment_id = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='parent_comment_id', related_name='parent_comment', verbose_name='parent comment')

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return f"{self.id}"


class CommentReportAssoc(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True, db_column='comment_id', related_name='report_assoc_set')
    report_id = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, blank=True, db_column='report_id', related_name='comment_assoc_set')

    class Meta:
        db_table = 'comment_report_assoc'
        verbose_name = 'Report(Comment)'

    def __str__(self):
        return f"{self.comment_id} {self.report_id}"


class Penalty(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='user_id', null=True, blank=True, related_name='penalties')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    report_id = models.OneToOneField(Report, on_delete=models.SET_NULL, db_column='report_id', null=True, blank=True, related_name='penalty')
    comment = models.TextField()
    memo = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'penalty'
        ordering = ('-update_at', '-create_at', )

    def __str__(self):
        return f"{self.user_id} ({self.start_at} - {self.end_at}) {self.report_id}"


class LikePostAssoc(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='user_id', null=True, blank=True, related_name='like_post_assoc_set')
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, db_column='post_id', related_name='like_post_assoc_set')

    class Meta:
        db_table = 'like_post_assoc'
        verbose_name = 'like post'

    def __str__(self):
        return f"{self.user_id} likes {self.post_id}"


class LikeCommentAssoc(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, db_column='user_id', null=True, blank=True, related_name='like_comment_assoc_set')
    comment_id = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True, db_column='comment_id', related_name='like_comment_assoc_set')

    class Meta:
        db_table = 'like_comment_assoc'
        verbose_name = 'like comment'

    def __str__(self):
        return f"{self.user_id} likes {self.comment_id}"
