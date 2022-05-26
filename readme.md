# Permutation and Combination Service
### Sebagai individual assignment untuk MK Service Oriented Architecture

<br>

## Overview  

Sistem terdiri dari 3 service, yaitu:
1. Gateway Service sebagai API Gateway untuk menghandle request dari user.
2. User Service untuk melakukan operasi terkait user (login, register)
3. Calculation Service untuk melakukan operasi permutasi dan kombinasi.

Menggunakan microservice framework **Nameko** yang menggunakan RPC over AMQP untuk melakukan RPC antar service-service. Hal ini memungkinkan untuk scaling satu atau banyak service dengan menambahkan node baru untuk service itu yang akan otomatis menjadi cosnumer dari message queue service tersebut (dilakukan oleh Nameko).

***Placeholder Diagram***


***Hiyaaa***

<br>

---

<br>

## Cara setup/instalasi
### **Prerequisites**:
- Docker
- Python & Pip package manager.
- Pipenv sebagai virtual env manager.

### **Steps**:
1. Install dependencies dengan `pipenv install` apabila menggunakan pipenv, atau pip install -r requirements.txt untuk menginstall dependency dengan pip.
2. Jalankan script di `scripts/run.sh` atau `scripts/run.bat` untuk Windows. (run.bat sudah tested.)
3. Lakukan test request di `localhost:8000`. Lihat directory `tests` untuk melihat contoh request.
