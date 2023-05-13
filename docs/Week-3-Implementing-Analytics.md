# 3. Data Analytics
This week you will be querying the data in the database to build a basic analytics dashboard for this application. Again, let's not worry about verifying the QR codes just yet (that's next week's project).

## Step 1. The `/app/overview?course=xyz` View
An instructor can visit the `/app/overview?course=xyz`, this should load summary statistics about class attendance for the course associated with the code `xyz`. This view should only load if the user is logged in and they are an instructor. If not logged in, redirect the user too the login view `/accounts/login`.

These summary statistics should have:
1. The class name/number printed at the top
2. The total number of students in the class
3. For each class meeting, you should have the fraction of students with any image uploaded.
 
## Step 2. The `/app/student?course=xyz` View
An instructor can visit the `/app/student?course=xyz`, this should load specific stats for a student in a course code `xyz`. This view should only load if the user is logged in and they are an instructor. If not logged in, redirect the user too the login view `/accounts/login`.

These statistics should have:
1. The class name/number printed at the top
2. For each class meeting, whether the student has an uploaded image or not.

## Step 3. Testing Plan (Write Below)
As you add more functionality to the application, testing becomes much harder. Write a detailed plan on how you are testing all of this functionality.

Hint: think about how to write scripts that generate fake data to add to the database.

### Testing Plan

To generate fake data for testing purposes in our application, we will use the `django-seed` package. This package allows us to create custom data sets and seed them into our database. It can be installed using pip:

```
pip install django-seed
```

Next, we will add it to our installed apps in `settings.py`:

```
INSTALLED_APPS = (
    ...
    'django_seed',
)
```

We will then create a Python script that defines the data we want to generate and then run it using Django's management command. For example, we can create a script called `seed_data.py` that generates fake course data like this:

```
from django_seed import Seed
from myapp.models import Student, Instructor, Course

seeder = Seed.seeder()
```

To seed the `Student` model with 10 random entries, we will use the following code:

```
seeder.add_entity(Student, 10, {
    'first_name': lambda x: seeder.faker.first_name(),
    'last_name': lambda x: seeder.faker.last_name(),
    'email': lambda x: seeder.faker.email(),
    'password': lambda x: seeder.faker.password()
})

inserted_pks = seeder.execute()
```

To seed the Instructor model, use the following code:

```
seeder.add_entity(Instructor, 10, {
    'first_name': lambda x: seeder.faker.first_name(),
    'last_name': lambda x: seeder.faker.last_name(),
    'email': lambda x: seeder.faker.email(),
    'password': lambda x: seeder.faker.password()
})

inserted_pks = seeder.execute()
```

Finally, we can seed the `Course` model:

```
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

seeder.add_entity(Course, 10, {
    'course_name': lambda x: seeder.faker.sentence(),
    'course_number': lambda x: seeder.faker.unique.random_number(digits=5),
    'instructor_id': lambda x: seeder.faker.random_element(instructors),
    'start': lambda x: seeder.faker.date_between('-1y', '+1y'),
    'end': lambda x: seeder.faker.date_between('-1y', '+1y'),
    'meet_days': lambda x: seeder.faker.random_element(weekdays),
    'meet_start_time': lambda x: seeder.faker.time(),
    'meet_end_time': lambda x: seeder.faker.time()
})

inserted_pks = seeder.execute()
```



We can adjust the number of objects we want to generate as well as the fields and values we want to populate. Once we have created the scripts, we can run the following in the terminal:

```
python manage.py seed courses
python manage.py seed instructors
python manage.py seed students
```

This will populate our database with fake data. By using `django-seed`, we can easily and quickly generate large amounts of fake data to test our application's functionality. 


## Step 4. Implement (Step 3)
Implement Step 3 in code and include the results with your submitted pull request. 