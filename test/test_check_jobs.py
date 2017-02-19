import os, sys, inspect
import re

# TODO figure out better approach than this
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import constants

test_string = "Current job offers Sorry, there are currently no vacancies You can send us your CV anyway and we'll " \
              "contact you if a position that matches your qualifications becomes vacant. Submit your CV"
fail_test_string = "lots of jobs on offer"


def test_regex_type():
    assert isinstance(re.compile(''), type(constants.job_regex))


def test_regex_match_type():
    match = constants.job_regex.search(test_string)
    assert isinstance(re.match('', ''), type(match))


def test_regex_match():
    match = constants.job_regex.search(test_string)
    assert match


def test_regex_match_fail():
    match = constants.job_regex.search(fail_test_string)
    assert not match
