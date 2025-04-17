import subprocess
import logging
import os
from threading import Timer

logger = logging.getLogger(__name__)

class UFWManager:
    UFW_PATH = '/usr/sbin/ufw'
    SUDO_PATH = '/usr/bin/sudo'
    TIMEOUT = 10  # Menambah timeout menjadi 10 detik

    @classmethod
    def block_ip(cls, ip_address):
        try:
            logger.info(f"Mencoba memblokir IP {ip_address}")

            # Pastikan path executable ada
            if not os.path.exists(cls.UFW_PATH) or not os.path.exists(cls.SUDO_PATH):
                logger.error("UFW atau sudo tidak ditemukan")
                return False, "UFW atau sudo tidak ditemukan"

            # Cek apakah IP sudah diblokir
            check_cmd = [cls.SUDO_PATH, cls.UFW_PATH, 'status', 'numbered']
            check_result = subprocess.run(
                check_cmd,
                capture_output=True,
                text=True,
                timeout=cls.TIMEOUT
            )
            
            if ip_address in check_result.stdout:
                return False, f"IP {ip_address} sudah diblokir sebelumnya"

            # Blokir untuk seluruh traffic dari IP tersebut
            cmd = [cls.SUDO_PATH, cls.UFW_PATH, 'insert', '1', 'deny', 'from', ip_address, 'to', 'any']

            # Jalankan command dengan timeout yang lebih lama
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=cls.TIMEOUT
            )

            # Verifikasi hasil
            if result.returncode == 0:
                # Reload UFW untuk memastikan perubahan diterapkan
                reload_cmd = [cls.SUDO_PATH, cls.UFW_PATH, 'reload']
                subprocess.run(reload_cmd, timeout=cls.TIMEOUT)
                
                logger.info(f"Berhasil memblokir IP {ip_address}")
                return True, "Success"
            else:
                error_msg = result.stderr or "Unknown error occurred"
                logger.error(f"UFW command failed: {error_msg}")
                return False, f"UFW command failed: {error_msg}"

        except subprocess.TimeoutExpired:
            error_msg = f"Timeout saat memblokir IP {ip_address} (lebih dari {cls.TIMEOUT} detik)"
            logger.error(error_msg)
            return False, error_msg
        except subprocess.CalledProcessError as e:
            error_msg = f"Error blocking IP {ip_address}: {e.stderr if e.stderr else str(e)}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error blocking IP {ip_address}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    @classmethod
    def unblock_ip(cls, ip_address):
        try:
            logger.info(f"Mencoba membuka blokir IP {ip_address}")

            if not os.path.exists(cls.UFW_PATH) or not os.path.exists(cls.SUDO_PATH):
                logger.error("UFW atau sudo tidak ditemukan")
                return False, "UFW atau sudo tidak ditemukan"

            cmd = [cls.SUDO_PATH, cls.UFW_PATH, 'delete', 'deny', 'from', ip_address, 'to', 'any']

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=cls.TIMEOUT
            )

            if result.returncode == 0:
                # Reload UFW untuk memastikan perubahan diterapkan
                reload_cmd = [cls.SUDO_PATH, cls.UFW_PATH, 'reload']
                subprocess.run(reload_cmd, timeout=cls.TIMEOUT)
                
                logger.info(f"Berhasil membuka blokir IP {ip_address}")
                return True, "Success"
            else:
                error_msg = result.stderr or "Unknown error occurred"
                logger.error(f"UFW command failed: {error_msg}")
                return False, f"UFW command failed: {error_msg}"

        except subprocess.TimeoutExpired:
            error_msg = f"Timeout saat membuka blokir IP {ip_address} (lebih dari {cls.TIMEOUT} detik)"
            logger.error(error_msg)
            return False, error_msg
        except subprocess.CalledProcessError as e:
            error_msg = f"Error unblocking IP {ip_address}: {e.stderr if e.stderr else str(e)}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Unexpected error unblocking IP {ip_address}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
