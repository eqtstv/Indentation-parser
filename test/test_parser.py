import unittest
from unittest.mock import patch
from indentation_parser import TxtParser
import os
import glob


class TestTxtParser(unittest.TestCase):
    def test_default_init(self):
        # GIVEN TxtParser class and default init variables dict
        default_dict = {
            "regex_search_spaces": "\\G\\ {4}",
            "regex_search_tabs": "\\G\\t",
            "regex_substitute_spaces": "    ",
            "regex_substitute_tabs": "\t",
        }
        # WHEN TxtParser is initiated
        txt_parser = TxtParser()

        # THEN class should have default variables
        self.assertEqual(txt_parser.__dict__, default_dict)

    def test_tab_chars_init(self):
        # GIVEN TxtParser class and init variables with tab_chars=2
        default_dict = {
            "regex_search_spaces": "\\G\\ {2}",
            "regex_search_tabs": "\\G\\t",
            "regex_substitute_spaces": "  ",
            "regex_substitute_tabs": "\t",
        }
        # WHEN TxtParser is initiated with tab_chars=2 variable
        txt_parser = TxtParser(2)

        # THEN class should have proper variables
        self.assertEqual(txt_parser.__dict__, default_dict)

    def test_get_filename(self):
        # GIVEN TxtParser class and filename variable
        txt_parser = TxtParser()
        filename = "myfilename.txt"

        # WHEN get_filename() method is ran on TxtParser with filename variable
        txt_parser.get_filename(filename)

        # THEN class should have proper filename variable
        self.assertEqual(txt_parser.__dict__["filename"], filename)

    def test_get_filename_nums_no_copies(self):
        # GIVEN TxtParser class, filename variable with no copies
        txt_parser = TxtParser()
        filename = "this_is_a_test_filename_for_filename_nums.txt"
        txt_parser.get_filename(filename)

        # WHEN get_filename_nums() method is ran on TxtParser
        result = txt_parser.get_filenames_nums()

        # THEN  it should return empty list of filename_nums
        self.assertEqual(result, [])

    def test_get_filename_nums_with_one_copy(self):
        # GIVEN TxtParser class, filename variable with one copy
        txt_parser = TxtParser()
        filename = "this_is_a_test_filename_for_filename_nums.txt"
        txt_parser.get_filename(filename)

        with open(filename, "w") as f:
            pass

        # WHEN get_filename_nums() method is ran on TxtParser
        result = txt_parser.get_filenames_nums()

        # THEN  it should return empty list
        self.assertEqual(result, [])

        os.remove(filename)

    def test_get_filename_nums_with_copies(self):
        # GIVEN TxtParser class, filename variable with 5 copies
        txt_parser = TxtParser()
        filename = "this_is_a_test_filename_for_filename_nums.txt"
        txt_parser.get_filename(filename)

        for i in range(5):
            with open(f"{filename[:-4]}_parsed_{i}.txt", "w") as f:
                pass

        # WHEN get_filename_nums() method is ran on TxtParser
        result = txt_parser.get_filenames_nums()

        # THEN  it should return list numbered 0-4
        self.assertEqual(result, [0, 1, 2, 3, 4])

        for i in range(5):
            os.remove(f"{filename[:-4]}_parsed_{i}.txt")

    def test_get_parsed_filename_no_copies(self):
        # GIVEN TxtParser class and filename variable and empty filenames_nums
        txt_parser = TxtParser()
        filename = "myfilename.txt"
        txt_parser.get_filename(filename)
        filenames_nums = []

        # WHEN get_filename() method is ran on TxtParser with filename variable
        result = txt_parser.get_parsed_filename(filenames_nums)

        # THEN  it should return filenames with _parsed_0.txt at the end
        self.assertEqual(result, f"{filename[:-4]}_parsed_0.txt")

    def test_get_parsed_filename_with_copies(self):
        # GIVEN TxtParser class and filename variable and list of filenames_nums
        txt_parser = TxtParser()
        filename = "myfilename.txt"
        txt_parser.get_filename(filename)
        filenames_nums = [0, 1, 2, 3, 4]

        # WHEN get_filename() method is ran on TxtParser with filename variable
        result = txt_parser.get_parsed_filename(filenames_nums)

        # THEN  it should return filenames with _parsed_5.txt at the end
        self.assertEqual(result, f"{filename[:-4]}_parsed_5.txt")