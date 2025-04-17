import json
import subprocess
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SuricataMonitor:
    def __init__(self):
        self.fast_log_process = None
        self.eve_json_process = None
        self.fast_log_path = '/var/log/suricata/fast.log'
        self.eve_json_path = '/var/log/suricata/eve.json'

    def check_log_file(self, file_path):
        """Verifikasi keberadaan dan aksesibilitas file log"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Log file tidak ditemukan: {file_path}")
            if not os.access(file_path, os.R_OK):
                raise PermissionError(f"Tidak dapat membaca log file: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error checking log file {file_path}: {e}")
            return False

    def start_fast_log_monitoring(self):
        """Monitoring fast.log dengan penanganan error yang lebih baik"""
        try:
            if not self.check_log_file(self.fast_log_path):
                return None

            # Gunakan tail -F untuk lebih tahan terhadap rotasi log
            cmd = ['tail', '-F', self.fast_log_path]
            self.fast_log_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )

            # Cek apakah proses berhasil dimulai
            if self.fast_log_process.poll() is not None:
                logger.error("Failed to start fast log monitoring process")
                return None

            return self.fast_log_process

        except Exception as e:
            logger.error(f"Error starting fast log monitoring: {e}")
            return None

    def start_eve_json_monitoring(self):
        """Monitoring eve.json dengan penanganan error yang lebih baik"""
        try:
            if not self.check_log_file(self.eve_json_path):
                return None

            # Gunakan jq untuk memfilter dan memformat JSON
            cmd = f"tail -F {self.eve_json_path} | jq -c 'select(.event_type==\"alert\")'"
            self.eve_json_process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )

            # Cek apakah proses berhasil dimulai
            if self.eve_json_process.poll() is not None:
                logger.error("Failed to start eve.json monitoring process")
                return None

            return self.eve_json_process

        except Exception as e:
            logger.error(f"Error starting eve.json monitoring: {e}")
            return None

    def stop_monitoring(self):
        """Hentikan semua proses monitoring dengan aman"""
        try:
            if self.fast_log_process:
                self.fast_log_process.terminate()
                self.fast_log_process.wait(timeout=5)
                self.fast_log_process = None
        except Exception as e:
            logger.error(f"Error stopping fast log process: {e}")

        try:
            if self.eve_json_process:
                self.eve_json_process.terminate()
                self.eve_json_process.wait(timeout=5)
                self.eve_json_process = None
        except Exception as e:
            logger.error(f"Error stopping eve.json process: {e}")

