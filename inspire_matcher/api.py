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

"""Matcher API."""

from __future__ import absolute_import, division, print_function

from flask import current_app
from invenio_search import current_search_client as es
from invenio_search.utils import prefix_index
from six import string_types
from werkzeug.utils import import_string

from inspire_matcher.core import compile


def _get_validator(validator_param):
    if callable(validator_param):
        return validator_param

    try:
        validator = import_string(validator_param)
    except (KeyError, ImportError, AttributeError):
        current_app.logger.debug(
            'No validator provided. Falling back to the default validator.'
        )
        validator = import_string('inspire_matcher.validators:default_validator')

    return validator


def match(record, config=None):
    """Given a record, yield the records in INSPIRE most similar to it.

    This method can be used to detect if a record that we are ingesting as a
    submission or as an harvest is already present in the system, or to find
    out which record a reference should be pointing to.
    """
    if config is None:
        current_app.logger.debug(
            'No configuration provided. Falling back to the default configuration.'
        )
        config = current_app.config['MATCHER_DEFAULT_CONFIGURATION']

    try:
        index = prefix_index(config['index'])
        size = config.get('size', 10)
        algorithm = config['algorithm']
        query_config = {'index': index, 'size': size}
    except KeyError as e:
        raise KeyError('Malformed configuration: %s.' % repr(e))

    source = config.get('source', [])
    if source:
        query_config['_source'] = source
    match_deleted = config.get('match_deleted', False)
    collections = config.get('collections')
    if not (
        collections is None
        or (
            isinstance(collections, (list, tuple))
            and all(isinstance(collection, string_types) for collection in collections)
        )
    ):
        raise ValueError(
            'Malformed collections. Expected a list of strings bug got: %s'
            % repr(collections)
        )

    for i, step in enumerate(algorithm):
        try:
            queries = step['queries']
        except KeyError:
            raise KeyError('Malformed algorithm: step %d has no queries.' % i)

        if not isinstance(step.get('validator'), list):
            validator_params = [step.get('validator')]
        else:
            validator_params = step.get('validator')

        validators = []
        for validator_param in validator_params:
            validators.append(_get_validator(validator_param))

        for j, query in enumerate(queries):
            try:
                body = compile(
                    query, record, collections=collections, match_deleted=match_deleted
                )
            except Exception as e:
                raise ValueError(
                    'Malformed query. Query %d of step %d does not compile: %s.'
                    % (j, i, repr(e))
                )

            if not body:
                continue
            query_config['body'] = body
            current_app.logger.debug('Sending ES query: %s' % repr(body))
            result = es.search(**query_config)
            for hit in result['hits']['hits']:
                is_hit_valid = all([validator(record, hit) for validator in validators])
                if is_hit_valid:
                    yield hit
