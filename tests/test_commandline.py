import pytest
import os

from env import env, token, auth

test_proj = "files from mengel:gen_cfg"

def test_ddisp_help(auth):
    with os.popen("ddisp help", "r") as fin:
        data = fin.read()
        assert data.find("login") > 0
        assert data.find("version") > 0

def test_ddisp_version(auth):
    with os.popen("ddisp version", "r") as fin:
        data = fin.read()
        assert data.find("Server version") > 0
        assert data.find("Client version") > 0

def test_ddisp_login_token(auth, token):
    with os.popen(f"ddisp login -m token {os.environ['USER']}", "r") as fin:
        data = fin.read()
        assert data.find(os.environ["USER"]) > 0
        assert data.find("User") >= 0
        assert data.find("Expires") >= 0

@pytest.fixture
def test_ddisp_project_create(auth):
    with os.popen(f"ddisp project create {test_proj} ", "r") as fin:
        data = fin.read()
        assert type(data) == int
    return data

def test_ddisp_project_show(auth, test_ddisp_project_create):
    with os.popen(f"ddisp project show {test_ddisp_project_create}", "r") as fin:
        data = fin.read()
    assert data.find("Owner") > 0
    assert data.find("Status") > 0
    assert data.find("Created") > 0

#def test_ddisp_project_copy(auth, test_ddisp_project_create):
#    with os.popen(f"ddisp project copy {test_ddisp_project_create} ", "r") as fin:
#        data = fin.read()
#        assert type(data) == int
#        assert data != proj_id

def test_ddisp_project_list(auth):
    with os.popen("ddisp project list", "r") as fin:
        data = fin.read()
    assert data.find("owner") > 0
    assert data.find("created") > 0
    assert data.find("state") > 0

def test_ddisp_project_search(auth):
    with os.popen("ddisp project search -s active", "r") as fin:
        data = fin.read()
    assert data.find(str(proj_id)) > 0
    assert data.find(os.environ["USER"]) > 0

#def test_ddisp_project_restart():


#def test_ddisp_project_cancel():
#    os.system(f"ddisp project cancel {proj_id} ")
#    with os.popen(f"ddisp project show {proj_id} ", "r") as fin:
#        data = fin.read()
#    assert data.find("cancelled") > 0

#def test_ddisp_project_activate():
#    os.system(f"ddisp project activate {proj_id} ")
#    with os.popen(f"ddisp project show {proj_id} ", "r") as fin:
#        data = fin.read()
#    assert data.find("active") > 0

#def test_ddisp_project_delete():


#def test_ddisp_file_show():


#def test_ddisp_file_list():
 

def test_ddisp_worker_id(auth):
    with os.popen("ddisp worker id", "r") as fin:
        data = fin.read()
    assert data > 0

#def test_ddisp_worker_list():


#def test_ddisp_worker_next():


#def test_ddisp_worker_done():


#def test_ddisp_worker_fail():


def test_ddisp_rse_list(auth):
    with os.popen("ddisp rse list", "r") as fin:
        data = fin.read()
    assert data.find("Name") > 0
    assert data.find("Status") > 0
    assert data.find("Description") > 0

#def test_ddisp_rse_set():


def test_ddisp_rse_show(auth):
    with os.popen("ddisp rse show FNAL_DCACHE_DISK_TEST", "r") as fin:
        data = fin.read()
    assert data.find("RSE") > 0
    assert data.find("Available") > 0


