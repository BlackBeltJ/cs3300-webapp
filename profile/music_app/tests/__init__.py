from django.test import TestCase

# Create your tests here.

@classmethod
def setUpTestData(cls):
    print("setUpTestData: Run once to set up non-modified data for all class methods.")
    pass
    #return super().setUpTestData()
    
def setUp(self):
    print("setUp: Run once for every test method to setup clean data.")
    pass
    #return super().setUp()
    
def test_false_is_false(self):
    print("Method: test_false_is_false.")
    self.assertFalse(False)
        
def test_false_is_true(self):
    print("Method: test_false_is_true.")
    self.assertTrue(False)
        
def test_true_is_true(self):
    print("Method: test_true_is_true.")
    self.assertTrue(True)
    