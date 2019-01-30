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
    cds_identifier_validator,
    default_validator,
)


def test_default_validator_is_not_very_exciting():
    assert default_validator(None, None)


def test_authors_titles_validator_does_match_when_authors_are_same_and_titles_contain_perfect_match():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'harvest_record_1601.02340.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_result_1601.02340.json')))

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_does_not_match_when_authors_are_similar_but_titles_are_too_different():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'harvest_record_1804.09082.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_wrong_result_1211.4028.json')))

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_does_not_match_when_authors_are_same_but_titles_are_too_different():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'harvest_record_1712.05946.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_wrong_result_10.1103.json')))

    assert not authors_titles_validator(record, result)


def test_cds_identifier_validator_does_match_when_external_system_identifiers_contain_perfect_match():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'harvest_record_2654944.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_result_2654944.json')))

    assert cds_identifier_validator(record, result)


def test_cds_identifier_validator_does_not_match_when_system_identifiers_are_from_different_sources():
    record = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'harvest_record_2654944.json')))

    result = json.loads(pkg_resources.resource_string(
        __name__, os.path.join('fixtures', 'matching_wrong_2654944.json')))

    assert not cds_identifier_validator(record, result)
