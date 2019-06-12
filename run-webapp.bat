call .\venv\Scripts\activate
pip install -r requirements.txt --upgrade
set FLASK_APP=run.py
set FLASK_ENV=development
python -m flask run --host=0.0.0.0 --port=5000
timeout 20