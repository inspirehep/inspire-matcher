<!--
This file is part of INSPIRE.
Copyright (C) 2014-2017 CERN.

INSPIRE is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

INSPIRE is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
INSPIRE. If not, see <http://www.gnu.org/licenses/>.

In applying this license, CERN does not waive the privileges and immunities
granted to it by virtue of its status as an Intergovernmental Organization or
submit itself to any jurisdiction.
-->

# INSPIRE-Matcher

## About

Finds the records in INSPIRE most similar to a given record or reference.

## Local setup and tests

Requires Python 3.11 or newer and Poetry 2.2 or newer.

```bash
poetry install -E tests -E dev -E opensearch3
poetry run pytest tests
```

The project uses the `opensearch3` extra.

Build distribution packages with `poetry build`.
