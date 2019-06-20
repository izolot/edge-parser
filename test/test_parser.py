import unittest
import constants
import parser
import hashlib
import os
import difflib
import pandas as pd
from app import parser



class TestParser(unittest.TestCase):

    def setUp(self):
       
        self.test_parser = parser.Parser("test/")
    
    
    def test_init_camera_folders(self):
        camera_uuids = {
        'ba9b1742-496b-4815-96ce-9aa8ec72f000': 'test/archive/edge2/inner_folder2', 
        'f95421e1-9857-4211-bfab-90fcfe94d2ae': 'test/archive/edge2/inner_folder2', 
        'bd6a0672-b72d-42d3-a54e-e1f9e7467a93': 'test/archive/edge1/inner_folder', 
        '5dda52a1-7cb0-4c25-a186-5a0d8ccf734d': 'test/archive/edge1/inner_folder'}
        self.test_parser.init_camera_folders()
        self.assertEqual(self.test_parser.camera_uuids, camera_uuids)


    def test_format_date(self):
       check_date = {
           "day_path": "2019/06/19",
           "year": 2019,
           "month": 6,
            "day": 19,
            "hour": 15,
            "minute": 1
       }       
       test_date = self.test_parser.format_date("2019-06-19T15:01:00.308+0300")
       self.assertEqual(test_date,check_date)

    def test_search_by_time(self):
        self.test_parser.init_camera_folders()
        test_edge1 = self.test_parser.search_by_time("2019-06-02T03:00:00.308+0300","2019-06-02T18:00:00.308+0300","f95421e1-9857-4211-bfab-90fcfe94d2ae")
        test_edge2 = self.test_parser.search_by_time("2019-06-07T03:00:00.308+0300","2019-06-07T18:00:00.308+0300","bd6a0672-b72d-42d3-a54e-e1f9e7467a93")
        self.assertEqual(test_edge1, constants.JSON_EDGE2)
        self.assertEqual(test_edge2, constants.JSON_EDGE1)

    def test_create_excel(self):
        self.test_parser.init_camera_folders()
        test_data = self.test_parser.search_by_time("2019-06-07T03:00:00.308+0300","2019-06-07T18:00:00.308+0300","bd6a0672-b72d-42d3-a54e-e1f9e7467a93")
        self.test_parser.create_excel("test_excel",test_data)
        self.assertTrue(os.stat("test/xlsx/test_excel.xlsx").st_size==os.stat("test/example.xlsx").st_size)
        

if __name__ == "__main__":
    unittest.main()    