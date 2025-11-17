# Django Signals Demo Project  
## ✔ Covers all topics in Django 5.2 Signals Documentation

This project demonstrates:

- Built-in signals  
- Model signals  
- Management of signal receivers  
- Connecting signals using `@receiver`  
- Connecting inside `AppConfig.ready()`  
- Custom signals (`django.dispatch.Signal`)  
- Request/response signals  
- ManyToMany signals  
- Disconnecting signals  
- Sending signals manually

---

# 📁 Project Structure

```
signals_demo/
│
├── manage.py
├── signals_demo/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── apps.py
│
└── core/
    ├── __init__.py
    ├── apps.py
    ├── models.py
    ├── signals.py
    ├── views.py
    ├── admin.py
    ├── receivers.py
    └── custom_signals.py
```