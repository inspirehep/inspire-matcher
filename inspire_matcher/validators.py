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

"""Matcher validators."""

from __future__ import absolute_import, division, print_function

from itertools import product

from inspire_utils.record import get_value

from .utils import (
    compute_authors_jaccard_index,
    compute_titles_jaccard_index,
)


def default_validator(record, result):
    return True


def authors_titles_validator(record, possible_match):
    """Compute a validation score for the possible match.

    The score is based on the Jaccard index of the authors sets and the maximum Jaccard index found between 2 titles from
    the record and the possible match title sets.

    The default score is 0.5. If the computed score is higher than this, then the match is valid, otherwise it is not.

    Args:
        record (dict): the given record we are trying to match with similar ones in INSPIRE.
        possible_match (dict): possible match returned by the ES query that needs to be validated.

    Returns:
        bool: validation decision.

    """
    author_score = 0.5
    record_authors = get_value(record, 'authors', [])
    result_authors = get_value(possible_match, '_source.authors', [])

    if record_authors and result_authors:
        record_sample_nr = min(len(record_authors), 5)
        match_sample_nr = min(len(result_authors), 5)
        author_score = compute_authors_jaccard_index(record_authors[:record_sample_nr], result_authors[:match_sample_nr])

    title_max_score = 0.5
    record_titles = get_value(record, 'titles.title', [])
    result_titles = get_value(possible_match, '_source.titles.title', [])

    if record_titles and result_titles:
        for cartesian_pair in product(record_titles, result_titles):
            current_title_jaccard = compute_titles_jaccard_index(cartesian_pair[0], cartesian_pair[1])

            if current_title_jaccard > title_max_score:
                title_max_score = current_title_jaccard

    return (author_score + title_max_score) / 2 > 0.5
