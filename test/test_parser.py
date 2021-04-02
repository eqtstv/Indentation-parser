import glob
import os
import unittest

from indentation_parser import TxtParser, parse_txt_file


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

        with open(filename, "w"):
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
            with open(f"{filename[:-4]}_parsed_{i}.txt", "w"):
                pass

        # WHEN get_filename_nums() method is ran on TxtParser
        result = txt_parser.get_filenames_nums()

        # THEN  it should return list numbered 0-4
        self.assertEqual(max(result), 4)

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


class TestParseTxtFile(unittest.TestCase):
    def test_check_main_indentation_type(self):
        # GIVEN test txt file
        filename = "is_prime.txt"
        # WHEN parse_txt_file() is ran with test file
        result = parse_txt_file(filename)

        # THEN it sould return proper message
        self.assertEqual(
            result,
            "File has:\n    rows indented with tabs: 2\
                \n    rows indented with spaces: 7\
                \n\nThe file has mainly spaces as indentation",
        )

    def test_from_tabs_to_spaces(self):
        # GIVEN test txt file
        filename = "is_prime.txt"

        # AND other test files are deleted
        for filename in glob.glob(f"{filename[:-4]}_parsed_*"):
            os.remove(filename)

        # WHEN parse_txt_file is ran with that file, and "tabs" argument
        result = parse_txt_file("is_prime.txt", "tabs")

        # THEN is sould modify 2 rows and create is_prime_parsed_0.txt
        self.assertEqual(
            result,
            "\nRows modified: 2\
                \nCreated file: is_prime_parsed_0.txt",
        )

    def test_from_spaces_to_tabs(self):
        # GIVEN test txt file
        filename = "is_prime.txt"

        # AND other test files are deleted
        for filename in glob.glob(f"{filename[:-4]}_parsed_*"):
            os.remove(filename)

        # WHEN parse_txt_file is ran with that file, and "spaces" argument
        result = parse_txt_file("is_prime.txt", "spaces")

        # THEN is sould modify 7 rows and create is_prime_parsed_0.txt
        self.assertEqual(
            result,
            "\nRows modified: 7\
                \nCreated file: is_prime_parsed_0.txt",
        )

    def test_from_tabs_to_spaces_inplace(self):
        # GIVEN test txt file
        filename = "is_prime.txt"
        test_filename = "test_file.txt"

        # AND copy test file
        with open(test_filename, "w+") as outfile, open(filename, "r") as infile:
            for line in infile:
                text_after = line
                outfile.write(text_after)

        # WHEN parse_txt_file is ran with that file, "tabs" argument and replace=True
        result = parse_txt_file(test_filename, "tabs", True)

        # THEN is sould modify 2 rows inplace
        self.assertEqual(
            result,
            "\nRows modified: 2\
                \nParsed file inplace",
        )

        os.remove(test_filename)

    def test_from_spaces_to_tabs_inplace(self):
        # GIVEN test txt file
        filename = "is_prime.txt"
        test_filename = "test_file.txt"

        # AND copy test file
        with open(test_filename, "w+") as outfile, open(filename, "r") as infile:
            for line in infile:
                text_after = line
                outfile.write(text_after)

        # WHEN parse_txt_file is ran with that file, "spaces" argument and replace=True
        result = parse_txt_file(test_filename, "spaces", True)

        # THEN is sould modify 7 rows inplace
        self.assertEqual(
            result,
            "\nRows modified: 7\
                \nParsed file inplace",
        )

        os.remove(test_filename)
