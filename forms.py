from django import forms
import bleach
import re

class BlockIPForm(forms.Form):
    ip_address = forms.CharField(
        label='IP Address',
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-dark-800 border border-primary-700/30 text-dark-200 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-primary-400',
            'placeholder': 'Masukkan IP address...'
        })
    )
    duration = forms.IntegerField(
        label='Durasi (jam)',
        min_value=1,
        max_value=720,  # 30 hari
        initial=24,
        widget=forms.NumberInput(attrs={
            'class': 'w-full bg-dark-800 border border-primary-700/30 text-dark-200 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-primary-400',
            'placeholder': 'Durasi dalam jam'
        })
    )

    def clean_ip_address(self):
        """Validasi dan sanitasi IP address"""
        ip = bleach.clean(self.cleaned_data['ip_address'].strip())
        
        # Validasi format IP address dengan regex
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(ip_pattern, ip):
            raise forms.ValidationError('Format IP address tidak valid')
        
        # Validasi nilai oktet
        octets = ip.split('.')
        for octet in octets:
            value = int(octet)
            if value < 0 or value > 255:
                raise forms.ValidationError('Nilai oktet IP harus antara 0-255')
                
        # Cek IP localhost dan private network
        if ip.startswith('127.') or ip.startswith('10.') or ip.startswith('192.168.') or (ip.startswith('172.') and 16 <= int(ip.split('.')[1]) <= 31):
            raise forms.ValidationError('Tidak dapat memblokir IP private network')
            
        return ip

    def clean_duration(self):
        """Validasi dan sanitasi durasi"""
        duration = self.cleaned_data['duration']
        
        # Validasi rentang nilai
        if duration < 1:
            return 1
        elif duration > 720:
            return 720
            
        return duration
        
        
# Remote SSH Protection
from .models import SSHBruteForceConfig

class SSHBruteForceConfigForm(forms.ModelForm):
    class Meta:
        model = SSHBruteForceConfig
        fields = ['max_retry', 'find_time', 'ban_time', 'enabled']
        widgets = {
            'max_retry': forms.NumberInput(attrs={
                'class': 'w-full bg-dark-800 border border-primary-700/30 text-dark-200 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-primary-400',
                'min': '1',
                'max': '100'
            }),
            'find_time': forms.NumberInput(attrs={
                'class': 'w-full bg-dark-800 border border-primary-700/30 text-dark-200 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-primary-400',
                'min': '60',
                'max': '86400',
                'step': '60'
            }),
            'ban_time': forms.NumberInput(attrs={
                'class': 'w-full bg-dark-800 border border-primary-700/30 text-dark-200 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-primary-400',
                'min': '300',
                'max': '604800',
                'step': '300'
            }),
            'enabled': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-primary-500 bg-dark-800 border-primary-700/30 rounded focus:ring-primary-400 focus:ring-2'
            })
        }
    
    def clean_max_retry(self):
        max_retry = self.cleaned_data['max_retry']
        if max_retry < 1:
            raise forms.ValidationError("Nilai minimal untuk maksimal percobaan adalah 1")
        if max_retry > 100:
            raise forms.ValidationError("Nilai maksimal untuk maksimal percobaan adalah 100")
        return max_retry
    
    def clean_find_time(self):
        find_time = self.cleaned_data['find_time']
        if find_time < 60:
            raise forms.ValidationError("Jendela waktu minimal adalah 60 detik")
        if find_time > 86400:
            raise forms.ValidationError("Jendela waktu maksimal adalah 86400 detik (24 jam)")
        return find_time
    
    def clean_ban_time(self):
        ban_time = self.cleaned_data['ban_time']
        if ban_time < 300:
            raise forms.ValidationError("Waktu blokir minimal adalah 300 detik (5 menit)")
        if ban_time > 604800:
            raise forms.ValidationError("Waktu blokir maksimal adalah 604800 detik (7 hari)")
        return ban_time
    