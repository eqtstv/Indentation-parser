import argparse
import regex as re
import sys


class Parser:
    def __init__(self, parser):
        self.parser = parser

    def tabs_to_spaces(self, no_spaces):
        fin = open("is_prime.txt", "r")
        fout = open("output.txt", "w")
        regex_search_term = r"\G\t"
        regex_replacement = " " * no_spaces
        print(regex_search_term)
        for line in fin:
            text_after = re.sub(regex_search_term, regex_replacement, line)
            fout.write(text_after)

        fin.close()
        fout.close()

    def spaces_to_tabs(self, no_spaces):
        fin = open("is_prime.txt", "r")
        fout = open("output.txt", "w")
        regex_search_term = r"\G\s{4}"
        regex_replacement = "\t"
        print(regex_search_term)
        for line in fin:
            print(re.findall(regex_search_term, line))
            text_after = re.sub(regex_search_term, regex_replacement, line)
            fout.write(text_after)

        fin.close()
        fout.close()


if __name__ == "__main__":
    if "-f" in sys.argv:
        print("-f in")
    if "-r" in sys.argv:
        print("-r in")
    if "-t" in sys.argv:
        print("-t in")
    print(sys.argv)

    parser = Parser("parser")
    parser.spaces_to_tabs(4)