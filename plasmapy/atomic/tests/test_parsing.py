import pytest

from ...utils import (
    InvalidParticleError,
    InvalidElementError,
)

from ..particles import _special_particles

from ..parsing import (
    _dealias_particle_aliases,
    _case_insensitive_aliases,
    _case_sensitive_aliases,
    _parse_and_check_atomic_input,)

aliases_and_symbols = [
    ('electron', 'e-'),
    ('beta-', 'e-'),
    ('beta+', 'e+'),
    ('positron', 'e+'),
    ('proton', 'p+'),
    ('', ''),
    (5, 5),
    ('deuterium+', 'D 1+'),
    ('deuterium 1+', 'D 1+'),
    ('tritium +1', 'T 1+'),
    ('alpha', 'He-4 2+'),
    ('D+', 'D 1+'),
    ('Deuterium', 'D'),
    ('deuteron', 'D 1+'),
    ('triton', 'T 1+'),
    ('muon', 'mu-'),
    ('antimuon', 'mu+'),
    ('tau particle', 'tau-'),
    ('antitau', 'tau+'),
    ('p', 'p+'),
    ('H-1 1+', 'p+'),
    ('H-1+', 'p+'),
    ('H-1 +1', 'p+'),
    ('hydrogen-1+', 'p+'),
]


@pytest.mark.parametrize("alias, symbol", aliases_and_symbols)
def test_dealias_particle_aliases(alias, symbol):
    """Test that _dealias_particle_aliases correctly takes in aliases and
    returns the corresponding symbols, and returns the original argument
    if the argument does not correspond to an alias."""
    result = _dealias_particle_aliases(alias)
    assert result == symbol, \
        (f"_dealias_particle_aliases({alias}) returns '{result}', which "
         f"differs from the expected symbol of '{symbol}'.\n\n"
         f"_case_insensitive_aliases:\n{_case_insensitive_aliases}\n\n"
         f"_case_sensitive_aliases:\n{_case_sensitive_aliases}")


alias_dictionaries = [_case_sensitive_aliases, _case_insensitive_aliases]


@pytest.mark.parametrize("alias_dict", alias_dictionaries)
def test_alias_dict_properties(alias_dict):
    """Test properties of the alias dictionaries."""

    for key in alias_dict.keys():
        assert isinstance(key, str), \
            (f"The following key should be a string, but isn't: {key}\n\n"
             f"The entire dictionary is:\n\n{alias_dict}")

    for value in alias_dict.values():
        assert isinstance(value, str), \
            (f"The following value should be a string, but isn't: {value}\n\n"
             f"The entire dictionary is:\n\n{alias_dict}")


# (arg, kwargs, expected)
parse_check_table = [

    ('He', {'Z': 1, 'mass_numb': 4},
     {'symbol': 'He-4 1+',
      'element': 'He',
      'isotope': 'He-4',
      'ion': 'He-4 1+',
      'mass_numb': 4,
      'Z': 1}),

    ('alpha', {},
     {'symbol': 'He-4 2+',
      'element': 'He',
      'isotope': 'He-4',
      'ion': 'He-4 2+',
      'mass_numb': 4,
      'Z': 2}),

    (1, {},
     {'symbol': 'H',
      'element': 'H',
      'isotope': None,
      'ion': None,
      'Z': None,
      'mass_numb': None}),

    ('H', {'mass_numb': 2},
     {'symbol': 'D',
      'element': 'H',
      'isotope': 'D',
      'ion': None,
      'Z': None,
      'mass_numb': 2}),

    (2, {},
     {'symbol': 'He',
      'element': 'He',
      'isotope': None,
      'ion': None,
      'Z': None,
      'mass_numb': None}),

    ('T', {'Z': 0},
     {'symbol': 'T 0+',
      'element': 'H',
      'isotope': 'T',
      'ion': 'T 0+',
      'Z': 0,
      'mass_numb': 3}),

    ('Fe-56+++++++', {},
     {'symbol': 'Fe-56 7+',
      'element': 'Fe',
      'isotope': 'Fe-56',
      'ion': 'Fe-56 7+',
      'Z': 7,
      'mass_numb': 56}),

    ('H-', {},
     {'symbol': 'H 1-',
      'element': 'H',
      'isotope': None,
      'ion': 'H 1-',
      'Z': -1,
      'mass_numb': None}),

    ('D+', {},
     {'symbol': 'D 1+',
      'element': 'H',
      'isotope': 'D',
      'ion': 'D 1+',
      'Z': 1,
      'mass_numb': 2}),

    ('Au', {},
     {'symbol': 'Au',
      'element': 'Au',
      'isotope': None,
      'ion': None,
      'Z': None,
      'mass_numb': None}),

    ('Ar 2-', {},
     {'symbol': 'Ar 2-',
      'element': 'Ar',
      'isotope': None,
      'ion': 'Ar 2-',
      'Z': -2,
      'mass_numb': None}),

    ('Fe +24', {'mass_numb': 56},
     {'symbol': 'Fe-56 24+',
      'element': 'Fe',
      'isotope': 'Fe-56',
      'ion': 'Fe-56 24+',
      'Z': 24,
      'mass_numb': 56}),

    ('Be-8 +3', {},
     {'symbol': 'Be-8 3+',
      'element': 'Be',
      'isotope': 'Be-8',
      'ion': 'Be-8 3+',
      'Z': 3,
      'mass_numb': 8}),

    ('p+', {},
     {'symbol': 'p+',
      'element': 'H',
      'isotope': 'H-1',
      'ion': 'p+',
      'Z': 1,
      'mass_numb': 1}),

]


