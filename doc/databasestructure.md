[Sommaire](https://ursi-2020.github.io/Documentation/)

# Database structure and fixtures

## Database structure

### The structure

Your application will interact with the database through an ORM (Object Relational Mapping) whether for the synchronous or asynchronous process. 
If you don't know what an ORM is, well you didn't listen in URSI class and that's bad !

You have to define all your classes in the models file located here : ```application/djangoapp/models.py```. 
The example app comes with 2 classes ("Article" and "Vente") with a relation : an "Article" can have many object "Vente" related to it.

Each time you start your app with start_app.sh, the database structure will be updated to match this models file.

### Access to the objects

To access to these objects in your database, you have to import the models package in your code :
```python
from application.djangoapp.models import *
```

Then access to the objects list with this method :
```python
Vente.objects.all()
```

The example app will print by default all the sales recorded in the database at the launch of the application.
The example code is located at : ```application/asynmsg/main.py```

Django's ORM is mush more complete than this. You can have a look at the official Django documentation to learn more : [Django models](https://docs.djangoproject.com/fr/2.2/topics/db/models/)

## Database fixtures

As you have noticed, each member of your team has his own database and so his own data set.
Fortunately, it exists a way to dump or import your application data !

Indeed, it is sometimes useful to pre-fill the database with fixed data when first configuring an application. This is done with fixture files.

Your application fixtures must be located inside the ```fixture``` directory and be in json format.
The example app comes with one fixture (example.json) containing data for the "Article" and "Vente" classes seen previously.

To load all the fixtures located in the fixtures directory, simply launch the start_app script with the loadexampledata argument :
```bash
start_app.sh loadexampledata
```

If you do this with the example app, you should see the list of sales printed in standard output.

### Create a fixture

To create a fixture, simply run the create_fixture script with the name of your fixture as argument :
```bash
create_fixture.sh mafixture
```

For sure, you must launch your application and create some data before creating a fixture.

As always, you can refer to django tutorials about fixtures for more information : [fixtures](https://docs.djangoproject.com/fr/2.2/howto/initial-data/)