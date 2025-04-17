from django.urls import path
from . import views

urlpatterns = [
    path('remote/chkrootkit/', views.remote_chkrootkit, name='remote_chkrootkit'),
    path('remote/lynis/', views.remote_lynis, name='remote_lynis'),
    path('remote/ufw-status/', views.remote_ufw_status, name='remote_ufw_status'),
    path('remote/nginx-logs/', views.remote_nginx_logs, name='remote_nginx_logs'),
    path('remote/block-ip/', views.block_ip, name='block_ip'),
    path('remote/export-blocked-ips-pdf/', views.export_blocked_ips_pdf, name='export_blocked_ips_pdf'),
    path('remote/get-blocked-ips/', views.get_blocked_ips, name='get_blocked_ips'),
    # SSH Anti Brute Force
    path('remote/anti-brute-force/', views.ssh_anti_brute_force, name='ssh_anti_brute_force'),
    path('remote/ssh-log-stream/', views.ssh_log_stream, name='ssh_log_stream'),
    path('remote/update-ssh-config/', views.update_ssh_config, name='update_ssh_config'),
    path('remote/clear-attempts/', views.clear_ssh_attempts, name='clear_ssh_attempts'),
    path('remote/get-ssh-stats/', views.get_ssh_stats, name='get_ssh_stats'),
]
