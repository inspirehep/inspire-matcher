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
from werkzeug.utils import import_string

from invenio_search import current_search_client as es

from .core import compile


def match(record, config=None):
    """Given a record, yield the records in INSPIRE most similar to it.

    This method can be used to detect if a record that we are ingesting as a
    submission or as an harvest is already present in the system, or to find
    out which record a reference should be pointing to.
    """
    if config is None:
        current_app.logger.debug('No configuration provided. Falling back to the default configuration.')
        config = current_app.config['MATCHER_DEFAULT_CONFIGURATION']

    try:
        algorithm, doc_type, index = config['algorithm'], config['doc_type'], config['index']
    except KeyError as e:
        raise KeyError('Malformed configuration: %s.' % repr(e))

    for i, step in enumerate(algorithm):
        try:
            queries = step['queries']
        except KeyError:
            raise KeyError('Malformed algorithm: step %d has no queries.' % i)

        try:
            validator = import_string(step['validator'])
        except (KeyError, ImportError):
            current_app.logger.debug('No validator provided. Falling back to the default validator.')
            validator = import_string('inspire_matcher.validators:default_validator')

        for j, query in enumerate(queries):
            try:
                body = compile(query, record)
            except Exception as e:
                raise ValueError('Malformed query. Query %d of step %d does not compile: %s.' % (j, i, repr(e)))

            if not body:
                continue

            results = es.search(index=index, doc_type=doc_type, body=body)

            for result in results['hits']['hits']:
                if validator(record, result):
                    yield result
