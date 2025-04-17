from django.contrib import admin
from .models import RemoteBlockedIP, SSHBruteForceConfig, SSHFailedAttempt

class RemoteBlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'duration', 'blocked_at', 'blocked_by', 'status')
    list_filter = ('is_active',)
    search_fields = ('ip_address', 'notes')
    readonly_fields = ('blocked_at',)
    fieldsets = (
        ('Informasi IP', {
            'fields': ('ip_address', 'duration', 'blocked_at')
        }),
        ('Status', {
            'fields': ('is_active', 'blocked_by', 'notes')
        }),
    )

class SSHBruteForceConfigAdmin(admin.ModelAdmin):
    list_display = ('max_retry', 'find_time', 'ban_time', 'enabled', 'last_updated', 'updated_by')
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('Parameter Keamanan', {
            'fields': ('max_retry', 'find_time', 'ban_time', 'enabled')
        }),
        ('Informasi Update', {
            'fields': ('last_updated', 'updated_by')
        }),
    )

class SSHFailedAttemptAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'username', 'attempt_count', 'last_attempt', 'is_blocked')
    list_filter = ('is_blocked',)
    search_fields = ('ip_address', 'username')
    readonly_fields = ('first_attempt', 'last_attempt', 'blocked_at')
    fieldsets = (
        ('Detail Percobaan', {
            'fields': ('ip_address', 'username', 'attempt_count')
        }),
        ('Waktu', {
            'fields': ('first_attempt', 'last_attempt')
        }),
        ('Status Blokir', {
            'fields': ('is_blocked', 'blocked_at')
        }),
    )

admin.site.register(RemoteBlockedIP, RemoteBlockedIPAdmin)
admin.site.register(SSHBruteForceConfig, SSHBruteForceConfigAdmin)
admin.site.register(SSHFailedAttempt, SSHFailedAttemptAdmin)
