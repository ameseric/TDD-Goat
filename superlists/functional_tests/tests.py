''' Functional Tests 
    Author: Eric Ames
'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

from django.test import LiveServerTestCase

MAX_WAIT = 10

class NewVisitorTest( LiveServerTestCase):
    browser = None

    def setUp( self):
        self.browser = webdriver.Firefox()



    def tearDown( self):
        self.browser.quit()


    def wait_and_check_for_row_in_table( self ,rowtext ,table_id):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id( table_id)
                rows = table.find_elements_by_tag_name( 'tr')
                self.assertIn( rowtext ,[row.text for row in rows])
                return
            except (AssertionError ,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep( 0.5)



    def test_start_list_and_retrieve( self):
        self.browser.get( self.live_server_url)

        #User notices title and header are To-Do
        self.assertIn( 'To-Do' ,self.browser.title)
        header_text = self.browser.find_element_by_tag_name( 'h1').text
        self.assertIn( 'To-Do' ,header_text)


        # User is invited to enter items
        inputbox = self.browser.find_element_by_id( 'id_new_item')
        self.assertEqual(
                inputbox.get_attribute( 'placeholder')
                ,'Enter a to-do item'
        )

        items = [ 'Buy feathers' ,'Dye feathers']

        #User enters items and hits enter, one-by-one
        for i,item in enumerate( items):
            inputbox = self.browser.find_element_by_id( 'id_new_item')
            inputbox.send_keys( item)
            inputbox.send_keys( Keys.ENTER)
            self.wait_and_check_for_row_in_table( '%d: %s' % ( i+1 ,item) ,'id_list_table')


        # User checks if list persists, she is given a permanent URL for her list
        self.fail( 'Finish the test!')

        # User visit unique URL

