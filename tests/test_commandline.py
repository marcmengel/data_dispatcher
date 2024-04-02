import pytest
import os

#test_proj = 

def test_ddisp_help():
    with os.popen("ddisp help", "r") as fin:
        data = fin.read()
        assert data.find("login") > 0
        assert data.find("version") > 0

def test_ddisp_version():
    with os.popen("ddisp version", "r") as fin:
        data = fin.read()
        assert data.find("Server version") > 0
        assert data.find("Client version") > 0

def test_ddisp_login_token():
    with os.popen(f"ddisp login -m token {os.environ['USER']}", "r") as fin:
        data = fin.read()
        assert data.find(os.environ["USER"]) > 0
        assert data.find("User") >= 0
        assert data.find("Expires") >= 0

def test_ddisp_project_create():
    with os.popen(f"ddisp project create {test_proj} ", "r") as fin:
        data = fin.read()
        assert type(data) == int

def test_ddisp_project_copy():
    with os.popen(f"ddisp project copy {proj_id} ", "r") as fin:
        data = fin.read()
        assert type(data) == int
        assert data != proj_id

def test_ddisp_project_show():
    with os.popen(f"ddisp project show {proj_id}", "r") as fin:
        data = fin.read()
    assert data.find("Owner") > 0
    assert data.find("Status") > 0
    assert data.find("Created") > 0

def test_ddisp_project_list():
    with os.popen("ddisp project list", "r") as fin:
        data = fin.read()
    assert data.find("owner") > 0
    assert data.find("created") > 0
    assert data.find("state") > 0

def test_ddisp_project_search():


def test_ddisp_project_restart():


def test_ddisp_project_activate():


def test_ddisp_project_cancel():


def test_ddisp_project_delete():


def test_ddisp_file_show():


def test_ddisp_file_list():
 

def test_ddisp_worker_id():
    with os.popen("ddisp worker id", "r") as fin:
        data = fin.read()
    assert data > 0

def test_ddisp_worker_list():


def test_ddisp_worker_next():


def test_ddisp_worker_done():


def test_ddisp_worker_fail():


def test_ddisp_rse_list():
    with os.popen("ddisp rse list", "r") as fin:
        data = fin.read()
    assert data.find("Name") > 0
    assert data.find("Status") > 0
    assert data.find("Description") > 0

def test_ddisp_rse_set():


def test_ddisp_rse_show():
    with os.popen("ddisp rse show FNAL_DCACHE_DISK_TEST", "r") as fin:
        data = fin.read()
    assert data.find("RSE") > 0
    assert data.find("Available") > 0


