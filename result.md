```shell
$ pipenv run make coverage
'python3' -m pytest --cov=. --cov-config=setup.cfg tests
========================================================================= test session starts ==========================================================================
platform darwin -- Python 3.8.2, pytest-6.2.2, py-1.10.0, pluggy-0.13.1 -- /Users/nvzhiga/.local/share/virtualenvs/avito-hw-4-classes-N39BFytA/bin/python3
cachedir: .pytest_cache
rootdir: /Users/nvzhiga/code/python/avito-hw-4-classes, configfile: setup.cfg
plugins: flake8-1.0.7, cov-2.11.1
collected 9 items

tests/test_advert.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                                   [ 11%]
tests/test_advert.py::test_validation[given0-NotAllowedKeyError] PASSED                                                                                          [ 22%]
tests/test_advert.py::test_validation[given1-NotAllowedKeyError] PASSED                                                                                          [ 33%]
tests/test_advert.py::test_validation[given2-TooLowPriceError] PASSED                                                                                            [ 44%]
tests/test_advert.py::test_validation[given3-RequiredFieldError] PASSED                                                                                          [ 55%]
tests/test_advert.py::test_default_price PASSED                                                                                                                  [ 66%]
tests/test_advert.py::test_has_fields_from_dict PASSED                                                                                                           [ 77%]
tests/test_colorized_mixin.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                          [ 88%]
tests/test_colorized_mixin.py::test_corgi_in_colors PASSED                                                                                                       [100%]

---------- coverage: platform darwin, python 3.8.2-final-0 -----------
Name          Stmts   Miss  Cover
---------------------------------
issue_01.py      44      6    86%
issue_02.py      14      3    79%
---------------------------------
TOTAL            58      9    84%


===================================================================== 7 passed, 2 skipped in 0.16s =====================================================================
```