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
