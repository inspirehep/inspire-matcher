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

from inspire_matcher.utils import (
    compute_author_match_score,
    compute_jaccard_index,
    compute_title_score,
    get_number_of_author_matches,
    get_tokenized_title,
)


def test_get_number_of_author_matches():
    x_authors = [
        {"full_name": "Cabibbo, Nicola"},
        {"full_name": "Kobayashi, Makoto"},
        {"full_name": "Maskawa, Toshihide"},
    ]

    y_authors = [
        {"full_name": "Kobayashi, Makoto"},
        {"full_name": "Maskawa, Toshihide"},
    ]

    expected = 2
    result = get_number_of_author_matches(x_authors, y_authors)

    assert expected == result


def test_compute_author_match_score_matching_authors():
    x_authors = [
        {"full_name": "Cabibbo, Nicola"},
        {"full_name": "Kobayashi, Makoto"},
        {"full_name": "Maskawa, Toshihide"},
        {"full_name": "Smith, John"},
    ]
    y_authors = [
        {"full_name": "Cabibbo, Nicola"},
        {"full_name": "Kobayashi, Makoto"},
        {"full_name": "Maskawa, Toshihide"},
        {"full_name": "Smith, John"},
    ]

    result = compute_author_match_score(x_authors, y_authors)

    assert result == 1.0


def test_compute_author_match_score_different_authors():
    x_authors = [
        {"full_name": "Cabibbo, Nicola"},
        {"full_name": "Kobayashi, Makoto"},
        {"full_name": "Maskawa, Toshihide"},
        {"full_name": "Smith, John"},
    ]
    y_authors = [
        {"full_name": "Sinatra, Mary"},
        {"full_name": "Blueds, Michael"},
    ]

    result = compute_author_match_score(x_authors, y_authors)

    assert result == 0.0


def test_compute_author_match_score_similar_authors():
    x_authors = [
        {"full_name": "Cabibbo, Nicola"},
        {"full_name": "Kobayashi, Makoto"},
        {"full_name": "Maskawa, Toshihide"},
        {"full_name": "Smith, John"},
    ]
    y_authors = [
        {"full_name": "Kobayashi, Makoto"},
        {"full_name": "Maskawa, Toshihide"},
    ]

    result = compute_author_match_score(x_authors, y_authors)

    assert result == 0.5


@pytest.mark.parametrize(
    ("x_authors", "y_authors", "expected"),
    [
        (
            [
                {"full_name": "Kobayashi, Makoto"},
                {"full_name": "Maskawa, Toshihide"},
            ],
            [],
            1.0,
        ),
        (
            [],
            [
                {"full_name": "Kobayashi, Makoto"},
                {"full_name": "Maskawa, Toshihide"},
            ],
            1.0,
        ),
    ],
)
def test_compute_author_match_one_empty_list(x_authors, y_authors, expected):
    result = compute_author_match_score(x_authors, y_authors)

    assert result == expected


def test_compute_author_match_both_empty_list():
    x_authors = []
    y_authors = []

    result = compute_author_match_score(x_authors, y_authors)

    assert result == 0.0


def test_compute_jaccard_index_perfect_matching_titles():
    title1_tokens = {"cp", "violation", "in", "the", "b", "system"}
    title2_tokens = {"cp", "violation", "in", "the", "b", "system"}

    result = compute_jaccard_index(title1_tokens, title2_tokens)

    assert result == 1.0


def test_compute_jaccard_index_different_titles():
    title1_tokens = {"pythia", "6.4", "physics", "and", "manual"}
    title2_tokens = {"cp", "violation", "in", "the", "b", "system"}

    result = compute_jaccard_index(title1_tokens, title2_tokens)

    assert result == 0.0


def test_compute_jaccard_index_similar_titles():
    title1_tokens = {"cp", "violation", "b"}
    title2_tokens = {"cp", "violation", "in", "the", "b", "system"}

    result = compute_jaccard_index(title1_tokens, title2_tokens)

    assert result == 0.5


def test_compute_jaccard_index_one_empty_set():
    title1_tokens = {}
    title2_tokens = {"cp", "violation", "in", "the", "b", "system"}

    result = compute_jaccard_index(title1_tokens, title2_tokens)

    assert result == 0.0


def test_get_tokenized_title():
    title = "Exotic Exotic RG RG Flows from Holography"

    expected = {"exotic", "rg", "flows", "from", "holography"}

    result = get_tokenized_title(title)

    assert expected == result


def test_compute_title_score_below_threshold():
    title1 = "Some random title"
    title2 = "Some other different title"

    result = compute_title_score(title1, title2, threshold=0.5, math_threshold=0.3)

    assert result == 0.0


def test_compute_title_score_above_threshold():
    title1 = "Some random title"
    title2 = "Some other title"

    result = compute_title_score(title1, title2, threshold=0.5, math_threshold=0.3)

    assert result == 0.5


def test_compute_title_score_above_math_threshold():
    title1 = "Some $\\pi$ title"
    title2 = "Some other different title"

    result = compute_title_score(title1, title2, threshold=0.5, math_threshold=0.3)

    assert result == 0.4


def test_compute_title_score_below_math_threshold():
    title1 = "Some $\\pi$ title"
    title2 = "Some other title that really doesn't match at all"

    result = compute_title_score(title1, title2, threshold=0.5, math_threshold=0.3)

    assert result == 0.0
