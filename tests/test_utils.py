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

from inspire_matcher.utils import (
    compute_authors_jaccard_index,
    compute_titles_jaccard_index,
    get_number_of_author_matches,
    get_tokenized_title,
)


def test_get_number_of_author_matches():
    x_authors = [
        {'full_name': 'Cabibbo, Nicola'},
        {'full_name': 'Kobayashi, Makoto'},
        {'full_name': 'Maskawa, Toshihide'},
    ]
    y_authors = [
        {'full_name': 'Kobayashi, Makoto'},
        {'full_name': 'Maskawa, Toshihide'},
    ]

    expected = 2
    result = get_number_of_author_matches(x_authors, y_authors)

    assert expected == result


def test_get_tokenized_title():
    title = 'Exotic Exotic RG RG Flows from Holography'

    expected = {'exotic', 'rg', 'flows', 'from', 'holography'}

    result = get_tokenized_title(title)

    assert expected == result


def test_compute_authors_jaccard_index_perfect_matching_authors():
    author_list1 = [
        {
            'full_name': 'Smith, J.'
        },
        {
            'full_name': 'Zappacosta, L.',
        },
        {
            'full_name': 'Comastri, A.',
            'name_variations': [
                'comastri a',
                'comastri a.',
                'a comastri',
                'comastri',
                'comastri, a',
                'a. comastri',
                'comastri, a.',
                'a, comastri',
                'a., comastri'
            ]
        }
    ]

    author_list2 = [
        {
            'full_name': 'Smith, J.',
            'signature_block': 'SMITHJO',
        },
        {
            'full_name': 'Zappacosta, L.',
            'uuid': '2160fa69-9efa-44a9-bbe9-2121a8bd52e4'
        },
        {
            'full_name': 'Comastri, A.',
        }
    ]

    result = compute_authors_jaccard_index(author_list1, author_list2)

    assert result == 1.0


def test_compute_authors_jaccard_index_no_author_match():
    author_list1 = [
        {
            'full_name': 'Smith, J.'
        },
        {
            'full_name': 'Zappacosta, L.',
        },
        {
            'full_name': 'Black, S.',
            'signature_block': 'BLACKS',
        },
        {
            'full_name': 'Comastri, A.',
            'name_variations': [
                'comastri a',
                'comastri a.',
                'a comastri',
                'comastri',
                'comastri, a',
                'a. comastri',
                'comastri, a.',
                'a, comastri',
                'a., comastri'
            ]
        }
    ]

    author_list2 = [
        {
            'full_name': 'Roberts, A.',
        }
    ]

    result = compute_authors_jaccard_index(author_list1, author_list2)

    assert result == 0.0


def test_compute_authors_jaccard_index_half_authors_match():
    author_list1 = [
        {
            'full_name': 'Smith, J.'
        },
        {
            'full_name': 'Zappacosta, L.',
        },
        {
            'full_name': 'Black, S.',
            'signature_block': 'BLACKS',
        },
        {
            'full_name': 'Comastri, A.',
            'name_variations': [
                'comastri a',
                'comastri a.',
                'a comastri',
                'comastri',
                'comastri, a',
                'a. comastri',
                'comastri, a.',
                'a, comastri',
                'a., comastri'
            ]
        }
    ]

    author_list2 = [
        {
            'full_name': 'Smith, J.',
            'signature_block': 'SMITHJO',
        },
        {
            'full_name': 'Zappacosta, L.',
            'name_variations': [
                'zappacosta l',
                'zappacosta l.',
                'l zappacosta',
                'zappacosta',
                'zappacosta, l',
                'l. zappacosta',
                'zappacosta, l.',
                'l, zappacosta',
                'l., zappacosta'
            ]
        },
    ]

    result = compute_authors_jaccard_index(author_list1, author_list2)

    assert result == 0.5


def test_compute_titles_jaccard_index_perfect_matching_titles():
    title1 = 'CP VIOLATION IN THE B SYSTEM'
    title2 = 'cp violation in the b system'

    result = compute_titles_jaccard_index(title1, title2)

    assert result == 1.0


def test_compute_titles_jaccard_index_different_titles():
    title1 = 'PYTHIA 6.4 Physics and Manual'
    title2 = 'cp violation in the b system'

    result = compute_titles_jaccard_index(title1, title2)

    assert result == 0.0


def test_compute_titles_jaccard_index_similar_titles():
    title1 = 'CP violation B'
    title2 = 'CP violation in the B system'

    result = compute_titles_jaccard_index(title1, title2)

    assert result == 0.5
