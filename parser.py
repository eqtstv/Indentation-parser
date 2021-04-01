import argparse
import glob
import os

import regex as re


def get_argparser():
    parser = argparse.ArgumentParser(
        description="Txt file parser.\
            Convert indentation (tabs to spaces and vice versa)."
    )

    parser.add_argument(
        "filename",
        type=str,
        help="Name of the file to convert",
    )

    parser.add_argument(
        "-f",
        "--from",
        type=str,
        default=False,
        choices=["tabs", "spaces"],
        help="Convert from: ('tabs' or 'spaces')",
    )
    parser.add_argument(
        "-r",
        "--replace",
        action="store_true",
        help="Replace original file",
    )
    parser.add_argument(
        "-t",
        "--tab-chars",
        type=int,
        default=4,
        help="Number of spaces for one tab",
    )

    return vars(parser.parse_args())


class TxtParser:
    def __init__(self, no_spaces):
        self.regex_search_spaces = f"\\G\\ { {no_spaces} }"
        self.regex_search_tabs = r"\G\t"
        self.regex_substitute_spaces = " " * no_spaces
        self.regex_substitute_tabs = "\t"

    def get_filename(self, filename):
        self.filename = filename

    def get_parsed_filename(self):
        filenames_list = glob.glob(f"{self.filename[:-4]}_parsed_*.txt")
        filenames_nums_list = [
            int(os.path.splitext(val)[0].split("_")[-1]) for val in filenames_list
        ]

        if not filenames_list:
            return f"{self.filename[:-4]}_parsed_0.txt"

        else:
            new_num = max(filenames_nums_list) + 1
            return f"{self.filename[:-4]}_parsed_{new_num}.txt"

    def convert_file_from(self, from_indent, replace):
        if from_indent == "tabs":
            self.convert_file(
                self.regex_search_spaces, self.regex_substitute_tabs, replace
            )
        elif from_indent == "spaces":
            self.convert_file(
                self.regex_search_tabs, self.regex_substitute_spaces, replace
            )

    def convert_file(self, search, substitute, replace):
        if replace:
            with open("temp.txt", "w") as outfile, open(self.filename, "r") as infile:
                for line in infile:
                    text_after = re.sub(search, substitute, line)
                    outfile.write(text_after)
            os.remove(self.filename)
            os.rename("temp.txt", self.filename)
        else:
            parsed_filename = self.get_parsed_filename()
            with open(parsed_filename, "w+") as outfile, open(
                self.filename, "r"
            ) as infile:
                for line in infile:
                    text_after = re.sub(search, substitute, line)
                    outfile.write(text_after)

    def check_main_indentation_type(self):
        spaces, tabs = [], []

        with open(self.filename, "r") as fin:
            for line in fin:
                spaces.append(re.search(self.regex_search_spaces, line))
                tabs.append(re.search(self.regex_search_tabs, line))

        count_dict = {
            "tabs": len(list(filter(None, tabs))),
            "spaces": len(list(filter(None, spaces))),
        }

        print(
            f"File has:\n    lines indented with tabs: {count_dict['tabs']}\
                \n    lines indented with spaces: {count_dict['spaces']}\
                \n\nThe file has mainly {max(count_dict, key=count_dict.get)} as indentation"
        )


if __name__ == "__main__":
    args = get_argparser()
    txt_parser = TxtParser(args["tab_chars"])
    txt_parser.get_filename(args["filename"])

    if not args["from"]:
        txt_parser.check_main_indentation_type()
    else:
        txt_parser.convert_file_from(args["from"], args["replace"])
