
How to deploy (Render/Railway/Heroku-like):
1) Create a new empty repo on GitHub and upload these four files to the root: app.py, requirements.txt, Procfile, README_DEPLOY.txt
2) On your PaaS, create a new Web Service from that repo.
   Build command: pip install -r requirements.txt
   Start command: gunicorn app:app --preload --bind 0.0.0.0:$PORT
3) When Live, visit your URL (e.g., https://your-app.onrender.com). You should see the Friends Activity page.
4) JSON feed at /feed.json
