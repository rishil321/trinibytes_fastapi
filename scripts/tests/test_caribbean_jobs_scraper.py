import os
import pytest
from pathlib import Path

from scripts import caribbean_jobs_scraper


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
    result = caribbean_jobs_scraper.get_full_job_descriptions(sample_urls)
    assert len(result) > 0
    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert result[0] != {}


def test_write_full_job_descriptions_to_db():
    sample_full_job_descriptions = [
        {'url': 'https://www.caribbeanjobs.com/Diagnostic-Radiographer-Job-134606.aspx?p=1|application_confirmed',
         'company_name': 'not disclosed', 'job_title': 'Diagnostic Radiographer', 'caribbeanjobs_job_id': '134606',
         'job_category': 'medical professionals & healthcare', 'job_location': 'port-of-spain|castries|georgetown',
         'job_salary': 'Not disclosed', 'job_min_education_requirement': 'degree',
         'full_job_description': '\nThe successful candidates will specialize in general radiography as well as the CT and/or MRI modalities while ensuring the privacy, comfort and safety of all patients in a professional and caring manner.\nDiagnostic Radiology Services, an established group of diagnostic clinics in Barbados, is inviting suitably qualified persons to apply for the position of:\xa0Radiographer\xa0The successful candidates will specialize in general radiography as well as the CT and/or MRI modalities while ensuring the privacy, comfort and safety of all patients in a professional and caring manner.Key responsibilities include:\xa0Ensuring the safe use and maintenance of highly specialist imaging equipment; adhering to all CT, MRI and radiography safety procedures; and reporting problems to the Medical Imaging Manager and the engineering support teamMaintaining a positive partnership and continuity of service at all times with all affiliate healthcare institutions that contract our services.Observing all technical and organizational standards and protocols (including those related to safety and health); functioning in accordance with best practice and in a manner that meets professional, departmental and legal standards and requirements.Cooperating with the Company in ensuring that all infection prevention and control policies and procedures are complied with.Responding to the clinical requests of the Medical Imaging Manager and Consultant Radiologists.Conducting screening safety checks with patients prior to examination, to obtain consent and ensure their suitability for imaging examinations.Obtaining consent and conducting safety checks prior to a patient being administered contrast media and/or drugs specific to their examination.Adhering to policies, procedures and protocols within the department.Responding to out-of-hours emergency call-outs on nights and weekends as they arise.\xa0The successful candidate will possess the following skills and qualifications:At least three (3) years of relevant practical experience.ARRT, DCR, BSc or equivalent qualification in Diagnostic Radiography from an accredited institution.Up-to-date registration with the Barbados Paramedical Council (or other professional registration body if not resident in Barbados).Certification to undertake cannulation procedures and administration of contrast media and drugs in accordance with standard intravenous (IV) cannulation and contrast administration policies.BLS or ACLS certification would be an asset.\xa0Personal attributes:Patient-focused with exceptional interpersonal skillsStrong work ethic and professional demeanourExcellent written and oral communication skillsMeticulous nature and keen eye for detailAble to exercise sound judgment in times of crisisAble and willing to work closely and effectively with technical radiology team, inclusive of fellow radiographers as well as radiologists and administrative staff\xa0Applications, accompanied by up-to-date CVs and the names of two referees should be submitted no later than February 18th 2022 `Only suitable applications will be acknowledged.\n'},
        {'url': 'https://www.caribbeanjobs.com/Operations-Manager-Job-134746.aspx',
         'company_name': 'eve anderson recruitment ltd', 'job_title': 'Operations Manager',
         'caribbeanjobs_job_id': '134746', 'job_category': 'management', 'job_location': 'tunapuna/piarco|trincity',
         'job_salary': '10000 - 20000', 'job_min_education_requirement': 'masters degree',
         'full_job_description': "\nOur client in Distribution (Food) Sector is seeking to hire an Operations Manager.\nJob SummaryOur client in Distribution (Food) Sector is seeking to hire an Operations ManagerDirects, administers, and coordinates the internal operational activities of the organization in accordance with policies, goals, and objectives established by the Chief Executive Officer and the Board of Directors. Leads and directs the following functions and/or business units: operations, human resources, information systems, traffic, new business coordination, and agency promotion and communication. Assists the CEO in the development of organization policies and goals that cover operations, personnel, financial performance, and growth of the functions and/or business units mentioned above.Job DutiesPlans, develops and establishes strategy, programmes and systems for all store operations.Develops and implements checks and controls to ensure budgetary targets are met and implement shrink control measures.Monitors, measures and reports on store operational issues, opportunities, development plans and achievements.Manages and controls overall store expenditure within agreed budgets.Ensures overall store activities comply with and integrate with organisation's requirements for quality management, health and safety, legal stipulations and environmental policies.Ensures the efficient labour scheduling and proper staffing in the Stores are geared to meet customer requirements.Co-ordinates and monitors the maintenance of the stores physical appearanceSelects, develops and monitors the effective utilization of Store Managers.Evaluates the results of store operations regularly and systematically.Direct an organization's security functions, including physical security and safety of employees, facilities, and assets.Performs other duties as required by the job function.Job RequirementsMasters in Business Administration (MBA) or M.Sc. Degree in related discipline.Professional Certification from recognized Institution in retail management.Minimum: Two (5) years' experience in a similar positionEffective Leadership competenciesSound Managerial competenciesBusiness KnowledgeSound Analytical and Problem Solving SkillsProficient in Ms. OfficeIntermediate skills in retail management software.Familiarity with computerized applications, Excel, Word, Email etc .\n"},
    ]
    result = caribbean_jobs_scraper.write_full_job_descriptions_to_db(sample_full_job_descriptions)
    print('meep')
