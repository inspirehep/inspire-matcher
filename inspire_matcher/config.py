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

"""Matcher configuration."""

from __future__ import absolute_import, division, print_function


MATCHER_DEFAULT_CONFIGURATION = {
    'algorithm': [
        {
            'queries': [
                {
                    'path': 'arxiv_eprints.value',
                    'search_path': 'arxiv_eprints.value.raw',
                    'type': 'exact',
                },
                {
                    'path': 'dois.value',
                    'search_path': 'dois.value.raw',
                    'type': 'exact',
                },
            ],
        },
    ],
    'doc_type': 'hep',
    'index': 'records-hep',
}
"""Default configuration of the matcher."""
