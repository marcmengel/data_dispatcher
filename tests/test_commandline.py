import pytest
import os

from env import env, token, auth

test_proj = "files from mengel:gen_cfg"

def test_ddisp_help(auth):
    with os.popen("ddisp help 2>&1", "r") as fin:
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

@pytest.fixture(scope='session')
def proj_id(auth):
    with os.popen(f"ddisp project create {test_proj} ", "r") as fin:
        data = fin.read().strip()
    return data

def test_ddisp_project_create(auth, proj_id):
    assert len(proj_id) > 0
    assert type(int(proj_id)) == int

def test_ddisp_project_show(auth, proj_id):
    with os.popen(f"ddisp project show {proj_id}", "r") as fin:
        data = fin.read()
    assert data.find("Owner") > 0
    assert data.find("Status") > 0
    assert data.find("Created") > 0

def test_ddisp_project_list(auth):
    with os.popen("ddisp project list", "r") as fin:
        data = fin.read()
    assert data.find("Owner") > 0
    assert data.find("Created") > 0
    assert data.find("State") > 0

def test_ddisp_file_show(auth, proj_id):
    with os.popen(f"ddisp file show {proj_id} mengel:a.fcl ", "r") as fin:
        data = fin.read()
    assert data.find(f"{proj_id}") > 0
    assert data.find("namespace") > 0
    assert data.find("state") > 0

def test_ddisp_file_list(auth, proj_id):
    with os.popen(f"ddisp file list {proj_id} ", "r") as fin:
        data = fin.read()
    assert data.find("Status") > 0
    assert data.find("Replicas") > 0
    assert data.find("File") > 0

def test_ddisp_file_list_rse(auth, proj_id):
    with os.popen(f"ddisp file list -r FNAL_DCACHE_DISK_TEST {proj_id} ", "r") as fin:
        data = fin.read()
    assert data.find("mengel:a.fcl") > 0
    with os.popen(f"ddisp file list -r TEST {proj_id} ", "r") as fin:
        data = fin.read()
    assert data.find("mengel:a.fcl") < 0

@pytest.fixture(scope='session')
def next_file(auth, proj_id):
    with os.popen(f"ddisp worker next {proj_id} ", "r") as fin:
        did = fin.read()
    return did

def test_ddisp_worker_next(auth, next_file):
    assert len(next_file) > 0

def test_ddisp_worker_id(auth):
    with os.popen("ddisp worker id", "r") as fin:
        data = fin.read()
    assert len(data) > 0

def test_ddisp_worker_list(auth, proj_id):
    with os.popen(f"ddisp worker list {proj_id} ", "r") as fin:
        data = fin.read()
    assert data.find("project_id") >= 0
    assert data.find("worker_id") >= 0
    assert data.find("namespace") >= 0

def test_ddisp_worker_list_w(auth, proj_id):
    with os.popen("ddisp worker id", "r") as fin:
        wid = fin.read().strip()
    with os.popen(f"ddisp worker list -w {wid} {proj_id} ", "r") as fin:
        data = fin.read()
    assert data.find("namespace") >= 0
    assert data.find("project_id") >= 0
    assert data.find("worker_id") >= 0

def test_ddisp_project_show_state(auth, proj_id):
    with os.popen(f"ddisp project show -f initial {proj_id}", "r") as fin:
        data = fin.read()
    assert data.find(".fcl") >= 0
    with os.popen(f"ddisp project show -f done {proj_id}", "r") as fin:
        data = fin.read()
    assert len(data) == 0
    with os.popen(f"ddisp project show -f test {proj_id}", "r") as fin:
        data = fin.read()
    assert data.find("Invalid state") >= 0

# needs to be fixed
#def test_ddisp_project_search(auth, proj_id):
#    with os.popen("ddisp project search -s active", "r") as fin:
#        data = fin.read()
#    assert data.find(str(proj_id)) > 0
#    assert data.find(os.environ["USER"]) > 0

def test_ddisp_worker_done(auth, proj_id, next_file):
    with os.popen(f"ddisp worker done {proj_id} {next_file} ", "r") as fin:
        data = fin.read()
    assert len(data) == 0
    with os.popen(f"ddisp file show {proj_id} {next_file} ", "r") as fin:
        data = fin.read()
    assert data.find("done") > 0