@pytest.mark.parametrize('arg, kwargs, expected', parse_check_table)
def test_parse_and_check_atomic_input(arg, kwargs, expected):
    result = _parse_and_check_atomic_input(arg, **kwargs)

    assert result == expected, (
        "Error in _parse_and_check_atomic_input.\n"
        "The resulting dictionary is:\n\n"
        f"{result}\n\n"
        "whereas the expected dictionary is:\n\n"
        f"{expected}\n"
    )


# (arg, kwargs)
invalid_particles_table = [
    ('H-0', {}),
    ('Og-294b', {}),
    ('H-934361', {}),
    ('Fe 2+4', {}),
    ('Fe+24', {}),
    ('Fe +59', {}),
    ('C++++++++++++++++', {}),
    ('C-++++', {}),
    ('h', {}),
    ('H++', {}),
    ('H 2+', {}),
    ('T+++', {}),
    ('D', {'Z': 2}),
    ('d', {}),
    ('he', {}),
    ('au', {}),
    (0, {}),
    (119, {}),
    (0, {'mass_numb': 1}),
    ('p-', {'mass_numb': -1}),
    ('e-', {'Z': -1}),
    (0, {'mass_numb': 1}),
    ('n', {'mass_numb': 1}),
    ('He-4', {'mass_numb': 3}),
    ('H-2+', {'Z': 0, 'mass_numb': 2}),
    ('H-', {'Z': 1}),
]


@pytest.mark.parametrize('arg, kwargs', invalid_particles_table)
def test_parse_InvalidParticleErrors(arg, kwargs):
    r"""Tests that _parse_and_check_atomic_input raises an
    InvalidParticleError when the input does not correspond
    to a real particle."""
    with pytest.raises(InvalidParticleError):
        _parse_and_check_atomic_input(arg, **kwargs)


@pytest.mark.parametrize('arg', _special_particles)
def test_parse_InvalidElementErrors(arg):
    r"""Tests that _parse_and_check_atomic_input raises an
    InvalidElementError when the input corresponds to a valid
    particle but not a valid element, isotope, or ion."""
    with pytest.raises(InvalidElementError):
        _parse_and_check_atomic_input(arg)
        
# (arg, kwargs)
atomic_warnings_table = [
    ('H-2 1+', {'mass_numb': 2, 'Z': 1}),
    ('H 1+', {'Z': 1}),
    ('H-3', {'mass_numb': 3}),
    ('Fe-56', {'Z': -4}),
]

@pytest.mark.parametrize('arg, kwargs', atomic_warnings_table)
def test_parse_AtomicWarnings(arg, kwargs):
    r"""Tests that _parse_and_check_atomic_input issues
    an AtomicWarning under the required conditions."""
    with pytest.warns(AtomicWarning):
        _parse_and_check_atomic_input(arg, **kwargs)
