import pytest
import os
import sys


@pytest.fixture(scope="session")
def dir_class_fixture():
    sys.path.append('..')
    import module as mod
    return mod.Directories(base_dir=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), \
           os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def test_output_dir():
    # Check that output directory is good
    temp_obj, base_test_path = dir_class_fixture()
    assert temp_obj.get_output_dir() == os.path.join(base_test_path, 'Output')


def test_yml_dir():
    # Check that yml directory is good
    temp_obj, base_test_path = dir_class_fixture()
    assert temp_obj.get_yml_dir() == os.path.join(base_test_path, 'yaml')


def test_logging_dir():
    # Check that logging directory is good
    temp_obj, base_test_path = dir_class_fixture()
    assert temp_obj.get_logging_dir() == os.path.join(base_test_path, 'Logs')


def test_templates_dir_is_list():
    # Check that templates directory returns a list
    temp_obj, base_test_path = dir_class_fixture()
    assert isinstance(temp_obj.get_templates_dir(), list)


def test_verify_base_logging_level():
    # Check that templates directory returns a list
    temp_obj, base_test_path = dir_class_fixture()
    assert temp_obj.get_logging_level() == 30
