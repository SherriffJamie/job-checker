import re
JOB_REGEX = re.compile('no vacancies', re.IGNORECASE | re.UNICODE | re.MULTILINE)
JOB_CSS_SEARCH_LIST = ['.job-list']