from django.contrib import admin
from django.contrib.admin import ModelAdmin

from poll.models import Choice, Poll, Vote


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_filter = ("author",)
    date_hierarchy = "published"


class VoteAdmin(ModelAdmin):
    list_filter = ("voted_by",)
    date_hierarchy = "voted_at"


admin.site.register(Vote, VoteAdmin)
admin.site.register(Choice)
