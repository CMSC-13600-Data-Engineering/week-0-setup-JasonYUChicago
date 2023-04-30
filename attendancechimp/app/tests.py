from django.test import TestCase
import logging, sys, traceback

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

if __name__ == '__main__':
    doTests()

# Create your tests here.
doTests()