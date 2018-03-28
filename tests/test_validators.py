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

from inspire_matcher.validators import (
    authors_titles_validator,
    default_validator,
)


def test_default_validator_is_not_very_exciting():
    assert default_validator(None, None)


def test_authors_titles_validator_authors_only_passes_first_five_many_match():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'authors': [
            {
                'full_name': 'Smith, J.'
            },
            {
                'full_name': 'Zappacosta, L.',
            },
            {
                'full_name': 'Comastri, A.',
            }

        ]
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'authors': [
                {
                    'full_name': 'Smith, J.'
                },
                {
                    'full_name': 'Zappacosta, L.',
                },
                {
                    'full_name': 'Comastri, A.',
                },
                {
                    'full_name': 'Masini, A.'
                },
                {
                    'full_name': 'Civano, F.'
                },
                {
                    'full_name': 'Fornasini, F.'
                },
                {
                    'full_name': 'Treister, E.'
                },
                {
                    'full_name': 'Alexander, A.'
                },
                {
                    'full_name': 'Boorman, P.G.'
                },
                {
                    'full_name': 'Brandt, D.'
                },
                {
                    'full_name': 'Lanz, L.'
                }
            ]
        }
    }  # Matching score > 0.5 for first 5 authors

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_authors_only_fails_first_five_few_match():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'authors': [
            {
                'full_name': 'Smith, J.'
            },
            {
                'full_name': 'Comastri, A.',
            }
        ]
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'authors': [
                {
                    'full_name': 'Smith, J.'
                },
                {
                    'full_name': 'Zappacosta, L.',
                },
                {
                    'full_name': 'Comastri, A.',
                },
                {
                    'full_name': 'Masini, A.'
                },
                {
                    'full_name': 'Civano, F.'
                },
                {
                    'full_name': 'Fornasini, F.'
                },
                {
                    'full_name': 'Treister, E.'
                },
                {
                    'full_name': 'Alexander, A.'
                },
                {
                    'full_name': 'Boorman, P.G.'
                },
                {
                    'full_name': 'Brandt, D.'
                },
                {
                    'full_name': 'Lanz, L.'
                }
            ]
        }
    }  # Matching score < 0.5 for first 5 authors

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_titles_only_passes_exact_match():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'titles': [
            {
                'title': 'A MATCHING TITLE',  # Jaccard index == 1.0
            },
            {
                'title': 'CMB anisotropies: A Decadal survey'
            }
        ]
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'titles': [
                {
                    'title': 'a matching title'
                },
                {
                    'title': 'Exotic RG Flows from Holography'
                },
                {
                    'title': 'CP violation in the B system'
                },
                {
                    'title': 'Supersymmetry'
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual'
                }
            ]
        }
    }

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_titles_only_passes_partial_match():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'titles': [
            {
                'title': 'A PARTIAL MATCHING TITLE ONLY'  # 0.5 < Jaccard index < 1.0
            },
            {
                'title': 'CMB anisotropies: A Decadal survey'
            }
        ]
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'titles': [
                {
                    'title': 'a matching title'
                },
                {
                    'title': 'Exotic RG Flows from Holography'

                },
                {
                    'title': 'CP violation in the B system'
                },
                {
                    'title': 'Supersymmetry'
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual'
                }
            ]
        }
    }

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_titles_only_fails_no_match():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'titles': [
            {
                'title': 'CMB anisotropies: A Decadal survey'  # Jaccard index == 0.0.
            }
        ]
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'titles': [
                {
                    'title': 'Exotic RG Flows from Holography',

                },
                {
                    'title': 'CP violation in the B system',
                },
                {
                    'title': 'Supersymmetry',
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual',
                }
            ]
        }
    }

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_titles_only_fails_partial_match():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'titles': [
            {
                'title': 'CMB anisotropies: A Decadal survey'
            },
            {
                'title': 'partial matching title but not enough'  # 0.0 < Jaccard index < 0.5
            }
        ]
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'titles': [
                {
                    'title': 'partial matching title'
                },
                {
                    'title': 'Exotic RG Flows from Holography',

                },
                {
                    'title': 'CP violation in the B system',
                },
                {
                    'title': 'Supersymmetry',
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual',
                }
            ]
        }
    }

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_passes_authors_and_titles_match_both():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'authors': [
            {
                'full_name': 'Smith, J.'
            },
            {
                'full_name': 'Zappacosta, L.'
            },
            {
                'full_name': 'Comastri, A.'
            }
        ],
        'titles': [
            {
                'title': 'A MATCHING TITLE'  # 0.5 < Jaccard index < 1.0
            },
            {
                'title': 'CMB anisotropies: A Decadal survey'
            }
        ],
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'authors': [
                {
                    'full_name': 'Smith, J.'
                },
                {
                    'full_name': 'Zappacosta, L.'
                },

            ],
            'titles': [
                {
                    'title': 'a good matching title'
                },
                {
                    'title': 'Exotic RG Flows from Holography'

                },
                {
                    'title': 'CP violation in the B system'
                },
                {
                    'title': 'Supersymmetry'
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual'
                }
            ]
        }
    }

    assert authors_titles_validator(record, result)


