"""Tests of Stitching functions."""

import platform

import pytest
from flugelhorn import stitching

# Fixtures
@pytest.fixture
def system():
    return platform.system()


# Tests
class TestStitcherAppPath:

    # Mac OSX Tests
    def test_get_stitching_app_path_osx(self, system):
        if system == 'Darwin':
            expected_path = stitching.OSX_STITCHER_APP
            actual_path = stitching.get_stitching_app_path()
            assert actual_path == expected_path

    def test_stitching_app_install_error_osx(self, system, monkeypatch):
        if system == 'Darwin':
            monkeypatch.setattr(stitching.OSX_STITCHER_APP,
                                '/Users/NotExist/ProStitcher')
            with pytest.raises(stitching.StitcherInstallError):
                get_stitching_app_path() 


    # Windows tests 
    def test_get_stitching_app_path_win(self, system):
        if system == 'Windows':
            expected_path = stitching.WINDOWS_STITCHER_APP
            actual_path = get_stitching_app_path
            assert actual_path == expected_path
    
    def test_stitching_app_install_error_osx(self, system, monkeypatch):
        if system == 'Windows':
            monkeypatch.setattr(stitching.WINDOWS_STITCHER_APP,
                                'C:\\User\\NotExist\\ProStitcher.exe')
            with pytest.raises(stitching.StitcherInstallError):
                get_stitching_app_path() 

