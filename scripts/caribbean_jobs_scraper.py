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
import sys
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

# Imports from the local filesystem
from database import engine
import models as models
from logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

# Put your constants here. These should be named in CAPS.
HTTP_GET_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


# Put your global variables here.

# Put your class definitions here. These should use the CapWords convention.

# Put your function definitions here. These should be lowercase, separated by underscores.
def scrape_all_current_tnt_jobs() -> List[str]:
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
        response = requests.get(url, headers=HTTP_GET_HEADERS, verify=True)
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
            response = requests.get(url, headers=HTTP_GET_HEADERS, verify=True)
            if response.status_code != 200:
                raise RuntimeError("Incorrect status code returned from caribbeanjobs.com")
            soup = BeautifulSoup(response.text, 'html.parser')
        logging.info("Finished adding all currently listed URLs from caribbeanjobs.com")
        return all_job_urls
    except Exception as exc:
        logging.error("Error.", exc_info=exc)


def parse_all_job_posts(all_job_urls: List[str]) -> List[models.CaribbeanJobsPost]:
    """
    Make an HTTP GET request to each job url on the caribbean jobs website and scrape the full details of
    each job post, then create CaribbeanJobPost ORM objects for each post
    :param all_job_urls: A list of all the urls of all currently listed jobs on the website
    :return: A list of objects of the CaribbeanJobsPost model
    """
    try:
        logging.info("Scraping full job descriptions from each job URL")
        all_parsed_job_posts = []
        for url in all_job_urls:
            full_url = 'https://www.caribbeanjobs.com' + url
            response = requests.get(full_url, headers=HTTP_GET_HEADERS, verify=True)
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
                    job_post_details['company_name'] = detail.split(':')[1].replace(",", "").replace('\"', '').title()
                elif 'job__title' in detail:
                    job_post_details['job_title'] = detail.split(':')[1].replace(",", "").replace('\"', '').title()
                elif 'job_id' in detail:
                    job_post_details['caribbeanjobs_job_id'] = detail.split(':')[1].replace(",", "").replace('\"', '')
                elif 'primary_category_name' in detail:
                    job_post_details['job_category'] = detail.split(':')[1].replace(",", "").replace('\"', '').title()
                elif 'job__location' in detail:
                    job_post_details['job_location'] = detail.split(':')[1].replace(",", "").replace('\"', '').title()
                elif 'salary_range' in detail:
                    job_post_details['job_salary'] = detail.split(':')[1].replace(",", "").replace('\"', '')
                elif 'min_education' in detail:
                    job_post_details['job_min_education_requirement'] = detail.split(':')[1].replace(",", "").replace(
                        '\"', '').title()
            job_post_details['full_job_description'] = full_job_detail_node.text
            # create a new object for the db model
            job_post = models.CaribbeanJobsPost(url=job_post_details['url'],
                                                caribbeanjobs_job_id=job_post_details['caribbeanjobs_job_id'],
                                                job_title=job_post_details['job_title'],
                                                job_company=job_post_details['company_name'],
                                                job_category=job_post_details['job_category'],
                                                job_location=job_post_details['job_location'],
                                                job_salary=job_post_details['job_salary'],
                                                job_min_education_requirement=job_post_details[
                                                    'job_min_education_requirement'],
                                                full_job_description=job_post_details['full_job_description'])
            all_parsed_job_posts.append(job_post)
            logging.debug(
                f"Successfully added details for {job_post_details['job_title']} from {job_post_details['company_name']}.")
        logging.info("All full job descriptions added successfully")
        return all_parsed_job_posts
    except Exception as exc:
        logging.error("Error.", exc_info=exc)
        return []


