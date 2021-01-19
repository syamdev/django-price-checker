PriceChecker
==============================

Price Checker Web App

### Quick setup

> The next steps assume that conda is already installed

1 - <a name="step-1">Create a conda environment:</a>


```bash
conda create python=3.8 -n pricechecker
```
2 - <a name="step-2">Activate the conda environment</a>

```bash
conda activate pricechecker
```

3 - <a name="step-3">Install the project basic dependencies and development dependencies</a>

> Make sure you are inside the root project directory before executing the next commands.
>
> The root project directory is the directory that contains the `manage.py` file

On Linux and Mac

```bash
pip install -r requirements/local.txt
```

On Windows

```bash
pip install -r requirements\local.txt
```

4 - <a name="step-4">Configure the database connection string on the .env</a>

On Linux and Mac

```bash
cp env.sample.mac_or_linux .env
```

On Windows

```bash
copy env.sample.windows .env
```

Change the value of the variable `DATABASE_URL` inside the file` .env` with the information of the database we want to connect.

Note: Several project settings have been configured so that they can be easily manipulated using environment variables or a plain text configuration file, such as the `.env` file.
This is done with the help of a library called django-environ. We can see the formats expected by `DATABASE_URL` at https://github.com/jacobian/dj-database-url#url-schema. 

5 - <a name="step-5">Use the django-extension's `sqlcreate` management command to help to create the database</a>

On Linux:

```bash
python manage.py sqlcreate | sudo -u postgres psql -U postgres
```

On Mac:

```bash
python manage.py sqlcreate | psql
```

On Windows:

Since [there is no official support for PostgreSQL 12 on Windows 10](https://www.postgresql.org/download/windows/) (officially PostgreSQL 12 is only supported on Windows Server), we choose to use SQLite3 on Windows

6 - <a name="step-6">Run the `migrations` to finish configuring the database to able to run the project</a>


```bash
python manage.py migrate
```


### <a name="running-tests">Running the tests and coverage test</a>


```bash
coverage run -m pytest
```


## <a name="troubleshooting">Troubleshooting</a>

If for some reason you get an error similar to bellow, is because the DATABASE_URL is configured to `postgres:///pricechecker` and because of it the generated `DATABASES` settings are configured to connect on PostgreSQL using the socket mode.
In that case, you must create the database manually because the `sqlcreate` is not capable to correctly generate the SQL query in this case.

```sql
ERROR:  syntax error at or near "WITH"
LINE 1: CREATE USER  WITH ENCRYPTED PASSWORD '' CREATEDB;
                     ^
ERROR:  zero-length delimited identifier at or near """"
LINE 1: CREATE DATABASE pricechecker WITH ENCODING 'UTF-8' OWNER "";
                                                             ^
ERROR:  syntax error at or near ";"
LINE 1: GRANT ALL PRIVILEGES ON DATABASE pricechecker TO ;
```



```sql
ERROR:  role "myuser" already exists
ERROR:  database "pricechecker" already exists
GRANT
```

<a name="troubleshooting-delete-database">You can delete the database and the user with the commands below and then [perform step 5 again](#step-5).</a>

> :warning: **Be very careful here!**: The commands below erase data, and should only be executed on your local development machine and **NEVER** on a production server.


On Linux:

```bash
sudo -u postgres dropdb -U postgres --if-exists pricechecker
sudo -u postgres dropuser -U postgres --if-exists myuser
```

On Mac:

```bash
dropdb --if-exists pricechecker
dropuser --if-exists myuser
```


## Flow for New App

### Create New App
```commandline
python manage.py startapp app_coffee
```
  
### Move New App to app directory
```commandline
mv app_coffee pricechecker/
```

### Set the New App Config
- in **apps.py**
```python
name = 'pricechecker.app_coffee'
```

### Add New App to Installed Apps
- in LOCAL_APPS **settings/base.py**
```python
'pricechecker.app_coffee.apps.AppCoffeeConfig',
```

### Add New App Model in **models.py**
- create field
- makemigrations new_app & migrate new_app

### Test New App Model in Shell Plus
`python manage.py shell_plus`

### Create Module for App Model Tests
- Delete **tests.py**
- Create directory tests/
- Inside of tests/ , create **__init__.py**, **test_models.py** and other individual test modules.
- Create test function
- Run coverage.py
```
coverage run -m pytest
coverage report
coverage html
```

### Test using Factory
```
python manage.py shell_plus

from pricechecker.users.tests.factories import UserFactory
user = UserFactory()
user
user.username
user.email
user.name
user.password
# delete user that we have created above
user.delete()

from faker import Faker
fake = Faker({'en-US': 1})
fake.country_code()
```

### Create HTML Templates
- Add crispy-form

### Add authentication
- Make page accessible for logged-in user
```
from django.contrib.auth.mixins import LoginRequiredMixin

class CoffeeCreateView(LoginRequiredMixin, CreateView):
...
```

### Create the author of post in **models.py**
```
author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
```

### Set the default author of post
- Through: `python manage.py shell_plus`
```
coffeeauthor = User.objects.get(username='syam')

for coffee in Coffee.objects.all():
    coffee.author = coffeeauthor
    coffee.save()
```
- Check author via shell or admin
```
for coffee in Coffee.objects.all():
    print(coffee, coffee.author)
```

### Display author in detail view
- Set the author after form validation
- Add view to template

### Test again with factory via shell 
```
python manage.py shell_plus

from pricechecker.app_coffee.tests.factories import CoffeeFactory

coffee = CoffeeFactory()
coffee.author
# <User: sgonzalez>

# Delete coffee detail
coffee.delete()
# (1, {'app_coffee.Coffee': 1})

u = User.objects.last()
u
# <User: sgonzalez>

# Delete user
u.delete()
# (1, {'users.User': 1})
```
