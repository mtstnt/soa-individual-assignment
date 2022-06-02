# Permutation and Combination Service
### Sebagai individual assignment untuk MK Service Oriented Architecture

<br>

## Overview  

Sistem terdiri dari 3 service, yaitu:
1. Gateway Service sebagai API Gateway untuk menghandle request dari user.
2. User Service untuk melakukan operasi terkait user (login, register)
3. Calculation Service untuk melakukan operasi permutasi dan kombinasi.

Menggunakan microservice framework **Nameko** yang menggunakan RPC over AMQP untuk memanggil dan mendapatkan return value dari fungsi di service lain.

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
3. Lakukan test request di `localhost:8000`. Lihat directory `tests` untuk melihat contoh request yang bisa dilakukan.

### Notes:
- Untuk request login dan register, copy hasil token yang didapat ke HTTP header Cookie seperti di `tests/combination.http` atau `tests/permutation.http`.  
Tested menggunakan extension HTTP Client VSCode: [humao.rest-client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) **dengan setting `Rest-client: Remember Cookies For Subsequent Requests` TIDAK dicentang.**  
Testing dengan Insomnia akan segera dilakukan ^^.