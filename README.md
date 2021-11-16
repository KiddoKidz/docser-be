# BackEnd Document Search
[![pipeline status](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2021/DD/sirclo-docser-document-search/be-docser/badges/staging/pipeline.svg)](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2021/DD/sirclo-docser-document-search/be-docser/-/commits/staging)
[![coverage report](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2021/DD/sirclo-docser-document-search/be-docser/badges/staging/coverage.svg)](https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2021/DD/sirclo-docser-document-search/be-docser/-/commits/staging)

### Kontributor
- Muhammad Zuhdi Zamrud
- Nadia Victoria Aritonang
- Audilla Putri Ferialdi
- Brian Athallah Yudiva
- Mushaffa Huda

### Deskripsi singkat project
Menyediakan sebuah aplikasi website tool pencarian dokumen yang terintegrasi dengan Google Drive yang dapat melakukan pencarian dengan cepat, typo tolerance, memberikan hasil yang kontekstual dan relevan, dapat menunjukkan hierarki dari dokumen teknis dengan baik, dan juga terlindungi dari akses publik dengan me-leverage penggunaan OAuth dari Google.

### Cara run di local

1. Install [Docker](https://www.docker.com/get-started) dan [Docker Compose](https://docs.docker.com/compose/install/)

2. Clone repository **be-docser** 
```git clone https://gitlab.cs.ui.ac.id/ppl-fasilkom-ui/2021/DD/sirclo-docser-document-search/be-docser```

3. Pindah ke directory **be-docser** 
```cd be-docser```

4. Jalankan command berikut 
~~~
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
~~~

5. URL yang tersedia adalah:
- /admin/
- /auth/login/ 
- /auth/userinfo/
- /auth/oauth2callback/
- /api/drive/files/