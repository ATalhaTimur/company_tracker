# Python 3.12 imajını kullan
FROM python:3.12

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinimleri kopyala
COPY requirements.txt /app/

# Gereksinimleri yükle
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg

# Uygulama kodlarını kopyala
COPY . /app/

# Django migration çalıştır ve sunucuyu başlat
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