def test_ddisp_file_list_state(auth, proj_id):
    with os.popen(f"ddisp file list -s initial {proj_id} ", "r") as fin:
        data = fin.read()
    assert data.find("initial") > 0
    with os.popen(f"ddisp file list -s done {proj_id} ", "r") as fin:
        data = fin.read()
    assert data.find("done") > 0
    assert data.find("initial") < 0

def test_ddisp_worker_failed(auth, proj_id):
    # failing once causes the file to go back to the initial state to be retried
    with os.popen(f"ddisp worker next {proj_id} ", "r") as fin:
        did = fin.read()
    with os.popen(f"ddisp worker failed {proj_id} {did}", "r") as fin:
        data = fin.read()
    assert len(data) == 0
    with os.popen(f"ddisp file show {proj_id} {did}", "r") as fin:
        data = fin.read()
    assert data.find("initial") > 0

    # this time mark the file as permanently failed with the -f option
    with os.popen(f"ddisp worker next {proj_id} ", "r") as fin:
        did = fin.read()
    with os.popen(f"ddisp worker failed -f {proj_id} {did} ", "r") as fin:
        data = fin.read()
    assert len(data) == 0
    with os.popen(f"ddisp file show {proj_id} {did} ", "r") as fin:
        data = fin.read()
    assert data.find("failed") > 0

def test_ddisp_worker_failed_all(auth, proj_id):
    with os.popen(f"ddisp project show -f initial {proj_id}", "r") as fin:
        dids = fin.read()

    dids = dids.split('\n')
    dids = dids[:-1]

    for did in dids:
        os.system(f"ddisp worker next {proj_id}")

    with os.popen(f"ddisp worker failed -f {proj_id} all", "r") as fin:
        data = fin.read()
        assert len(data) == 0

    with os.popen(f"ddisp file list {proj_id}", "r") as fin:
        data = fin.read()
        assert data.find("initial") < 0
        assert data.find("failed") > 0

def test_ddisp_project_restart(auth, proj_id):
    with os.popen(f"ddisp project restart -a {proj_id}", "r") as fin:
        data = fin.read()
        assert len(data) == 0
    with os.popen(f"ddisp file list {proj_id}", "r") as fin:
        data = fin.read()
        assert data.find("initial") > 0
        assert data.find("failed") < 0

def test_ddisp_worker_done_all(auth, proj_id):
    with os.popen(f"ddisp project show -f initial {proj_id}", "r") as fin:
        dids = fin.read()
    dids = dids.split('\n')
    dids = dids[:-1]
    for did in dids:
        os.system(f"ddisp worker next {proj_id}")
    with os.popen(f"ddisp worker done {proj_id} all", "r") as fin:
        data = fin.read()
        assert len(data) ==0
    with os.popen(f"ddisp file list {proj_id}", "r") as fin:
        data = fin.read()
        assert data.find("done") > 0
        assert data.find("initial") < 0
        assert data.find("failed") < 0

@pytest.fixture(scope='session')
def proj_id_copy(auth, proj_id):
    with os.popen(f"ddisp project copy {proj_id} ", "r") as fin:
        data = fin.read().strip()
    return data

def test_ddisp_project_copy(auth, proj_id, proj_id_copy):
    assert proj_id_copy != proj_id
    assert type(int(proj_id_copy)) == int

#def test_ddisp_project_activate():
#    os.system(f"ddisp project activate {proj_id_copy} ")
#    with os.popen(f"ddisp project show {proj_id_copy} ", "r") as fin:
#        data = fin.read()
#    assert data.find("active") > 0

def test_ddisp_project_cancel(auth, proj_id_copy):
    os.system(f"ddisp project cancel {proj_id_copy} ")
    with os.popen(f"ddisp project show {proj_id_copy} ", "r") as fin:
        data = fin.read()
#        print(data.find("cancelled"))
    assert data.find("cancelled") > 0

# needs to be fixed
#def test_ddisp_project_delete(auth, proj_id_copy):
#    with os.popen(f"ddisp project delete {proj_id_copy} ", "r") as fin:
#        data = fin.read()
#    assert

def test_ddisp_rse_list(auth):
    with os.popen("ddisp rse list", "r") as fin:
        data = fin.read()
    assert data.find("Name") >= 0
    assert data.find("Status") >= 0
    assert data.find("Description") >= 0

#def test_ddisp_rse_set():


def test_ddisp_rse_show(auth):
    with os.popen("ddisp rse show FNAL_DCACHE_DISK_TEST", "r") as fin:
        data = fin.read()
    assert data.find("RSE") >= 0
    assert data.find("Available") >= 0


