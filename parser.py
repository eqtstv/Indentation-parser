import argparse
import regex as re


def get_argparser():
    parser = argparse.ArgumentParser(
        description="Txt file parser.\
            Convert indentation (tabs to spaces and vice versa)."
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
    def convert_tabs_to_spaces(self, no_spaces):
        fin = open("is_prime.txt", "r")
        fout = open("output.txt", "w")
        regex_search_term = r"\G\t"
        regex_replacement = " " * no_spaces
        for line in fin:
            text_after = re.sub(regex_search_term, regex_replacement, line)
            fout.write(text_after)

        fin.close()
        fout.close()

    def convert_spaces_to_tabs(self, no_spaces):
        fin = open("is_prime.txt", "r")
        fout = open("output.txt", "w")
        regex_search_term = f"\\G\\s{ {no_spaces} }"
        regex_replacement = "\t"
        for line in fin:
            text_after = re.sub(regex_search_term, regex_replacement, line)
            fout.write(text_after)

        fin.close()
        fout.close()


if __name__ == "__main__":
    args = get_argparser()

    if not args["from"]:
        print("None")
    elif args["from"] == "tabs":
        txt_parser = TxtParser()
        txt_parser.convert_tabs_to_spaces(args["tab_chars"])
    elif args["from"] == "spaces":
        txt_parser = TxtParser()
        txt_parser.convert_spaces_to_tabs(args["tab_chars"])
