import pytest
import os
import sys
base_path = os.path.join(os.path.abspath(os.path.dirname(__name__)))
sys.path.append(os.path.join(base_path))
import module as mod


@pytest.fixture
def dir_class_fixture():
    return mod.Directories(base_dir=base_path)
