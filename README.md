# Assignment Submission Portal

Flask app for submitting assignments, with automated tests and CI.

## Run the app
```
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Run the tests
```
pytest
```

## Start the report receiver
```
python receiver.py
```
It listens on port 5001 and saves incoming reports to `test-report.json`.
Expose it with a tunnel and store the public URL in the GitHub secret `RECEIVER_URL`.