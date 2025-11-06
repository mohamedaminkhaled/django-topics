✅ Full Django Shell Testing Guide (for drf_serializers_demo)
1️⃣ Open Django Shell
python manage.py shell

2️⃣ Import Required Models & Serializer

(Adjust names if different in your project)

from api.models import Account, User
from api.serializers import AccountSerializer, UserSerializer

✅ 3️⃣ Create a user (if not already created)
user1 = User.objects.create_user(username='mohamed', email='mohamed@example.com', password='test123')
user2 = User.objects.create_user(username='amin', email='amin@example.com', password='test123')


(If you already have users, you can just query them instead)

user1 = User.objects.get(username='mohamed')
user2 = User.objects.get(username='amin')

✅ 4️⃣ Create the Account object

Since created is automatic, you don’t need to provide it:

acc = Account.objects.create(account_name='Gold Account', slug='gold-account')

✅ 5️⃣ Add users to the ManyToMany relation
acc.users.add(user1, user2)


🧠 You can also use .set([...]) if you want to replace the current list of users:

acc.users.set([user1, user2])

✅ 6️⃣ Verify your data
acc.users.all()
# <QuerySet [<User: mohamed>, <User: amin>]>

Account.objects.all()
# <QuerySet [<Account: Gold Account>]>

✅ Query Records
Account.objects.all()
User.objects.filter(account__slug="acc-001")
User.objects.get(email="mohamed@example.com")

✅ Update Records
user.email = "amin@example.com"
user.save()


Or bulk update:

User.objects.filter(account=acc).update(name="Updated Name")

✅ Delete Records
user.delete()
Account.objects.filter(slug="acc-001").delete()

✅ Test Serializer — Create
data = {
    "slug": "acc-002",
    "name": "New Account"
}

# DRF hyperlink serializers need a "request" in context
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

acc = Account.objects.get(slug="acc-002")

factory = APIRequestFactory()
request = factory.get('/api/accounts/')
serializer = AccountSerializer(acc, context={'request': Request(request)})

✅ Test Serializer — Represent DB -> JSON
serializer = AccountSerializer(data=data)
serializer.is_valid()
serializer.save()
serializer.data

✅ Test Serializer Validation
invalid_data = {"name": ""}  # slug missing

serializer = AccountSerializer(data=invalid_data)
serializer.is_valid()
serializer.errors

✅ Test Related Serializer Behavior
acc = Account.objects.get(slug="acc-002")
users = UserSerializer(User.objects.filter(account=acc), many=True)
users.data

✅ Simulate View (DRF Request Factory)

(optional — advanced testing inside shell)

from rest_framework.test import APIRequestFactory
from api.views import AccountListView

factory = APIRequestFactory()
request = factory.get('/accounts/')
view = AccountListView.as_view()
response = view(request)
response.data

✅ Exit Shell
exit()

Bonus ✅ Test Admin Panel (in browser)
python manage.py createsuperuser
python manage.py runserver


Then open:

http://127.0.0.1:8000/admin/