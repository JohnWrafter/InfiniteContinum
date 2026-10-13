from django.contrib import admin

from studio.models import MemberInquiry


@admin.register(MemberInquiry)
class MemberInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "focus", "created_at")
    list_filter = ("focus", "created_at")
    search_fields = ("name", "email")
    readonly_fields = ("created_at",)