def update_inactive_job_posts(parsed_job_post_data: List[models.CaribbeanJobsPost]) -> int:
    """
    Get all the active jobs currently in the db, and check if any of these jobs
    are no longer listed on the website, based on our parsed current job post data
    :param parsed_job_post_data: A list of CaribbeanJobsPost objects scraped from the website
    :return: 0 if successfully updated, else -1
    """
    session = None
    try:
        logging.info("Now updating active/inactive jobs in database.")
        Session = sessionmaker(bind=engine)
        session = Session()
        all_active_job_posts_in_db = session.query(models.CaribbeanJobsPost).filter(
            models.CaribbeanJobsPost.job_listing_is_active).all()
        # create a list of caribbean_job ids of all the scraped/parsed job posts
        all_parsed_job_post_ids = []
        for job_post_data in parsed_job_post_data:
            all_parsed_job_post_ids.append(int(job_post_data.caribbeanjobs_job_id))
        for db_job_post in all_active_job_posts_in_db:
            if db_job_post.caribbeanjobs_job_id in all_parsed_job_post_ids:
                logging.debug(
                    f"Job post: {db_job_post.job_title} from {db_job_post.job_company} is still actively listed.")
            else:
                # mark the job as inactive
                logging.debug(f"Job post: {db_job_post.job_title} from {db_job_post.job_company} is no longer listed.")
                db_job_post.job_listing_is_active = False
                db_job_post.job_delisting_date = datetime.now()
                session.commit()
        return 0
    except Exception as exc:
        logging.error("Error.", exc_info=exc)
        return -1
    finally:
        if session:
            session.expunge_all()
            session.close()


def write_parsed_job_data_to_db(parsed_job_post_data: List[models.CaribbeanJobsPost]) -> int:
    """
    Writes the list of CaribbeanJobsPost objects to the db
    :param parsed_job_post_data: A list of models.CaribbeanJobsPost objects from the db
    :return: 0 is successful, else -1
    """
    session = None
    try:
        logging.info("Now updating/inserting all current caribbean job posts into the db")
        Session = sessionmaker(bind=engine)
        session = Session()
        for job_post_data in parsed_job_post_data:
            # check if the job post has been added already
            # job_post_in_db = session.execute(select(models.CaribbeanJobsPost).where(
            #    models.CaribbeanJobsPost.caribbeanjobs_job_id == job_post_data.caribbeanjobs_job_id)).first()
            job_post_in_db = session.query(models.CaribbeanJobsPost).filter(
                models.CaribbeanJobsPost.caribbeanjobs_job_id == job_post_data.caribbeanjobs_job_id).first()
            if job_post_in_db:
                # then update the row in the database
                logging.debug(
                    f"Job found in db: {job_post_in_db.job_title} from {job_post_in_db.job_company}. Updating.")
                job_post_in_db.job_title = job_post_data.job_title
                job_post_in_db.job_company = job_post_data.job_company
                job_post_in_db.job_category = job_post_data.job_category
                job_post_in_db.job_location = job_post_data.job_location
                job_post_in_db.job_salary = job_post_data.job_salary
                job_post_in_db.job_min_education_requirement = job_post_data.job_min_education_requirement
                session.commit()
            else:
                # else this is a new job to add to the db
                session.add(job_post_data)
                session.commit()
        # with engine.connect() as conn:
        #     conn = conn.execution_options(
        #         isolation_level="AUTOCOMMIT"
        #     )
        #     with conn.begin():
        #         metadata_obj = MetaData()
        #         metadata_obj.reflect(bind=engine)
        #         caribbeanjobs_posts_table = metadata_obj.tables['caribbeanjobs_posts']
        #         insert_stmt = insert(caribbeanjobs_posts_table).values(full_job_descriptions)
        #         do_update_stmt = insert_stmt.on_conflict_do_update(
        #             index_elements=['caribbeanjobs_job_id'],
        #             set_={"full_job_description": insert_stmt.excluded.full_job_description, }
        #         )
        #         conn.execute(do_update_stmt)
        logging.info("All records inserted into db successfully.")
        return 0
    except Exception as exc:
        logging.error("Error.", exc_info=exc)
        return -1
    finally:
        if session:
            session.expunge_all()
            session.close()


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
        full_job_data = parse_all_job_posts(all_active_job_posts)
        if not full_job_data:
            raise RuntimeError("Error while fetching full job descriptions from caribbeanjobs.com")
        # then write the jobs to the database
        result_code = write_parsed_job_data_to_db(full_job_data)
        if result_code != 0:
            raise RuntimeError("Error while writing data to db.")
        # then check which jobs are no longer actively listed
        result_code = update_inactive_job_posts(full_job_data)
        if result_code != 0:
            raise RuntimeError("Error while updating inactive jobs in db.")
    except Exception as exc:
        logging.error("Error in script " + os.path.basename(__file__), exc_info=exc)
        sys.exit(1)
    else:
        logging.info(os.path.basename(__file__) + " executed successfully.")
        return 0


# If this script is being run from the command-line, then run the main() function
if __name__ == "__main__":
    main()