def test_authors_titles_validator_fails_authors_and_titles_match_author():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'authors': [
            {
                'full_name': 'Smith, J.'
            },
            {
                'full_name': 'Zappacosta, L.'
            },
            {
                'full_name': 'Comastri, A.'
            }
        ],
        'titles': [
            {
                'title': 'CP violation'  # Jaccard index < 0.5
            }
        ],
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'authors': [
                {
                    'full_name': 'Smith, J.'
                },
                {
                    'full_name': 'Black, J.'
                },

            ],
            'titles': [
                {
                    'title': 'Exotic RG Flows from Holography',

                },
                {
                    'title': 'CP violation in the B system',
                },
                {
                    'title': 'Supersymmetry',
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual',
                }
            ]
        }
    }

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_fails_authors_and_titles_match_title():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'authors': [
            {
                'full_name': 'Bentley, M.'
            },
            {
                'full_name': 'Zappacosta, L.'
            },
            {
                'full_name': 'Comastri, A.'
            }
        ],
        'titles': [
            {
                'title': 'A MATCHING TITLE'  # Jaccard index = 1.0
            },
            {
                'title': 'CMB anisotropies: A Decadal survey'
            }
        ],
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'authors': [
                {
                    'full_name': 'Smith, J.'
                },
                {
                    'full_name': 'Black, J.'
                },

            ],
            'titles': [
                {
                    'title': 'a matching title'
                },
                {
                    'title': 'Exotic RG Flows from Holography',

                },
                {
                    'title': 'CP violation in the B system',
                },
                {
                    'title': 'Supersymmetry',
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual',
                }
            ]
        }
    }

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_fails_authors_and_titles_partial_match_title():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'authors': [
            {
                'full_name': 'Bentley, M.'
            },
            {
                'full_name': 'Zappacosta, L.'
            },
            {
                'full_name': 'Comastri, A.'
            }
        ],
        'titles': [
            {
                'title': 'partial matching title but not enough'  # Jaccard index = 0.5
            },
            {
                'title': 'CMB anisotropies: A Decadal survey'
            }
        ],
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'authors': [
                {
                    'full_name': 'Smith, J.'
                },
                {
                    'full_name': 'Black, J.'
                },

            ],
            'titles': [
                {
                    'title': 'partial matching title'
                },
                {
                    'title': 'Exotic RG Flows from Holography',

                },
                {
                    'title': 'CP violation in the B system',
                },
                {
                    'title': 'Supersymmetry',
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual',
                }
            ]
        }
    }

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_fails_authors_and_titles_partial_match_both():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'authors': [
            {
                'full_name': 'Smith, J.'
            },
            {
                'full_name': 'Zappacosta, L.'
            },
            {
                'full_name': 'Comastri, A.'
            }
        ],
        'titles': [
            {
                'title': 'partial matching title but not enough'  # Jaccard index = 0.5
            },
            {
                'title': 'CMB anisotropies: A Decadal survey'
            }
        ],
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'authors': [
                {
                    'full_name': 'Smith, J.'
                },
                {
                    'full_name': 'Black, J.'
                },

            ],
            'titles': [
                {
                    'title': 'partial matching title'
                },
                {
                    'title': 'Exotic RG Flows from Holography',

                },
                {
                    'title': 'CP violation in the B system',
                },
                {
                    'title': 'Supersymmetry',
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual',
                }
            ]
        }
    }

    assert not authors_titles_validator(record, result)


def test_authors_titles_validator_fails_authors_and_titles_no_match_both():
    record = {
        '_collections': ['Literature'],
        'document_type': ['article'],
        'titles': [
            {
                'title': 'CMB anisotropies: A Decadal survey'
            }
        ],
        'authors': [
            {
                'full_name': 'Smith, J.'
            },
            {
                'full_name': 'Zappacosta, L.'
            },
            {
                'full_name': 'Comastri, A.'
            }
        ]
    }

    result = {
        '_source': {
            '_collections': ['Literature'],
            'document_type': ['article'],
            'authors': [
                {
                    'full_name': 'Bentley, M.'
                },
                {
                    'full_name': 'Black, J.'
                }
            ],
            'titles': [
                {
                    'title': 'Exotic RG Flows from Holography',

                },
                {
                    'title': 'CP violation in the B system',
                },
                {
                    'title': 'Supersymmetry',
                },
                {
                    'title': 'PYTHIA 6.4 Physics and Manual',
                }
            ]
        }
    }

    assert not authors_titles_validator(record, result)
