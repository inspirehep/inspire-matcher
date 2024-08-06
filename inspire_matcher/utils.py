# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by
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

from inspire_json_merger.comparators import AuthorComparator


def get_number_of_author_matches(x_authors, y_authors):
    """Return the number of matches between two lists of authors.

    Args:
        x_authors (list(dict)): a schema-compliant list of authors.
        y_authors (list(dict)): another schema-compliant list of authors.

    Returns:
        int: the number of matching authors between the two lists.

    """
    return len(AuthorComparator(x_authors, y_authors).matches)


def compute_author_match_score(x_authors, y_authors):
    """Return the matching score of 2 given lists of authors.

    Args:
        x_authors (list(dict)): first schema-compliant list of authors.
        y_authors (list(dict)): second schema-compliant list of authors.

    Returns:
        float: matching score of authors.

    """
    if not x_authors and not y_authors:
        return 0.0

    if not x_authors or not y_authors:
        return 1.0

    matches = get_number_of_author_matches(x_authors, y_authors)
    max_length = max(len(x_authors), len(y_authors))

    return matches / float(max_length)


def compute_jaccard_index(x_set, y_set):
    """Return the Jaccard similarity coefficient of 2 given sets.

    Args:
        x_set (set): first set.
        y_set (set): second set.

    Returns:
        float: Jaccard similarity coefficient.

    """
    if not x_set or not y_set:
        return 0.0

    intersection_cardinal = len(x_set & y_set)
    union_cardinal = len(x_set | y_set)

    return intersection_cardinal / float(union_cardinal)


def get_tokenized_title(title):
    """Return the tokenised title.

    The title is lowercased and split on the spaces. Then, duplicate
        tokens are removed by adding the tokens to a set.

    Args:
        title (string): a title.

    Returns:
        set: contains the resulting tokens.

    """
    return set(title.lower().split())


def compute_title_score(x_title, y_title, threshold, math_threshold):
    """Compute a score for a pair of titles.

    Args:
        x_title (string): one title.
        y_title (string): the other title.
        threshold (float): minimum overlap for the score to be non-zero in general.
        math_threshold (float): minimum overlap for the score to be
            non-zero in the presence of math in any of the titles.

    Returns:
        float: a score indicating the overlap of both titles, which is ``0`` if
            below the threshold
    """
    x_title_tokens = get_tokenized_title(x_title)
    y_title_tokens = get_tokenized_title(y_title)
    current_title_jaccard = compute_jaccard_index(x_title_tokens, y_title_tokens)

    some_title_has_math = (
        "<math>" in x_title or "$" in x_title or "<math>" in y_title or "$" in y_title
    )
    current_threshold = math_threshold if some_title_has_math else threshold

    return current_title_jaccard if current_title_jaccard >= current_threshold else 0.0
