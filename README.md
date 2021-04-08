# Indentation-parser

Convert indentation (tabs to spaces and vice versa)


```
λ python indentation_parser.py -h

usage: indentation_parser.py [-h] [-f {tabs,spaces}] [-r] [-t TAB_CHARS] filename

Txt file parser. Convert indentation (tabs to spaces and vice versa).

positional arguments:
  filename              Name of the file to convert

optional arguments:
  -h, --help            show this help message and exit
  -f {tabs,spaces}, --from {tabs,spaces}
                        Convert from: ('tabs' or 'spaces')
  -r, --replace         Replace original file
  -t TAB_CHARS, --tab-chars TAB_CHARS
                        Number of spaces for one tab
```
