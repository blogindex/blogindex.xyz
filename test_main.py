from fastapi.testclient import TestClient

from api.main import app
import api.schemas as schemas
from api.helpers.checks import schema_check

client = TestClient(app)
api_key = "KKVy-0B6G-JzBz-NweS-p6sU-GhaX-hHYk-zIcM"

# ROOT /
def test_get_root():
    response= client.get("/", follow_redirects=False)
    assert response.status_code == 307
    print(response)
    #assert response.location == "https://blogindex.xyz"

def test_post_root():
    response = client.post(
        "/",
        follow_redirects=False
    )
    assert response.status_code == 307
    #assert response.location == "https://blogindex.xyz"

# /user/get/all
def test_user_get_all():
    response = client.get(
        "/user/get/all",
        headers = {"X-API-Key" : api_key}
    )
    assert response.status_code == 200
    assert schema_check(schemas.User(**response.json()[0]))

def test_user_get_all_no_apikey():
    response = client.get(
        "/user/get/all"
    )
    assert response.status_code == 403

def test_user_get_all_bad_apikey():
    response = client.get(
        "/user/get/all",
        headers = {"X-API-Key" : "invalid-key"}
    )
    assert response.status_code == 401

# /user/get/by-email
def test_user_get_by_email():
    response = client.get(
        "/user/get/by-email?email=kenny@beardedtek.com",
        headers = {"X-API-Key" : api_key}
    )
    assert response.status_code == 200
    assert schema_check(schemas.User(**response.json()[0]))

def test_user_get_by_email_bad_email():
    response = client.get(
        "/user/get/by-email?email=invalid@bad.net",
        headers = {"X-API-Key" : api_key}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "No users with `email` == invalid@bad.net exist."
    }

def test_user_get_by_email_no_apikey():
    response = client.get(
        "/user/get/by-email?email=kenny@beardedtek.com"
    )
    assert response.status_code == 403

def test_user_get_by_email_bad_apikey():
    response = client.get(
        "/user/get/by-email?email=kenny@beardedtek.com",
        headers = {"X-API-Key" : "invalid-key"}
    )
    assert response.status_code == 401

# /user/get/by-id
def test_user_get_by_id():
    user_id = 1
    response = client.get(
        f"/user/get/by-id?user_id={user_id}",
        headers = {"X-API-Key" : api_key}
    )
    assert response.status_code == 200
    assert schema_check(schemas.User(**response.json()[0]))

def test_user_get_by_id_bad_id():
    user_id = 4242
    response = client.get(
        f"/user/get/by-id?user_id={user_id}",
        headers = {"X-API-Key" : api_key}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": f"No users with `user_id` == `{user_id}` exist."
    }

def test_user_get_by_id_no_apikey():
    user_id = 1
    response = client.get(
        f"/user/get/by-id?user_id={user_id}",
    )
    assert response.status_code == 403

def test_user_get_by_id_bad_apikey():
    user_id = 1
    response = client.get(
        f"/user/get/by-id?user_id={user_id}",
        headers = {"X-API-Key" : "invalid-key"}
    )
    assert response.status_code == 401

# /site/get/all
def test_site_get_all():
    response = client.get(
        "/site/get/all",
        headers = {"X-API-Key" : api_key}
    )
    assert response.status_code == 200
    assert schema_check(schemas.Site(**response.json()[0]))

def test_site_get_all_no_apikey():
    response = client.get(
        "/site/get/all"
    )
    assert response.status_code == 403

def test_site_get_all_bad_apikey():
    response = client.get(
        "/site/get/all",
        headers = {"X-API-Key" : "invalid-key"}
    )
    assert response.status_code == 401