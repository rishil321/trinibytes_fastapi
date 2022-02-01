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
import re
# Imports from the cheese factory
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import insert

# Imports from the local filesystem
from .logging_config import LOGGING_CONFIG
import models

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
        logging.info(f"Total jobs currently listed: {total_jobs}")
        # then get all job urls in each page
        all_job_urls = []
        while current_page_num <= total_pages:
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
        full_job_descriptions = []
        for url in all_job_urls:
            full_url = 'https://www.caribbeanjobs.com' + url
            response = requests.get(full_url, headers=HTTP_GET_HEADERS, verify=False)
            if response.status_code != 200:
                raise RuntimeError("Incorrect status code returned from caribbeanjobs.com")
            soup = BeautifulSoup(response.text, 'html.parser')
            # find the javascript node containing all the juicy job details
            javascript_detail_node = soup.find('script', text=re.compile(r'\bdigitalData\b'))
            # also find the main node containing the main job data
            full_job_detail_node = soup.find('div', 'job-details')
            # now pull the data from these nodes and add them to our dict
            job_post_details = {
                'url': full_url
            }
            for detail in javascript_detail_node.text.split('\r\n'):
                if 'company_name' in detail:
                    job_post_details['company_name'] = detail.split(':')[1].replace(",", "").replace('\"', '')
                elif 'job__title' in detail:
                    job_post_details['job_title'] = detail.split(':')[1].replace(",", "").replace('\"', '')
                elif 'job_id' in detail:
                    job_post_details['caribbeanjobs_job_id'] = detail.split(':')[1].replace(",", "").replace('\"', '')
                elif 'primary_category_name' in detail:
                    job_post_details['job_category'] = detail.split(':')[1].replace(",", "").replace('\"', '')
                elif 'job__location' in detail:
                    job_post_details['job_location'] = detail.split(':')[1].replace(",", "").replace('\"', '')
                elif 'salary_range' in detail:
                    job_post_details['job_salary'] = detail.split(':')[1].replace(",", "").replace('\"', '')
                elif 'min_education' in detail:
                    job_post_details['job_min_education_requirement'] = detail.split(':')[1].replace(",", "").replace(
                        '\"', '')
            job_post_details['full_job_description'] = full_job_detail_node.text
            full_job_descriptions.append({'caribbeanjobs_job_id': job_post_details['caribbeanjobs_job_id'],
                                          'url': job_post_details['url'],
                                          'job_title': job_post_details['job_title'],
                                          'job_company': job_post_details['company_name'],
                                          'job_category': job_post_details['job_category'],
                                          'job_location': job_post_details['job_location'],
                                          'job_salary': job_post_details['job_salary'],
                                          'job_min_education_requirement': job_post_details[
                                              'job_min_education_requirement'],
                                          'full_job_description': job_post_details['full_job_description'],
                                          })
            logging.info(f"Successfully added details for {job_post_details['job_title']} from {job_post_details['company_name']}.")
        logging.info("All full job descriptions added successfully")
        return full_job_descriptions
    except Exception as exc:
        logging.error("Error.", exc_info=exc)
        return []


def write_full_job_descriptions_to_db(full_job_descriptions):
    try:
        postgres_user = 'postgres'
        postgres_password = 'postgres'
        if 'POSTGRES_USER' in os.environ:
            postgres_user = os.environ['POSTGRES_USER']
            logging.info("Postgres username found in environ")
        if 'POSTGRES_PASSWORD' in os.environ:
            postgres_password = os.environ['POSTGRES_PASSWORD']
        db_string = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@postgres:5432/trinibytes_db"
        db_engine = create_engine(db_string, pool_pre_ping=True)
        logging.info("Now writing all current caribbean jobs descriptions to the db")
        with db_engine.connect() as conn:
            conn = conn.execution_options(
                isolation_level="AUTOCOMMIT"
            )
            with conn.begin():
                metadata_obj = MetaData()
                metadata_obj.reflect(bind=db_engine)
                caribbeanjobs_posts_table = metadata_obj.tables['caribbeanjobs_posts']
                insert_stmt = insert(caribbeanjobs_posts_table).values(full_job_descriptions)
                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=['caribbeanjobs_job_id'],
                    set_={"full_job_description": insert_stmt.excluded.full_job_description, }
                )
                conn.execute(do_update_stmt)
        # Session = sessionmaker(bind=db_engine)
        # session = Session()
        # session.add_all(full_job_descriptions)
        # session.commit()
        logging.info("All records inserted into db successfully.")
        return 0
    except Exception as exc:
        logging.error("Error.", exc_info=exc)
        return -1


def main():
    """
    The main logic to execute the sequence of functions when the script is run.
    :return:
    """
    try:
        # All main code here
        all_active_job_posts = scrape_all_current_tnt_jobs()
        if not all_active_job_posts:
            raise RuntimeError("Error while fetching all active job posts from caribbeanjobs.com")
        # then go to the url of each job post and scrape the full data
        full_job_data = get_full_job_descriptions(all_active_job_posts)
        if not full_job_data:
            raise RuntimeError("Error while fetching full job descriptions from caribbeanjobs.com")
        # then write the jobs to the database
        result_code = write_full_job_descriptions_to_db(full_job_data)
        if result_code != 0:
            raise RuntimeError("Error while writing data to db.")
    except Exception as exc:
        logging.error("Error in script " + os.path.basename(__file__), exc_info=exc)
        return -1
    else:
        logging.info(os.path.basename(__file__) + " executed successfully.")
        return 0


# If this script is being run from the command-line, then run the main() function
if __name__ == "__main__":
    main()
