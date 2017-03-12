import re
JOB_REGEX = re.compile('(no vacancies|No jobs)', re.IGNORECASE | re.UNICODE | re.MULTILINE)
JOB_CSS_SEARCH_LIST = ['.job-list', '.list', '.view-content', '.jv-page-body']
