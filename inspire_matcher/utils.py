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


def compute_authors_jaccard_index(x_authors, y_authors):
    """Return the Jaccard similarity coefficient between 2 author sets.

    Args:
        x_authors (list(dict)): first schema-compliant list of authors.
        y_authors (list(dict)): second schema-compliant list of authors.

    Returns:
        float: Jaccard similarity coefficient between the 2 author sets.

    """
    intersection_cardinal = get_number_of_author_matches(x_authors, y_authors)
    union_cardinal = max(len(x_authors), len(y_authors))

    if union_cardinal:
        return intersection_cardinal / float(union_cardinal)
    else:
        return 0.0


def compute_titles_jaccard_index(x_title, y_title):
    """Return the Jaccard similarity coefficient between 2 titles.

    Args:
        x_title (string): first title.
        y_title (string): second title.

    Returns:
        float: Jaccard similarity coefficient between the 2 titles token sets.

    """
    record_title_tokens = get_tokenized_title(x_title)
    result_title_tokens = get_tokenized_title(y_title)

    intersection_cardinal = len(record_title_tokens & result_title_tokens)
    union_cardinal = len(record_title_tokens | result_title_tokens)

    if union_cardinal:
        return intersection_cardinal / float(union_cardinal)
    else:
        return 0.0


def get_tokenized_title(title):
    """Return the tokenised title.

    The title is lowercased and split on the spaces. Then, duplicate tokens are removed by adding the tokens to a set.

    Args:
        title (string): a titles.

    Returns:
        set: contains the resulting tokens.

    """
    return set(title.lower().split())
