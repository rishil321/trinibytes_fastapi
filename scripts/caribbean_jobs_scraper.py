#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description of this module/script goes here
:param -f OR --first_parameter: The description of your first input parameter
:returns: Whatever your script returns when called
:raises Exception if any issues are encountered
"""

# Put all your imports here, one per line.
# However multiple imports from the same lib are allowed on a line.
# Imports from Python standard libraries
import sys
import logging
import os


# Imports from the cheese factory

# Imports from the local filesystem

# Put your constants here. These should be named in CAPS.

# Put your global variables here.

# Put your class definitions here. These should use the CapWords convention.

# Put your function definitions here. These should be lowercase, separated by underscores.
def scrape_all_current_tnt_jobs():
    """
    Scrape all the jobs currently listed on the Caribbean Jobs page for Trinidad and Tobago
    :return: A list of all the jobs listed
    """

def main():
    """Docstring description for each function"""
    try:
        # All main code here
        pass
    except Exception:
        logging.exception("Error in script " + os.path.basename(__file__))
        return 1
    else:
        logging.info(os.path.basename(__file__) + " executed successfully.")
        return 0


# If this script is being run from the command-line, then run the main() function
if __name__ == "__main__":
    main()
