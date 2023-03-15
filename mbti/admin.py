from django.contrib import admin
from .models import *


@admin.register(MBTIQuestion)
class MBTIQuestionAdmin(admin.ModelAdmin):
    list_display = ('index', 'category', 'text', 'select0_score', 'select1_score', 'select2_score', 'select3_score')
    list_display_links = ('text', )
    def short_text(self, obj: MBTIQuestion):
        return obj.text[:20]

    fieldsets = (
        (None, {
            'fields': ('index', 'category', 'text')
        }),
        ('Score', {
            # 'classes': ('extrapretty', 'thin'),
            'fields': ('select0_score', 'select1_score', 'select2_score', 'select3_score',)
        })
    )
    list_filter = ['category', ]
    ordering = ['index', ]





@admin.register(MBTITestThreshold)
class MBTITTesthreshold(admin.ModelAdmin):
    list_display = ['energy', 'information', 'decision', 'lifestyle']
    list_display_links = ['energy', 'information', 'decision', 'lifestyle']


@admin.register(MBTIClass)
class MBTITTesthresholdAdmin(admin.ModelAdmin):
    list_display = ['mbti', 'title', 'summary', 'content']


@admin.register(MBTIClassImage)
class MBTIClassImageAdmin(admin.ModelAdmin):
    list_display = ['mbti_class_id', 'name', 'image', 'alt']


@admin.register(MBTIClassHashtagAssoc)
class MBTIClassHashtagAssocAdmin(admin.ModelAdmin):
    list_display = ['mbti_class_id', 'hashtag_id']
    list_filter = ['mbti_class_id__mbti']
    search_fields = ['mbti_class_id__mbti']
