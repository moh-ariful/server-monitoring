from django.db import models
from django.utils import timezone

class RemoteBlockedIP(models.Model):
    ip_address = models.CharField(max_length=15, verbose_name="IP Address")
    duration = models.IntegerField(verbose_name="Durasi (jam)")
    blocked_at = models.DateTimeField(default=timezone.now, verbose_name="Waktu Pemblokiran")
    blocked_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='blocked_ips',
        verbose_name="Diblokir Oleh"
    )
    is_active = models.BooleanField(default=True, verbose_name="Masih Aktif")
    notes = models.TextField(blank=True, null=True, verbose_name="Catatan")

    class Meta:
        verbose_name = "IP yang Diblokir"
        verbose_name_plural = "IP yang Diblokir"
        ordering = ['-blocked_at']

    def __str__(self):
        return self.ip_address
    
    @property
    def unblock_time(self):
        """Menghitung waktu ketika IP akan dibuka blokirnya"""
        if not self.is_active:
            return None
        return self.blocked_at + timezone.timedelta(hours=self.duration)
    
    @property
    def status(self):
        """Mengembalikan status blokir (aktif/tidak aktif)"""
        if not self.is_active:
            return "Tidak Aktif"
        
        now = timezone.now()
        unblock_time = self.unblock_time
        
        if unblock_time and now > unblock_time:
            return "Sudah Berakhir"
        
        return "Aktif"
        
        
# SSH Remote Protection
class SSHBruteForceConfig(models.Model):
    max_retry = models.IntegerField(default=5, verbose_name="Maksimal Percobaan")
    find_time = models.IntegerField(default=300, verbose_name="Jendela Waktu (detik)")
    ban_time = models.IntegerField(default=3600, verbose_name="Waktu Blokir (detik)")
    enabled = models.BooleanField(default=True, verbose_name="Status Aktif")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")
    updated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='ssh_configs',
        verbose_name="Diperbarui Oleh"
    )

    class Meta:
        verbose_name = "Konfigurasi Anti-Brute Force SSH"
        verbose_name_plural = "Konfigurasi Anti-Brute Force SSH"

    def __str__(self):
        return f"Konfigurasi Anti-Brute Force SSH (Max: {self.max_retry}, Enabled: {self.enabled})"


class SSHFailedAttempt(models.Model):
    ip_address = models.CharField(max_length=15, verbose_name="IP Address")
    username = models.CharField(max_length=100, verbose_name="Username")
    attempt_count = models.IntegerField(default=1, verbose_name="Jumlah Percobaan")
    first_attempt = models.DateTimeField(auto_now_add=True, verbose_name="Percobaan Pertama")
    last_attempt = models.DateTimeField(auto_now=True, verbose_name="Percobaan Terakhir")
    is_blocked = models.BooleanField(default=False, verbose_name="Status Blokir")
    blocked_at = models.DateTimeField(null=True, blank=True, verbose_name="Waktu Diblokir")
    
    class Meta:
        verbose_name = "Percobaan SSH Gagal"
        verbose_name_plural = "Percobaan SSH Gagal"
        unique_together = ['ip_address', 'username']
        ordering = ['-last_attempt']
        
    def __str__(self):
        return f"{self.ip_address} ({self.username}) - {self.attempt_count} percobaan"
    