pip3 install -r requirements.txt --upgrade --user
export FLASK_APP=run.py
export FLASK_ENV=development
python3 -m flask run --host=0.0.0.0 --port=5000
