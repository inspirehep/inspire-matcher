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

"""Find the records in INSPIRE most similar to a given record or reference."""

from __future__ import absolute_import, division, print_function

from setuptools import find_packages, setup

URL = 'https://github.com/inspirehep/inspire-matcher'

with open("README.rst") as f:
    readme = f.read()

setup_requires = [
    'autosemver~=0.0,>=0.5.2',
]

install_requires = [
    'inspire-json-merger~=11.0,>=11.0.0',
    'dictdiffer<0.9.0; python_version <= "2.7"',
    'dictdiffer>=0.9.0; python_version >= "3.6"',
    'inspire-utils~=3.0,>=3.0.0',
    'invenio-search>=1.2.3',
    'six~=1.0,>=1.11.0',
    'invenio-base>=1.2.3,<2.0.0',
    'pyyaml==5.4.1; python_version <= "2.7"',
    'pyyaml>=6.0,<7.0; python_version >= "3.6"',
]

docs_require = []

tests_require = [
    'mock~=3.0,>=3.0.0',
    'pytest-cov~=2.0,>=2.5.1',
    'pytest~=4.0,>=4.6.0; python_version <= "2.7"',
    'pytest~=8.0,>=8.2.2; python_version >= "3.6"',
    'pytest-pep8',
]

dev_require = [
    "pre-commit==3.5.0",
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
    'dev': dev_require,
    'tests:python_version=="2.7"': [
        'unicode-string-literal~=1.0,>=1.1',
    ],
    'opensearch1': ['opensearch-py>=1.0.0,<3.0.0', 'opensearch-dsl>=1.0.0,<3.0.0'],
    'elasticsearch7': [
        'elasticsearch-dsl~=7.0',
        'elasticsearch~=7.0',
    ],
    'opensearch2': [
        'opensearch-py>=2.0.0,<3.0.0',
        'opensearch-dsl>=2.0.0,<3.0.0',
    ],
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name not in ('opensearch1', 'opensearch2', 'elasticsearch7'):
        extras_require['all'].extend(reqs)

packages = find_packages(exclude=['docs'])

setup(
    name='inspire-matcher',
    autosemver={
        'bugtracker_url': URL + '/issues',
    },
    url=URL,
    license='GPLv3',
    author='CERN',
    author_email='admin@inspirehep.net',
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    description=__doc__,
    long_description=readme,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    entry_points={
        'invenio_base.apps': [
            'inspire_matcher = inspire_matcher:InspireMatcher',
        ],
    },
    version="9.0.30",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
