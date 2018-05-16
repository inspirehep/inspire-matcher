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

import os

from inspire_utils.helpers import force_list
from inspire_utils.record import get_value


def compile(query, record):
    type_ = query['type']

    if type_ == 'exact':
        return _compile_exact(query, record)
    elif type_ == 'fuzzy':
        return _compile_fuzzy(query, record)
    elif type_ == 'nested':
        return _compile_nested(query, record)

    raise NotImplementedError(type_)


def _compile_exact(query, record):
    path, search_path = query['path'], query['search_path']

    collections = query.get('collections', [])

    values = force_list(get_value(record, path))
    if not values:
        return

    result = {
        'query': {
            'bool': {
                'should': [],
            },
        },
    }

    if collections:
        result['query']['bool']['minimum_should_match'] = 1
        result['query']['bool']['filter'] = {'bool': {'should': []}}

        for collection in collections:
            result['query']['bool']['filter']['bool']['should'].append({
                'match': {
                    '_collections': collection,
                },
            })

    for value in values:
        result['query']['bool']['should'].append({
            'match': {
                search_path: value,
            },
        })

    return result


def _compile_fuzzy(query, record):
    clauses = query['clauses']

    result = {
        'min_score': 1,
        'query': {
            'dis_max': {
                'queries': [],
                'tie_breaker': 0.3,
            },
        },
    }

    for clause in clauses:
        path = clause['path']

        boost = clause.get('boost', 1)

        values = get_value(record, path)
        if not values:
            continue

        path = path.split('[')[0]
        if '.' in path:
            raise ValueError('the "path" key can\'t contain dots')
        # TODO: This query should be refined instead of relying on validation to filter out irrelevant results.
        result['query']['dis_max']['queries'].append({
            'more_like_this': {
                'boost': boost,
                'docs': [
                    {
                        'doc': {
                            path: values,
                        },
                    },
                ],
                'max_query_terms': 25,
                'min_doc_freq': 1,
                'min_term_freq': 1,
            },
        })

    if not result['query']['dis_max']['queries']:
        return

    return result


def _compile_nested(query, record):
    paths, search_paths = query['paths'], query['search_paths']

    if len(paths) != len(search_paths):
        raise ValueError('paths and search_paths must be of the same length')

    common_path = _get_common_path(search_paths)
    if not common_path:
        raise ValueError('search_paths must share a common path')

    result = {
        'query': {
            'nested': {
                'path': common_path,
                'query': {
                    'bool': {
                        'must': [],
                    },
                },
            },
        },
    }

    for path, search_path in zip(paths, search_paths):
        value = get_value(record, path)
        if not value:
            return

        result['query']['nested']['query']['bool']['must'].append({
            'match': {
                search_path: value,
            },
        })

    return result


def _get_common_path(paths):
    return '.'.join(os.path.commonprefix([path.split('.') for path in paths]))
