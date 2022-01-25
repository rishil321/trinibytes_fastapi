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
    print(1+1)
    print(1+1)

def test_get_full_job_descriptions():
    sample_urls = []
