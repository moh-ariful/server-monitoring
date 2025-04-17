from openai import OpenAI
import json
import os

class GroqAnalyzer:
    def __init__(self):
        # Mengakses API key dari variabel lingkungan (akan diatur di settings.py)
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

    def analyze_alert(self, alert_data):
        # Membuat prompt yang lebih terstruktur
        prompt = f"""
        Analisis log Suricata berikut dan berikan analisis terstruktur dalam bahasa Indonesia:

        Data Alert:
        {alert_data}

        Berikan analisis dengan format berikut:
        1. RINGKASAN ANCAMAN:
        [Jelaskan jenis dan tingkat ancaman yang terdeteksi]

        2. ANALISIS DETAIL:
        [Berikan analisis teknis tentang alert ini]

        3. REKOMENDASI:
        [Berikan langkah-langkah spesifik untuk menangani ancaman ini]

        4. TINGKAT URGENSI:
        [Tentukan apakah perlu penanganan segera atau bisa ditunda]
        """

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Anda adalah analis keamanan siber berpengalaman yang ahli dalam menganalisis log Suricata. Berikan analisis yang jelas dan actionable dalam bahasa Indonesia."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="gpt-4.1-nano-2025-04-14",
                temperature=0.3,
                max_tokens=8000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error dalam analisis: {str(e)}"
