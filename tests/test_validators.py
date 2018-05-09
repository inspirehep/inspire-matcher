# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

import json
import os
import pkg_resources

from inspire_matcher.validators import (
    authors_titles_validator,
    default_validator,
)


def test_default_validator_is_not_very_exciting():
    assert default_validator(None, None)


def test_authors_titles_validator_matching_result_1():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_1.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_result_1.json')))

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_2():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_2.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_result_2.json')))

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_3():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_3.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_result_3.json')))

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_4():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_4.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_result_4.json')))

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_5():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_5.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_result_5.json')))

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_6():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_6.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_result_6.json')))

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_7():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_7.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_wrong_result_7.json')))

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_8():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_8.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_wrong_result_8.json')))

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_9():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_9.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_wrong_result_9.json')))

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_10():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_10.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_wrong_result_10.json')))

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_11():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_11.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_wrong_result_11.json')))

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_matching_result_12():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'record_12.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_wrong_result_12.json')))

    assert not authors_titles_validator(record, result)
