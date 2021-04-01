import argparse
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
        self.no_spaces = no_spaces

    def get_filename(self, filename, replace):
        self.filename = filename
        self.replace = replace

    def convert_file(self, from_indent):
        if from_indent == "tabs":
            self.convert_tabs_to_spaces()
        elif from_indent == "spaces":
            self.convert_spaces_to_tabs()

    def convert_tabs_to_spaces(self):
        fout = open("output.txt", "w")
        regex_search_term = r"\G\t"
        regex_replacement = " " * self.no_spaces

        with open(self.filename, "r") as fin:
            for line in fin:
                text_after = re.sub(regex_search_term, regex_replacement, line)
                fout.write(text_after)
        fout.close()

    def convert_spaces_to_tabs(self):
        fout = open("output.txt", "w")
        regex_search_term = f"\\G\\s{ {self.no_spaces} }"
        regex_replacement = "\t"

        with open(self.filename, "r") as fin:
            for line in fin:
                text_after = re.sub(regex_search_term, regex_replacement, line)
                fout.write(text_after)
        fout.close()

    def check_main_indentation_type(self):
        spaces, tabs = [], []
        fout = open("output.txt", "w")

        regex_search_term = f"\\G\\s{ {4} }"
        regex_search_term2 = r"\G\t"

        with open(self.filename, "r") as fin:
            for line in fin:
                spaces.append(re.search(regex_search_term, line))
                tabs.append(re.search(regex_search_term2, line))
        fout.close()

        count_dict = {
            "tabs": len(list(filter(None, tabs))),
            "spaces": len(list(filter(None, spaces))),
        }

        print(
            f"File has:\n    lines indented with tabs: {count_dict['tabs']}\
                \n    lines indented with spaces: {count_dict['spaces']}\
                \n\nFile has mainly {max(count_dict, key=count_dict.get)} as indentation"
        )


if __name__ == "__main__":
    args = get_argparser()
    txt_parser = TxtParser(args["tab_chars"])
    txt_parser.get_filename(args["filename"], args["replace"])

    if not args["from"]:
        txt_parser.check_main_indentation_type()

    else:
        txt_parser.convert_file(args["from"])
