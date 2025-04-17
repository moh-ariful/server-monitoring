import paramiko
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@login_required
def remote_chkrootkit(request):
    if request.method == 'POST':
        try:
            # Konfigurasi SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Koneksi ke server remote
            ssh.connect(
                'fauzanmalware.my.id',
                username='admin',
                password='xxxxxxxxxxxxx'
            )

            # Eksekusi chkrootkit
            stdin, stdout, stderr = ssh.exec_command('sudo /usr/sbin/chkrootkit')

            # Ambil output
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                return JsonResponse({'status': 'error', 'message': error})

            # Analisis dengan OpenAI menggunakan format yang benar
            analysis_prompt = f"""Analisis hasil scan Chkrootkit berikut dan berikan penjelasan dalam bahasa Indonesia yang mudah dipahami:

            {output}

            Berikan analisis dengan format:
            1. Ringkasan umum hasil scan
            2. Temuan penting (jika ada)
            3. Rekomendasi tindakan (jika diperlukan)
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "developer",
                        "content": "Anda adalah security analyst yang ahli dalam menganalisis hasil scan keamanan server. Berikan analisis yang detail namun mudah dipahami dalam bahasa Indonesia."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                temperature=0.5,
            )

            # Mengambil hasil analisis dari response dengan format yang benar
            analysis = response.choices[0].message.content

            # Generate timestamp
            tz = pytz.timezone('Asia/Jakarta')
            timestamp = datetime.now(tz).strftime("%d %B %Y %H:%M:%S WIB")

            return JsonResponse({
                'status': 'success',
                'scan_result': output,
                'analysis': analysis,
                'timestamp': timestamp
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        finally:
            if 'ssh' in locals():
                ssh.close()

    return render(request, 'remote/chkrootkit.html')


# Remote Lynis 
import paramiko
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@login_required
def remote_lynis(request):
    if request.method == 'POST':
        try:
            # Konfigurasi SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Koneksi ke server remote
            ssh.connect(
                'fauzanmalware.my.id',
                username='admin',
                password='xxxxxxxxxxxxxxxx'
            )

            # Eksekusi Lynis dengan sudo
            stdin, stdout, stderr = ssh.exec_command('sudo /usr/sbin/lynis audit system', get_pty=True)
            stdin.write('RahasiaKita2025\n')  # Input password untuk sudo
            stdin.flush()

            # Ambil output
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error and "sudo" not in error.lower():  # Ignore sudo password prompt
                return JsonResponse({'status': 'error', 'message': error})

            # Analisis dengan OpenAI
            analysis_prompt = f"""Analisis hasil audit Lynis berikut dan berikan penjelasan dalam bahasa Indonesia yang mudah dipahami:

            {output}

            Berikan analisis dengan format:
            1. Ringkasan Umum Hasil Audit
            2. Temuan Penting dan Level Risikonya
            3. Rekomendasi Perbaikan
            4. Skor Keamanan dan Interpretasinya
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "developer",
                        "content": "Anda adalah security analyst yang ahli dalam menganalisis hasil audit Lynis. Berikan analisis yang detail namun mudah dipahami dalam bahasa Indonesia."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                temperature=0.5,
            )

            # Mengambil hasil analisis
            analysis = response.choices[0].message.content

            # Generate timestamp
            tz = pytz.timezone('Asia/Jakarta')
            timestamp = datetime.now(tz).strftime("%d %B %Y %H:%M:%S WIB")

            return JsonResponse({
                'status': 'success',
                'scan_result': output,
                'analysis': analysis,
                'timestamp': timestamp
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        finally:
            if 'ssh' in locals():
                ssh.close()

    return render(request, 'remote/lynis.html')


# Remote UFW Status
import paramiko
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import pytz

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@login_required
def remote_ufw_status(request):
    if request.method == 'POST':
        try:
            # Konfigurasi SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Koneksi ke server remote
            ssh.connect(
                'fauzanmalware.my.id',
                username='admin',
                password='xxxxxxxxxxx'
            )

            # Eksekusi UFW status numbered
            stdin, stdout, stderr = ssh.exec_command('sudo /usr/sbin/ufw status numbered')

            # Ambil output
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                return JsonResponse({'status': 'error', 'message': error})

            # Analisis dengan OpenAI
            analysis_prompt = f"""Analisis hasil UFW Status berikut dan berikan penjelasan dalam bahasa Indonesia yang mudah dipahami:

            {output}

            Berikan analisis dengan format:
            1. Status UFW (aktif/nonaktif)
            2. Daftar rules yang ada
            3. Analisis keamanan dari rules yang diterapkan
            4. Rekomendasi perbaikan (jika ada)
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "developer",
                        "content": "Anda adalah security analyst yang ahli dalam menganalisis konfigurasi firewall UFW. Berikan analisis yang detail namun mudah dipahami dalam bahasa Indonesia."
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ],
                temperature=0.5,
            )

            # Mengambil hasil analisis
            analysis = response.choices[0].message.content

            # Generate timestamp
            tz = pytz.timezone('Asia/Jakarta')
            timestamp = datetime.now(tz).strftime("%d %B %Y %H:%M:%S WIB")

            return JsonResponse({
                'status': 'success',
                'scan_result': output,
                'analysis': analysis,
                'timestamp': timestamp
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        finally:
            if 'ssh' in locals():
                ssh.close()

    return render(request, 'remote/ufw_status.html')


# Remote Nginx Log 
import paramiko
import bleach 
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import BlockIPForm
import logging
from django.utils import timezone
from .models import RemoteBlockedIP
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Setup logger (pastikan sudah dikonfigurasi di settings.py)
logger = logging.getLogger('research_agent')

@login_required
def remote_nginx_logs(request):

    if request.method == 'POST':
        command = request.POST.get('command')
        ssh = None # Inisialisasi ssh ke None
        try:
            # Konfigurasi SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(
                'fauzanmalware.my.id',
                username='admin',         
                password='xxxxxxxxxxxxx',    
                timeout=30
            )

            # Jika perintah terminal dikirim
            if command:
                # Jalankan perintah tanpa menunggu input password
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()

                if error:
                    if "password is required" in error or "try again" in error:
                       return JsonResponse({'status': 'error', 'output': f"Error: Perintah '{command}' memerlukan password sudo atau konfigurasi NOPASSWD salah."})
                    return JsonResponse({'status': 'error', 'output': error})

                return JsonResponse({'status': 'success', 'output': output})

            # Jika hanya melihat log (perintah default)
            else:
                # Gunakan sudo -n dan path lengkap
                stdin_check, stdout_check, stderr_check = ssh.exec_command('ls /usr/bin/tail /var/log/nginx/access.log /var/log/nginx/error.log')
                check_error = stderr_check.read().decode()
                if "No such file or directory" in check_error:
                     return JsonResponse({'status': 'error', 'message': f"Error: File log Nginx atau perintah 'tail' tidak ditemukan di server remote. Detail: {check_error}"})

                # Ambil Access Log
                stdin_acc, stdout_acc, stderr_acc = ssh.exec_command('sudo -n /usr/bin/tail -n 100 /var/log/nginx/access.log')
                access_log = stdout_acc.read().decode()
                access_error = stderr_acc.read().decode()

                if access_error:
                    if "password is required" in access_error:
                        access_log = "Error: Tidak dapat mengakses access.log via sudo. Pastikan user 'admin' punya NOPASSWD untuk '/usr/bin/tail /var/log/nginx/access.log' di sudoers."
                    else:
                        access_log = f"Error saat membaca access.log: {access_error}"

                # Ambil Error Log
                stdin_err, stdout_err, stderr_err = ssh.exec_command('sudo -n /usr/bin/tail -n 100 /var/log/nginx/error.log')
                error_log = stdout_err.read().decode()
                error_error = stderr_err.read().decode()

                if error_error:
                     if "password is required" in error_error:
                        error_log = "Error: Tidak dapat mengakses error.log via sudo. Pastikan user 'admin' punya NOPASSWD untuk '/usr/bin/tail /var/log/nginx/error.log' di sudoers."
                     else:
                        error_log = f"Error saat membaca error.log: {error_error}"

                return JsonResponse({
                    'status': 'success',
                    'access_log': access_log,
                    'error_log': error_log
                })

        except paramiko.AuthenticationException:
            return JsonResponse({'status': 'error', 'message': 'Gagal autentikasi SSH ke server remote (user admin). Periksa username/password.'})
        except paramiko.SSHException as sshException:
            return JsonResponse({'status': 'error', 'message': f'Gagal koneksi SSH (user admin): {sshException}'})
        except Exception as e:
            logger.error(f"Error di remote_nginx_logs: {e}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': f'Terjadi kesalahan internal: {e}'})
        finally:
            if ssh:
                ssh.close()

    # Ambil 5 data terakhir IP yang diblokir
    recent_blocks = RemoteBlockedIP.objects.all()[:5]
    form = BlockIPForm()
    return render(request, 'remote/nginx_logs.html', {'form': form, 'recent_blocks': recent_blocks})


@login_required
def block_ip(request):
    if request.method == 'POST':
        form = BlockIPForm(request.POST)
        if form.is_valid():
            ip_address = form.cleaned_data['ip_address']
            duration = form.cleaned_data['duration']

            # Log tindakan
            logger.info(f"User {request.user.username} mencoba memblokir IP {ip_address} selama {duration} jam")

            ssh = None # Inisialisasi ssh ke None
            try:
                # Konfigurasi SSH
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # Koneksi ke server remote menggunakan user admin
                ssh.connect(
                    'fauzanmalware.my.id',
                    username='admin',     
                    password='xxxxxxxxxxxxxx',      
                    timeout=30
                )

                # Buat perintah UFW untuk memblokir IP (Gunakan path lengkap)
                block_command = f"sudo -n /usr/sbin/ufw deny from {ip_address} to any"
                logger.debug(f"Executing block command: {block_command}")
                stdin_block, stdout_block, stderr_block = ssh.exec_command(block_command)
                block_output = stdout_block.read().decode().strip() # Tangkap output sukses juga
                block_error = stderr_block.read().decode().strip()

                if block_error:
                    logger.error(f"Error saat menjalankan block command '{block_command}': {block_error}")
                    if "password is required" in block_error:
                        return JsonResponse({
                            'status': 'error',
                            'message': "Error: Gagal menjalankan ufw deny. Pastikan user 'admin' punya NOPASSWD untuk '/usr/sbin/ufw' di sudoers."
                        })
                    elif "ERROR: Bad source address" in block_error:
                         return JsonResponse({
                            'status': 'error',
                            'message': f"Error UFW: Format IP address '{ip_address}' ditolak oleh UFW."
                        })
                    # Tangani kemungkinan error rule sudah ada (mungkin tidak perlu dianggap error fatal)
                    elif "Skipping adding existing rule" in block_output or "Rule already exists" in block_error:
                         logger.warning(f"UFW rule for IP {ip_address} already exists. Block command output: {block_output}, error: {block_error}")
                         # Lanjutkan ke penjadwalan unblock jika rule sudah ada
                    else:
                        return JsonResponse({
                            'status': 'error',
                            'message': f'Gagal memblokir IP (UFW Error): {block_error}'
                        })
                else:
                    logger.info(f"Block command successful. Output: {block_output}")

                # Jadwalkan penghapusan aturan setelah durasi tertentu
                unblock_scheduled = False
                at_error_message = None
                if duration > 0:
                    try:
                        unblock_time = f"now + {duration} hours"
                        # Perintah echo dengan path lengkap untuk sudo dan ufw, di-pipe ke at (path lengkap juga)
                        unblock_command = f"echo '/usr/bin/sudo /usr/sbin/ufw delete deny from {ip_address} to any' | /usr/bin/at {unblock_time}"
                        logger.debug(f"Executing unblock schedule command: {unblock_command}")

                        stdin_at, stdout_at, stderr_at = ssh.exec_command(unblock_command)
                        # Baca output dan error, hilangkan spasi di awal/akhir
                        at_output = stdout_at.read().decode().strip()
                        at_error = stderr_at.read().decode().strip()

                        # --- Logika pengecekan error 'at' yang sudah diperbaiki ---
                        scheduling_failed = False
                        known_warning = "warning: commands will be executed using /bin/sh" # Peringatan yg diketahui

                        if at_error:
                            # Cek apakah pesan di stderr HANYA berisi (atau dimulai dengan) peringatan yang kita kenal
                            if at_error.startswith(known_warning):
                                # Jika ya, ini bukan error fatal, hanya peringatan. Log saja.
                                logger.warning(f"Penjadwalan 'at' berhasil dengan peringatan: {at_error}")
                                # Tetap anggap berhasil (unblock_scheduled akan jadi True nanti)
                            else:
                                # Jika stderr berisi sesuatu SELAIN peringatan itu, anggap error.
                                logger.error(f"Gagal menjadwalkan unblock via 'at' (stderr): {at_error}")
                                # Siapkan pesan error untuk ditampilkan ke user
                                at_error_message = f"IP berhasil diblokir, TAPI gagal menjadwalkan unblock otomatis ({at_error}). Periksa service 'atd' dan izin 'at'."
                                scheduling_failed = True # Tandai sebagai gagal
                        # --- Akhir logika pengecekan error 'at' ---

                        # Set status penjadwalan berdasarkan flag scheduling_failed
                        if not scheduling_failed:
                            logger.info(f"Unblock command scheduled via 'at'. Output stdout: {at_output}")
                            unblock_scheduled = True
                            at_error_message = None # Pastikan pesan error kosong jika sukses
                        else:
                            unblock_scheduled = False
                            # at_error_message sudah diatur di atas jika scheduling_failed = True

                    except Exception as e_at:
                         logger.error(f"Exception saat mencoba menjadwalkan unblock via 'at': {e_at}", exc_info=True)
                         at_error_message = f"IP berhasil diblokir, TAPI terjadi exception saat mencoba menjadwalkan unblock otomatis: {e_at}. Periksa log aplikasi."
                         unblock_scheduled = False # Gagal karena exception

                # Simpan data ke database
                blocked_ip = RemoteBlockedIP(
                    ip_address=ip_address,
                    duration=duration,
                    blocked_by=request.user,
                    notes=f"Diblokir melalui Remote Nginx Log Monitor. Unblock otomatis: {'Ya' if unblock_scheduled else 'Tidak'}"
                )
                blocked_ip.save()
                logger.info(f"IP {ip_address} berhasil disimpan ke database dengan ID {blocked_ip.id}")

                # Susun pesan sukses akhir
                success_message = f'IP {ip_address} berhasil diblokir dan disimpan ke database.'
                if duration > 0:
                    if unblock_scheduled:
                         success_message += f' Unblock otomatis dijadwalkan dalam {duration} jam.'
                    else:
                        # Jika penjadwalan gagal (baik karena error 'at' maupun exception)
                        # Pastikan at_error_message punya nilai default jika belum diset
                        if not at_error_message:
                           at_error_message = "Gagal menjadwalkan unblock otomatis karena alasan tidak diketahui. Periksa log."
                        success_message += f' Durasi: {duration} jam. PERINGATAN: {at_error_message}'
                else:
                     # Jika durasi tidak valid atau 0 (meskipun form harusnya mencegah < 1)
                     success_message += ' (Durasi tidak ditentukan atau tidak valid, pemblokiran mungkin permanen).'

                # Ambil data terbaru untuk dikirim ke frontend
                recent_blocks_data = list(RemoteBlockedIP.objects.values('ip_address', 'duration', 'blocked_at')[:5])
                # Format tanggal untuk JSON
                for block in recent_blocks_data:
                    block['blocked_at'] = block['blocked_at'].strftime('%Y-%m-%d %H:%M:%S')

                return JsonResponse({
                    'status': 'success',
                    'message': success_message,
                    'recent_blocks': recent_blocks_data
                })

            except paramiko.AuthenticationException:
                 logger.error("Gagal autentikasi SSH ke server remote (user admin).")
                 return JsonResponse({'status': 'error', 'message': 'Gagal autentikasi SSH ke server remote (user admin). Periksa username/password.'})
            except paramiko.SSHException as sshException:
                 logger.error(f"Gagal koneksi SSH (user admin): {sshException}")
                 return JsonResponse({'status': 'error', 'message': f'Gagal koneksi SSH (user admin): {sshException}'})
            except Exception as e:
                logger.error(f"Error saat memblokir IP {ip_address}: {str(e)}", exc_info=True)
                return JsonResponse({
                    'status': 'error',
                    'message': f'Gagal memblokir IP: Terjadi kesalahan internal server ({type(e).__name__}). Periksa log.'
                })
            finally:
                if ssh:
                    ssh.close()
        else:
            # Form tidak valid
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]

            logger.warning(f"Form block IP tidak valid: {errors}")
            return JsonResponse({
                'status': 'error',
                'message': 'Input tidak valid. Periksa kembali IP address dan durasi.', # Pesan generik
                'errors': errors 
            }, status=400) 

    return redirect('remote_nginx_logs')


@login_required
def export_blocked_ips_pdf(request):
    """Generate PDF dari IP yang diblokir"""
    # Ambil semua IP yang diblokir
    blocked_ips = RemoteBlockedIP.objects.all().order_by('-blocked_at')
    
    # Buat buffer untuk menyimpan PDF
    buffer = BytesIO()
    
    # Buat dokumen PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Judul
    elements.append(Paragraph("Laporan IP yang Diblokir", title_style))
    elements.append(Paragraph(f"Dibuat pada: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", subtitle_style))
    elements.append(Paragraph(f"Total IP: {blocked_ips.count()}", normal_style))
    elements.append(Paragraph(" ", normal_style))  # Spasi
    
    # Buat data tabel
    data = [['No', 'IP Address', 'Durasi (jam)', 'Waktu Blokir', 'Diblokir Oleh', 'Status']]
    
    for i, ip in enumerate(blocked_ips, 1):
        blocked_at = ip.blocked_at.strftime('%d-%m-%Y %H:%M')
        blocked_by = ip.blocked_by.username if ip.blocked_by else 'System'
        
        data.append([
            str(i),
            ip.ip_address,
            str(ip.duration),
            blocked_at,
            blocked_by,
            ip.status
        ])
    
    # Buat tabel
    table = Table(data, repeatRows=1)
    
    # Style tabel
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.skyblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    
    # Footer
    elements.append(Paragraph(" ", normal_style))  # Spasi
    elements.append(Paragraph("Laporan ini dibuat secara otomatis oleh XyberXecurity Lab Remote Monitoring System.", normal_style))
    
    # Build PDF
    doc.build(elements)
    
    # Siapkan respon
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="blocked_ips_report.pdf"'
    
    return response


@login_required
def get_blocked_ips(request):
    """API untuk mendapatkan data IP yang diblokir"""
    blocked_ips = RemoteBlockedIP.objects.all().order_by('-blocked_at')
    
    data = []
    for ip in blocked_ips:
        data.append({
            'id': ip.id,
            'ip_address': ip.ip_address,
            'duration': ip.duration,
            'blocked_at': ip.blocked_at.strftime('%Y-%m-%d %H:%M:%S'),
            'blocked_by': ip.blocked_by.username if ip.blocked_by else 'System',
            'is_active': ip.is_active,
            'status': ip.status,
            'notes': ip.notes,
        })
    
    return JsonResponse({'status': 'success', 'data': data})


# SSH Remote Protection
from datetime import datetime, timedelta
from django.http import StreamingHttpResponse
import bleach
import time
from django.utils import timezone
current_time = timezone.now()
import json
import re
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Count, Q
from .models import SSHBruteForceConfig, SSHFailedAttempt
from .forms import SSHBruteForceConfigForm

@login_required
def ssh_anti_brute_force(request):
    """Halaman utama Anti-Brute Force SSH"""
    # Ambil atau buat konfigurasi
    config, created = SSHBruteForceConfig.objects.get_or_create(
        pk=1,
        defaults={
            'max_retry': 5,
            'find_time': 300,
            'ban_time': 3600,
            'enabled': True,
            'updated_by': request.user
        }
    )
    
    # Form konfigurasi
    config_form = SSHBruteForceConfigForm(instance=config)
    
    # Statistik percobaan
    total_attempts = SSHFailedAttempt.objects.count()
    unique_ips = SSHFailedAttempt.objects.values('ip_address').distinct().count()
    blocked_ips = SSHFailedAttempt.objects.filter(is_blocked=True).count()
    
    # Riwayat percobaan (100 terakhir)
    attempts = SSHFailedAttempt.objects.all()[:100]
    
    context = {
        'config': config,
        'config_form': config_form,
        'stats': {
            'total_attempts': total_attempts,
            'unique_ips': unique_ips,
            'blocked_ips': blocked_ips
        },
        'attempts': attempts
    }
    
    return render(request, 'remote/ssh_anti_brute_force.html', context)

@login_required
def ssh_log_stream(request):
    """Streaming log file SSH secara real-time"""
    def event_stream():
        ssh = None
        try:
            # Konfigurasi SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                'fauzanmalware.my.id',
                username='admin',
                password='xxxxxxxxxxxx',
                timeout=30
            )
            
            # Jalankan tail -f untuk memantau auth.log
            stdin, stdout, stderr = ssh.exec_command('sudo -n /usr/bin/tail -f /var/log/auth.log')
            
            # Parse dan kirim log line by line
            for line in stdout:
                # Sanitasi output untuk keamanan
                line = bleach.clean(line.strip())
                
                # Deteksi pola login gagal
                is_failed_login = False
                if "Failed password" in line or "authentication failure" in line:
                    is_failed_login = True
                    line_class = "text-red-400"
                elif "Accepted password" in line:
                    line_class = "text-green-400"
                else:
                    line_class = "text-gray-400"
                
                # Format untuk event-stream
                data = {
                    'line': line,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'class': line_class,
                    'is_failed_login': is_failed_login
                }
                
                yield f"data: {json.dumps(data)}\n\n"
                time.sleep(0.1)  # Kecilkan beban
                
        except Exception as e:
            logger.error(f"Error streaming SSH log: {e}", exc_info=True)
            data = {
                'line': f"Error: {str(e)}",
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'class': "text-red-600",
                'is_failed_login': False
            }
            yield f"data: {json.dumps(data)}\n\n"
        finally:
            if ssh:
                ssh.close()
    
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

@login_required
@csrf_exempt
def update_ssh_config(request):
    """Update konfigurasi Anti-Brute Force SSH"""
    if request.method == 'POST':
        # Ambil konfigurasi yang ada atau buat baru
        config, created = SSHBruteForceConfig.objects.get_or_create(pk=1)
        
        # Update dengan data form
        form = SSHBruteForceConfigForm(request.POST, instance=config)
        
        if form.is_valid():
            config = form.save(commit=False)
            config.updated_by = request.user
            config.save()
            
            logger.info(f"User {request.user.username} memperbarui konfigurasi Anti-Brute Force SSH")
            
            return JsonResponse({
                'status': 'success',
                'message': 'Konfigurasi berhasil diperbarui'
            })
        else:
            # Form tidak valid
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [str(error) for error in error_list]
            
            logger.warning(f"Form konfigurasi SSH tidak valid: {errors}")
            
            return JsonResponse({
                'status': 'error',
                'message': 'Input tidak valid. Periksa kembali nilai parameter.',
                'errors': errors
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, status=405)

@login_required
def clear_ssh_attempts(request):
    """Hapus semua riwayat percobaan SSH gagal"""
    if request.method == 'POST':
        count = SSHFailedAttempt.objects.count()
        SSHFailedAttempt.objects.all().delete()
        
        logger.info(f"User {request.user.username} menghapus {count} riwayat percobaan SSH gagal")
        
        return JsonResponse({
            'status': 'success',
            'message': f'Berhasil menghapus {count} riwayat percobaan'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan'}, status=405)

@login_required
def get_ssh_stats(request):
    """API untuk mendapatkan statistik terbaru"""
    # Statistik dasar
    total_attempts = SSHFailedAttempt.objects.count()
    unique_ips = SSHFailedAttempt.objects.values('ip_address').distinct().count()
    blocked_ips = SSHFailedAttempt.objects.filter(is_blocked=True).count()
    
    # Top 5 IP dengan percobaan terbanyak
    top_ips = SSHFailedAttempt.objects.values('ip_address').annotate(
        total=Count('ip_address')
    ).order_by('-total')[:5]
    
    # Top 5 username yang paling sering dicoba
    top_usernames = SSHFailedAttempt.objects.values('username').annotate(
        total=Count('username')
    ).order_by('-total')[:5]
    
    # Percobaan dalam 24 jam terakhir
    day_ago = timezone.now() - timedelta(days=1)
    attempts_24h = SSHFailedAttempt.objects.filter(last_attempt__gte=day_ago).count()
    
    # Buat data untuk grafik (per jam)
    hourly_data = []
    for i in range(24):
        hour_start = timezone.now() - timedelta(hours=24-i)
        hour_end = timezone.now() - timedelta(hours=23-i)
        count = SSHFailedAttempt.objects.filter(
            last_attempt__gte=hour_start,
            last_attempt__lt=hour_end
        ).count()
        hourly_data.append({
            'hour': hour_start.strftime('%H:00'),
            'count': count
        })
    
    return JsonResponse({
        'status': 'success',
        'stats': {
            'total_attempts': total_attempts,
            'unique_ips': unique_ips,
            'blocked_ips': blocked_ips,
            'attempts_24h': attempts_24h,
            'top_ips': list(top_ips),
            'top_usernames': list(top_usernames),
            'hourly_data': hourly_data
        }
    })

# Fungsi bantuan untuk menjalankan tugas pemantauan SSH
def monitor_ssh_brute_force():
    """
    Fungsi bantuan untuk memantau percobaan bruteforce SSH
    Fungsi ini dijalankan oleh task scheduler di background
    """
    # Ambil konfigurasi
    try:
        config = SSHBruteForceConfig.objects.get(pk=1)
        if not config.enabled:
            logger.info("Monitor SSH brute force dinonaktifkan dalam konfigurasi")
            return
    except SSHBruteForceConfig.DoesNotExist:
        logger.error("Konfigurasi SSH brute force tidak ditemukan, menggunakan nilai default")
        config = SSHBruteForceConfig(
            max_retry=5,
            find_time=300,
            ban_time=3600,
            enabled=True
        )
    
    ssh = None
    try:
        # Konfigurasi SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(
            'fauzanmalware.my.id',
            username='admin',
            password='xxxxxxxxxx',
            timeout=30
        )
        
        # Ambil log auth.log
        stdin, stdout, stderr = ssh.exec_command('sudo -n /usr/bin/tail -n 1000 /var/log/auth.log')
        log_content = stdout.read().decode()
        
        # Pattern untuk deteksi login gagal
        failed_pattern = r'Failed password for (\S+) from (\d+\.\d+\.\d+\.\d+)'
        
        # Parse log
        matches = re.findall(failed_pattern, log_content)
        
        # Waktu threshold berdasarkan find_time
        threshold_time = datetime.now() - timedelta(seconds=config.find_time)
        
        # Proses setiap login gagal
        for username, ip_address in matches:
            # Sanitasi input
            username = bleach.clean(username)
            ip_address = bleach.clean(ip_address)
            
            # Cari atau buat record percobaan
            attempt, created = SSHFailedAttempt.objects.get_or_create(
                ip_address=ip_address,
                username=username,
                defaults={
                    'attempt_count': 1,
                    'is_blocked': False
                }
            )
            
            # Jika sudah ada, update counter
            if not created:
                # Reset counter jika di luar jendela waktu
                if attempt.last_attempt < threshold_time:
                    attempt.attempt_count = 1
                else:
                    attempt.attempt_count += 1
                attempt.save()
            
            # Cek apakah perlu diblokir
            if attempt.attempt_count >= config.max_retry and not attempt.is_blocked:
                # Blokir IP
                block_ssh_ip(ssh, ip_address, config.ban_time)
                
                # Update status
                attempt.is_blocked = True
                attempt.blocked_at = datetime.now()
                attempt.save()
                
                logger.warning(f"IP {ip_address} diblokir setelah {attempt.attempt_count} percobaan login sebagai {username}")
        
    except Exception as e:
        logger.error(f"Error memantau brute force SSH: {e}", exc_info=True)
    finally:
        if ssh:
            ssh.close()

def block_ssh_ip(ssh_client, ip_address, ban_time):
    """Helper function untuk memblokir IP via SSH"""
    try:
        # Buat perintah UFW untuk memblokir IP
        block_command = f"sudo -n /usr/sbin/ufw deny from {ip_address} to any"
        stdin_block, stdout_block, stderr_block = ssh_client.exec_command(block_command)
        block_error = stderr_block.read().decode().strip()
        
        if block_error and "Skipping adding existing rule" not in block_error and "Rule already exists" not in block_error:
            logger.error(f"Error saat memblokir IP {ip_address}: {block_error}")
            return False
        
        # Jadwalkan penghapusan aturan
        if ban_time > 0:
            unblock_time = f"now + {ban_time} seconds"
            unblock_command = f"echo '/usr/bin/sudo /usr/sbin/ufw delete deny from {ip_address} to any' | /usr/bin/at {unblock_time}"
            
            stdin_at, stdout_at, stderr_at = ssh_client.exec_command(unblock_command)
            at_error = stderr_at.read().decode().strip()
            
            if at_error and "warning: commands will be executed using /bin/sh" not in at_error:
                logger.error(f"Error saat menjadwalkan unblock untuk IP {ip_address}: {at_error}")
        
        return True
        
    except Exception as e:
        logger.error(f"Exception saat memblokir IP {ip_address}: {e}", exc_info=True)
        return False
