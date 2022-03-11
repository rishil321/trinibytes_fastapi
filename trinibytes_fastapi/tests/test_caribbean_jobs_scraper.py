import os
import pytest
from pathlib import Path
import models

import trinibytes_fastapi.trinibytes_fastapi.caribbean_jobs_scraper as caribbean_jobs_scraper


def test_main():
    caribbean_jobs_scraper.main()
    print("meep")


def test_scrape_all_current_tnt_jobs():
    result = caribbean_jobs_scraper.scrape_all_current_tnt_jobs()
    assert len(result) > 0
    assert isinstance(result, list)
    assert isinstance(result[0], str)
    assert result[0] != ''


def test_get_full_job_descriptions():
    sample_urls = ['/Diagnostic-Radiographer-Job-134606.aspx?p=1|application_confirmed',
                   '/Operations-Manager-Job-134746.aspx']
    result = caribbean_jobs_scraper.parse_all_job_posts(sample_urls)
    assert len(result) > 0
    assert isinstance(result, list)
    assert isinstance(result[0], models.CaribbeanJobsPost)


def test_write_full_job_descriptions_to_db():
    sample_full_job_descriptions = [
        models.CaribbeanJobsPost(caribbeanjobs_job_id='1', full_job_description='Testing',
                                 job_category="medical professionals", job_company='N/A', job_location='N/A',
                                 job_title='RAdio',
                                 url='https://www.caribbeanjobs.com/Diagnostic-Radiographer-Job-134606.aspx?p=1|application_confirmed'), ]
    result = caribbean_jobs_scraper.write_parsed_job_data_to_db(sample_full_job_descriptions)
    print('meep')


def test_update_inactive_jobs_in_db():
    sample_full_job_descriptions = [
        models.CaribbeanJobsPost(caribbeanjobs_job_id='1', full_job_description='Testing',
                                 job_category="medical professionals", job_company='N/A', job_location='N/A',
                                 job_title='RAdio',
                                 url='https://www.caribbeanjobs.com/Diagnostic-Radiographer-Job-134606.aspx?p=1|application_confirmed'), ]
    result = caribbean_jobs_scraper.update_inactive_job_posts(sample_full_job_descriptions)
    print('meep')
