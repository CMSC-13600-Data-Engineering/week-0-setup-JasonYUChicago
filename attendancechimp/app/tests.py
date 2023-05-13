from django.test import TestCase
import logging, sys, traceback
from django_seed import Seed,tests
from .models import Student, Instructor, Course

root=logging.getLogger()
root.setLevel(logging.DEBUG)
handler=logging.StreamHandler(sys.stdout)

from .models import*
def doTests():
    logging.info('Test 1. running addInstructor()')
    try:
        testAddInstructor()
        logging.info('Test 1. Passed')
    except AssertionError:
        logging.info('Test 1. Failed with error ' + str(traceback.format_exc()))
def testAddInstructor():
    Instructor.objects.filter(instructor_id = 0).delete()
    addInstructor(0,'John','Smith','john_smith@uchicago.edu', 'johnspassword')
    instructor = Instructor.objects.filter(instructor_id=0)
    assert(len(instructor)==1)

    assert(instructor[0].first_name=='John')
    assert(instructor[0].last_name=='Smith')
    assert(instructor[0].email == 'john_smith@uchicago.edu')
    assert(instructor[0].password == 'johnspassword')

    instructor.delete()

seeder = Seed.seeder()

seeder.add_entity(Student, 10, {
    'first_name': lambda x: seeder.faker.first_name(),
    'last_name':lambda x: seeder.faker.last_name(),
    'email': lambda x: seeder.faker.email(),
    'password': lambda x: seeder.faker.password(),
})

inserted_pks = seeder.execute()

seeder.add_entity(Instructor, 10, {
    'first_name':lambda x: seeder.faker.first_name(),
    'last_name':lambda x: seeder.faker.last_name(),
    'email': lambda x: seeder.faker.email(),
    'password': lambda x: seeder.faker.password(),
})

inserted_pks = seeder.execute()

weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday']
seeder.add_entity(Course,10,{
    'course_name':lambda x: seeder.faker.sentence(),
    'course_number':lambda x: seeder.faker.unique.random_number(digits=5),
    'instructor_id':lambda x: seeder.faker.random_element(Instructor),
    'start':lambda x: seeder.faker.date_between('-1y','+1y'),
    'end':lambda x: seeder.faker.date_between('-1y','+1y'),
    'meet_days': lambda x: seeder.faker.random_element(weekdays),
    'meet_start_time':lambda x: seeder.faker.time(),
    'meet_end_time':lambda x: seeder.faker.time(),
})

inserted_pks = seeder.execute()

if __name__ == '__main__':
    doTests()

# Create your tests here.
doTests()