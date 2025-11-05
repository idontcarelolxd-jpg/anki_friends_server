
Cloud deploy (Render/Railway/Fly/Heroku-like)
---------------------------------------------
1) Put these files in a new GitHub repo's root (app.py, requirements.txt, Procfile).
2) On your PaaS, create a new web service from that repo.
   - Build command: (none; standard Python build)
   - Start command: use the Procfile or: gunicorn app:app --preload --bind 0.0.0.0:$PORT
3) After deploy, you'll get a URL like https://your-app.onrender.com
4) In Anki: Tools -> Add-ons -> Friends Activity -> Config
   Set "server" to that URL (no trailing slash), eg "https://your-app.onrender.com".
