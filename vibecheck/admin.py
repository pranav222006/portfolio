from django.contrib import admin
from .models import FAQ, ErrorCode, SupportTicket


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'category', 'order', 'is_active', 'updated_at')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')


@admin.register(ErrorCode)
class ErrorCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'category', 'is_custom', 'created_at')
    list_filter = ('is_custom', 'category')
    search_fields = ('code', 'title', 'description', 'common_causes')


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'subject', 'user_name', 'user_email', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('ticket_id', 'subject', 'message', 'user_name', 'user_email')
    readonly_fields = ('ticket_id', 'created_at', 'updated_at')
