from django.contrib import admin

from config import settings
from .models import *


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['index', 'category', 'hidden']
    list_display_links = ['category']
    ordering = ['index', ]


@admin.register(BoardHashtagAssoc)
class BoardHashtagAssocAdmin(admin.ModelAdmin):
    # board subtopic
    list_display = ['board_id', 'index', 'hashtag_id', 'hidden']
    ordering = ['board_id', 'index', ]

@admin.register(ReportReason)
class ReportReasonAdmin(admin.ModelAdmin):
    list_display = ['index', 'reason']
    list_display_links = ['reason']
    ordering = ('index', )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['create_at', 'complainant_id', 'defendant_id', 'reason_id', 'comment', 'status']
    list_display_links = ['comment']
    search_fields = ['complainant_id', 'defendant_id', 'status']
    list_filter = ['status']
    ordering = ['-create_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'board_id', 'hashtag_id', 'mbti', 'user_id', 'short_title', 'short_content', 'view', 'like', 'report', 'formed_create_at']
    list_display_links = ['short_title', 'short_content']
    search_fields = ['title', 'content', 'user_id']
    list_filter = ['board_id', 'mbti']
    ordering = ['-create_at']

    def formed_create_at(self, obj: Post):
        return obj.create_at.strftime(settings.DATETIME_FORMAT2)

    def short_title(self, obj: Post):
        return obj.title[:5]

    def short_content(self, obj: Post):
        return obj.content[:10]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'image', 'name', 'alt']
    list_display_links = ['image']
    search_fields = ['post_id', 'alt']


@admin.register(PostReportAssoc)
class PostReportAssocAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'report_id']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender_id', 'receiver_id', 'text']
    ordering = ['-create_at']


@admin.register(MessageReportAssoc)
class MessageReportAssocAdmin(admin.ModelAdmin):
    list_display = ['report_id', 'msg_id']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'parent_comment_id', 'user_id', 'content', 'like', 'formed_create_at']
    list_display_links = ['content']
    readonly_fields = ['like', 'report']
    search_fields = ['post_id', 'user_id', 'content']

    def formed_create_at(self, obj: Post):
        return obj.create_at.strftime(settings.DATETIME_FORMAT2)


@admin.register(CommentReportAssoc)
class CommentReportAssocAdmin(admin.ModelAdmin):
    list_display = ['comment_id', 'report_id']


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'report_id', 'formed_start_at', 'formed_end_at', 'comment']

    def formed_start_at(self, obj: Post):
        return obj.create_at.strftime(settings.DATETIME_FORMAT2)

    def formed_end_at(self, obj: Post):
        return obj.create_at.strftime(settings.DATETIME_FORMAT2)


@admin.register(LikePostAssoc)
class LikePostAssocAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'post_id']


@admin.register(LikeCommentAssoc)
class LikeCommentAssocAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'comment_id']
