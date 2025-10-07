🧠 Prerequisites

Before you start:

Make sure migrations are done:

python manage.py migrate


Ensure SessionMiddleware and django.contrib.sessions are enabled in settings.py.

🐚 Open Django Shell
python manage.py shell


Then inside the shell, follow along 👇

1️⃣ Import required classes
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

2️⃣ Create a new session manually
s = SessionStore()


Now you can use it like a dictionary.

s['theme_pref'] = 'dark'
s['recent_items'] = [1, 2, 3]

3️⃣ Save session to database
s.save()  # creates a row in django_session table
print(s.session_key)


✅ Output example:

'f4k4f3v27p4zcn4g9l8zz7s5v9xw0k5u'


This key is what Django stores in the client’s session cookie (sessionid).

4️⃣ Retrieve an existing session

You can re-open the session later with its key:

key = s.session_key
s2 = SessionStore(session_key=key)

print(s2['theme_pref'])      # → 'dark'
print(s2['recent_items'])    # → [1, 2, 3]

5️⃣ Modify or delete keys
s2['theme_pref'] = 'light'
del s2['recent_items']
s2.save()


Confirm changes:

print(s2['theme_pref'])  # → 'light'
print(s2.get('recent_items'))  # → None

6️⃣ Session expiry handling
s2.set_expiry(60 * 60 * 24)  # 1 day
print(s2.get_expiry_age())   # → seconds until expiry


You can also check the expiry date directly:

print(s2.get_expiry_date())

7️⃣ Explore sessions stored in DB
from django.contrib.sessions.models import Session
sessions = Session.objects.all()
for sess in sessions:
    print(sess.session_key, sess.expire_date)


To inspect session data (decoded):

for sess in sessions:
    print(sess.get_decoded())


Output example:

{'theme_pref': 'light'}

8️⃣ Delete a session manually
s2.delete()


Confirm removal:

Session.objects.filter(session_key=key).exists()  # → False