import os
import pytest
from pathlib import Path

from scripts import caribbean_jobs_scraper


def test_main():
    caribbean_jobs_scraper.main()
    print("meep")


def test_scrape_all_current_tnt_jobs():
    result = caribbean_jobs_scraper.scrape_all_current_tnt_jobs()
    assert len(result)>0
    assert isinstance(result,list)
    assert isinstance(result[0],str)
    assert result[0] != ''

def test_get_full_job_descriptions():
    sample_urls = ['/Diagnostic-Radiographer-Job-134606.aspx?p=1|application_confirmed','/Operations-Manager-Job-134746.aspx']
    result = caribbean_jobs_scraper.get_full_job_descriptions(sample_urls)
    assert len(result) > 0
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert result[0] != {}
