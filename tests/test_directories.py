import sys
import os

def test_output_dir(dir_class_fixture):
    # Check that output directory is good
    output_dir = os.path.split(dir_class_fixture.get_output_dir())[1]
    app_dir = os.path.split(os.path.split(dir_class_fixture.get_output_dir())[0])[1]
    assert 'QuickConfigTemplates' == app_dir
    assert 'Output' == output_dir


def test_yml_dir(dir_class_fixture):
    # Check that yml directory is good
    yml_dir = os.path.split(dir_class_fixture.get_yml_dir())[1]
    app_dir = os.path.split(os.path.split(dir_class_fixture.get_yml_dir())[0])[1]
    assert 'QuickConfigTemplates' == app_dir
    assert 'Output' == yml_dir


def test_logging_dir(dir_class_fixture):
    # Check that logging directory is good
    logs_dir = os.path.split(dir_class_fixture.get_logging_dir())[1]
    app_dir = os.path.split(os.path.split(dir_class_fixture.get_logging_dir())[0])[1]
    assert 'QuickConfigTemplates' == app_dir
    assert 'Logs' == logs_dir


def test_templates_dir_is_list(dir_class_fixture):
    # Check that templates directory returns a list
    assert list == type(dir_class_fixture.get_templates_dir())


def test_verify_base_logging_level(dir_class_fixture):
    # Check that templates directory returns a list
    assert 30 == dir_class_fixture.get_logging_level()
