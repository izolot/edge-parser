import unittest
import constants
import os
import pandas as pd
from edge_parser import Parser



class TestParser(unittest.TestCase):

    def setUp(self):
       
        self.test_parser = Parser("test/")
    
    
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
       test_date = self.test_parser.format_date("2019-06-19T15:01:00")
       self.assertEqual(test_date,check_date)

    def test_search_by_time(self):
        self.test_parser.init_camera_folders()
        test_edge1 = self.test_parser.search_by_time("2019-06-02T03:00:00","2019-06-02T18:00:00","f95421e1-9857-4211-bfab-90fcfe94d2ae")
        test_edge2 = self.test_parser.search_by_time("2019-06-07T03:00:00","2019-06-07T18:00:00","bd6a0672-b72d-42d3-a54e-e1f9e7467a93")
        self.assertEqual(test_edge1, constants.JSON_EDGE2)
        self.assertEqual(test_edge2, constants.JSON_EDGE1)

    def test_create_excel(self):
        self.test_parser.init_camera_folders()
        test_data = self.test_parser.search_by_time("2019-06-07T03:00:00","2019-06-07T18:00:00","bd6a0672-b72d-42d3-a54e-e1f9e7467a93")
        self.test_parser.create_excel("test_excel",test_data)
        test_excel = pd.read_excel("test/xlsx/test_excel.xlsx", sheet_name='Sheet1', index_col=0)
        example_excel = pd.read_excel("test/xlsx/example.xlsx", sheet_name='Sheet1', index_col=0)
        self.assertTrue(test_excel.equals(example_excel))
        

if __name__ == "__main__":
    unittest.main()    