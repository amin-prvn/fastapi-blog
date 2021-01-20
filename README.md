## Installation

1. Create virtualenv.
```
python3 -m virtualenv venv
```
2. Active environment.
```
source venv/bin/activate 
```
3. Install requirements.
```
pip install -r requirements.txt
```
4. Create database and set in app/database.py like this:
```
postgresql://<database user>:<database password>@<host>:<port>/<database name>
```
5. This code automaticaly create database table and schmas.
6. Run server with **uvicorn**:
```
uvicorn app.main:app --reload 
```

---
> Mohammad Amin Parvanian