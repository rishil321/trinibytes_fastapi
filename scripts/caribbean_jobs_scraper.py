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
import logging
import os
import logging.config
import math
# Imports from the cheese factory
import requests
from bs4 import BeautifulSoup

# Imports from the local filesystem
from .logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

# Put your constants here. These should be named in CAPS.
HTTP_GET_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# Put your global variables here.

# Put your class definitions here. These should use the CapWords convention.

# Put your function definitions here. These should be lowercase, separated by underscores.
def scrape_all_current_tnt_jobs():
    """
    Scrape all the jobs currently listed on the Caribbean Jobs page for Trinidad and Tobago
    :return: A list of the urls of all the jobs listed
    """
    try:
        # loop through all pages until we get all the jobs
        current_page_num = 1
        jobs_per_page = 100
        url = f'https://www.caribbeanjobs.com/ShowResults.aspx?Keywords=&autosuggestEndpoint=%2fautosuggest&Location' \
              f'=124&Category=&Recruiter=Company%2cAgency&btnSubmit=Search&PerPage={jobs_per_page}' \
              f'&Page={current_page_num} '
        response = requests.get(url, headers=HTTP_GET_HEADERS, verify=False)
        if response.status_code != 200:
            raise RuntimeError("Incorrect status code returned from caribbeanjobs.com")
        # else continue with our parsing
        # calculate how many pages we need to iterate through to get all jobs
        soup = BeautifulSoup(response.text, 'html.parser')
        sort_by_wrap = soup.find_all('div', 'sort-by-wrap')
        total_jobs = int(sort_by_wrap[0].findNext('label').text.split(": ")[1])
        total_pages = math.ceil(total_jobs / jobs_per_page)
        # then get all job urls in each page
        all_job_urls = []
        while (current_page_num <= total_pages):
            all_job_urls_soup = soup.find_all('div', 'job-result-title')
            for url in all_job_urls_soup:
                job_url = url.contents[1].contents[0].attrs['href']
                all_job_urls.append(job_url)
            logging.info(f"Added all URLs from page {current_page_num} of {total_pages}")
            # increment the page num
            current_page_num += 1
            # and get the next page of results
            url = f'https://www.caribbeanjobs.com/ShowResults.aspx?Keywords=&autosuggestEndpoint=%2fautosuggest' \
                  f'&Location=124&Category=&Recruiter=Company%2cAgency&btnSubmit=Search&Pe' \
                  f'rPage={jobs_per_page}&Page={current_page_num} '
            response = requests.get(url, headers=HTTP_GET_HEADERS, verify=False)
            if response.status_code != 200:
                raise RuntimeError("Incorrect status code returned from caribbeanjobs.com")
            soup = BeautifulSoup(response.text, 'html.parser')
        logging.info("Finished adding all currently listed URLs from caribbeanjobs.com")
        return all_job_urls
    except Exception as exc:
        logging.error("Error.", exc_info=exc)


def get_full_job_descriptions(all_job_urls):
    """
    Make an HTTP GET request to each job url on the caribbean jobs website and scrape the full details of
    each job post
    :param all_job_urls: A list of all the urls of all currently listed jobs on the website
    :return: A list of dictionaries, with each dictionary containing the full details of each job post
    """
    try:
        logging.info("Scraping full job descriptions from each job URL")
        for url in all_job_urls:
            full_url = 'https://www.caribbeanjobs.com/' + url
            response = requests.get(url, headers=HTTP_GET_HEADERS, verify=False)
            if response.status_code != 200:
                raise RuntimeError("Incorrect status code returned from caribbeanjobs.com")
            soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as exc:
        logging.error("Error.", exc_info=exc)


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
