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
    compute_author_match_score,
    compute_jaccard_index,
    get_tokenized_title,
)


def default_validator(record, result):
    return True


def authors_titles_validator(record, result):
    """Compute a validation score for the possible match.

    The score is based on a similarity score of the authors sets and the maximum Jaccard index found between 2 titles:
    one from the record and one from the result title sets.

    If the computed score is higher than 0.5, then the match is valid, otherwise it is not.

    Args:
        record (dict): the given record we are trying to match with similar ones in INSPIRE.
        result (dict): possible match returned by the ES query that needs to be validated.

    Returns:
        bool: validation decision.

    """
    record_authors = get_value(record, 'authors', [])
    result_authors = get_value(result, '_source.authors', [])

    author_score = compute_author_match_score(record_authors, result_authors)

    title_max_score = 0.0
    record_titles = get_value(record, 'titles.title', [])
    result_titles = get_value(result, '_source.titles.title', [])

    for cartesian_pair in product(record_titles, result_titles):
        record_title_tokens = get_tokenized_title(cartesian_pair[0])
        result_title_tokens = get_tokenized_title(cartesian_pair[1])
        current_title_jaccard = compute_jaccard_index(record_title_tokens, result_title_tokens)

        if current_title_jaccard > title_max_score and current_title_jaccard >= 0.5:
            title_max_score = current_title_jaccard

    return (author_score + title_max_score) / 2 > 0.5


def cds_identifier_validator(record, result):
    """Ensure that the two records have the same CDS identifier.

    This is needed because the search is done only for
    ``external_system_identifiers.value``, which might cause false positives in
    case the matched record has an identifier with the same ``value`` but
    ``schema`` different from CDS.

    Args:
        record (dict): the given record we are trying to match with similar ones in INSPIRE.
        result (dict): possible match returned by the ES query that needs to be validated.

    Returns:
        bool: validation decision.

    """

    record_external_identifiers = get_value(record, 'external_system_identifiers', [])
    result_external_identifiers = get_value(result, '_source.external_system_identifiers', [])

    record_external_identifiers = {external_id["value"] for external_id in record_external_identifiers if external_id["schema"] == 'CDS'}
    result_external_identifiers = {external_id["value"] for external_id in result_external_identifiers if external_id["schema"] == 'CDS'}

    return bool(record_external_identifiers & result_external_identifiers)
