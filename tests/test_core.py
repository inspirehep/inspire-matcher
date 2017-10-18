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

from inspire_matcher.core import _compile_exact


def test_compile_exact():
    query = {
        'match': 'arxiv_eprints.value',
        'search': 'arxiv_eprints.value.raw',
        'type': 'exact',
    }
    record = {
        'arxiv_eprints': [
            {
                'categories': [
                    'hep-th',
                ],
                'value': 'hep-th/9711200',
            },
        ],
    }

    expected = {
        'query': {
            'bool': {
                'minimum_should_match': 1,
                'should': [
                    {
                        'match': {
                            'arxiv_eprints.value.raw': 'hep-th/9711200',
                        },
                    },
                ],
            },
        },
    }
    result = _compile_exact(query, record)

    assert expected == result


def test_compile_exact_supports_a_collection():
    query = {
        'collections': [
            'HAL Hidden',
        ],
        'match': 'arxiv_eprints.value',
        'search': 'arxiv_eprints.value.raw',
        'type': 'exact',
    }
    record = {
        'arxiv_eprints': [
            {
                'categories': [
                    'hep-th',
                ],
                'value': 'hep-th/9711200',
            },
        ],
    }

    expected = {
        'query': {
            'bool': {
                'minimum_should_match': 1,
                'filter': {
                    'bool': {
                        'should': [
                            {
                                'match': {
                                    '_collections': 'HAL Hidden',
                                },
                            },
                        ],
                    },
                },
                'should': [
                    {
                        'match': {
                            'arxiv_eprints.value.raw': 'hep-th/9711200',
                        },
                    },
                ],
            },
        },
    }
    result = _compile_exact(query, record)

    assert expected == result


def test_compile_exact_supports_multiple_collections():
    query = {
        'collections': [
            'CDS Hidden',
            'HAL Hidden',
        ],
        'match': 'arxiv_eprints.value',
        'search': 'arxiv_eprints.value.raw',
        'type': 'exact',
    }
    record = {
        'arxiv_eprints': [
            {
                'categories': [
                    'hep-th',
                ],
                'value': 'hep-th/9711200',
            },
        ],
    }

    expected = {
        'query': {
            'bool': {
                'minimum_should_match': 1,
                'filter': {
                    'bool': {
                        'should': [
                            {
                                'match': {
                                    '_collections': 'CDS Hidden',
                                },
                            },
                            {
                                'match': {
                                    '_collections': 'HAL Hidden',
                                },
                            },
                        ],
                    },
                },
                'should': [
                    {
                        'match': {
                            'arxiv_eprints.value.raw': 'hep-th/9711200',
                        },
                    },
                ],
            },
        },
    }
    result = _compile_exact(query, record)

    assert expected == result


def test_compile_exact_supports_non_list_fields():
    query = {
        'match': 'reference.arxiv_eprint',
        'search': 'arxiv_eprints.value.raw',
        'type': 'exact',
    }
    reference = {
        'reference': {
            'arxiv_eprint': 'hep-th/9711200',
        },
    }

    expected = {
        'query': {
            'bool': {
                'minimum_should_match': 1,
                'should': [
                    {
                        'match': {
                            'arxiv_eprints.value.raw': 'hep-th/9711200',
                        },
                    },
                ],
            },
        },
    }
    result = _compile_exact(query, reference)

    assert expected == result
