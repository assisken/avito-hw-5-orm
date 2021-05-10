```shell
$ pipenv run make test
'python3' -m pytest lib tests
========================================================================= test session starts ==========================================================================
platform darwin -- Python 3.8.2, pytest-6.2.2, py-1.10.0, pluggy-0.13.1 -- /Users/nvzhiga/.local/share/virtualenvs/avito-hw-5-orm-nBW9bP5x/bin/python3
cachedir: .pytest_cache
rootdir: /Users/nvzhiga/code/python/avito-hw-5-orm, configfile: setup.cfg
plugins: flake8-1.0.7, cov-2.11.1
collected 20 items

lib/__init__.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                                        [  5%]
lib/orm.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                                             [ 10%]
lib/util.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                                            [ 15%]
lib/util.py::lib.util.Singleton PASSED                                                                                                                           [ 20%]
lib/util.py::lib.util.StrictDict PASSED                                                                                                                          [ 25%]
lib/util.py::lib.util.camel_to_snake_case PASSED                                                                                                                 [ 30%]
tests/conftest.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                                      [ 35%]
tests/test_meta.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                                     [ 40%]
tests/test_meta.py::test_meta_was_overrited PASSED                                                                                                               [ 45%]
tests/test_meta.py::test_meta_was_not_overrited PASSED                                                                                                           [ 50%]
tests/test_orm.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                                      [ 55%]
tests/test_orm.py::test_create_table PASSED                                                                                                                      [ 60%]
tests/test_orm.py::test_insert_some_data PASSED                                                                                                                  [ 65%]
tests/test_orm.py::test_create PASSED                                                                                                                            [ 70%]
tests/test_orm.py::test_select PASSED                                                                                                                            [ 75%]
tests/test_orm.py::test_validation[-1] PASSED                                                                                                                    [ 80%]
tests/test_orm.py::test_validation[aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-1] PASSED               [ 85%]
tests/test_orm.py::test_validation[AmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeusAmadeus-0] PASSED [ 90%]
tests/test_use_case.py::FLAKE8 SKIPPED (file(s) previously passed FLAKE8 checks)                                                                                 [ 95%]
tests/test_use_case.py::test_use_case PASSED                                                                                                                     [100%]

==================================================================== 13 passed, 7 skipped in 0.12s =====================================================================
```