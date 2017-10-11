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

import pytest

from inspire_matcher.api import match


def test_match_raises_if_the_configuration_does_not_have_all_the_keys():
    config = {
        'doc_type': 'records',
        'index': 'records-hep',
    }

    with pytest.raises(KeyError) as excinfo:
        list(match(None, config))
    assert 'Malformed configuration' in str(excinfo.value)


def test_match_raises_if_one_step_of_the_algorithm_has_no_queries():
    config = {
        'algorithm': [
            {'validator': 'inspire_matcher.validators:default_validator'},
        ],
        'doc_type': 'records',
        'index': 'records-hep',
    }

    with pytest.raises(KeyError) as excinfo:
        list(match(None, config))
    assert 'Malformed algorithm' in str(excinfo.value)


def test_match_raises_if_one_query_does_not_have_a_type():
    config = {
        'algorithm': [
            {
                'queries': [
                    {},
                ],
            },
        ],
        'doc_type': 'records',
        'index': 'records-hep',
    }

    with pytest.raises(ValueError) as excinfo:
        list(match(None, config))
    assert 'Malformed query' in str(excinfo.value)


def test_match_raises_if_one_query_type_is_not_supported():
    config = {
        'algorithm': [
            {
                'queries': [
                    {'type': 'not-supported'},
                ],
            },
        ],
        'doc_type': 'records',
        'index': 'records-hep',
    }

    with pytest.raises(ValueError) as excinfo:
        list(match(None, config))
    assert 'Malformed query' in str(excinfo.value)


def test_match_raises_if_an_exact_query_does_not_have_all_the_keys():
    config = {
        'algorithm': [
            {
                'queries': [
                    {
                        'search': 'arxiv_eprints.value.raw',
                        'type': 'exact',
                    },
                ],
            },
        ],
        'doc_type': 'records',
        'index': 'records-hep',
    }

    with pytest.raises(ValueError) as excinfo:
        list(match(None, config))
    assert 'Malformed query' in str(excinfo.value)
