from fastapi.testclient import TestClient
from os import environ
import sys

from api.main import app
import api.schemas as schemas
from api.helpers.checks import schema_check

if "TEST_KEY" not in environ:
    sys.exit("You must set \'TEST_KEY\' environment variable")
TEST_KEY = environ["TEST_KEY"]
good_bearer = {'Authorization': f"Bearer {TEST_KEY}"}
bad_bearer = {'Authorization': f"Bearer {TEST_KEY}-BAD"}
no_bearer = {}

client = TestClient(app)


# /author/get/all
def test_author_get_all():
    response = client.get(
        "/author/get/all",
        headers = good_bearer
    )
    assert response.status_code == 200
    assert schema_check(schemas.Author(**response.json()[0]))

def test_author_get_all_no_apikey():
    response = client.get(
        "/author/get/all"
    )
    assert response.status_code == 403

def test_author_get_all_bad_apikey():
    response = client.get(
        "/author/get/all",
        headers = bad_bearer
    )
    assert response.status_code == 400

# /author/get/by-email
def test_author_get_by_email():
    response = client.get(
        "/author/get/by-email?email=kenny@beardedtek.com",
        headers = good_bearer
    )
    assert response.status_code == 200
    assert schema_check(schemas.Author(**response.json()[0]))

def test_author_get_by_email_bad_email():
    response = client.get(
        "/author/get/by-email?email=invalid@bad.net",
        headers = good_bearer
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "no records"
    }

def test_author_get_by_email_no_apikey():
    response = client.get(
        "/author/get/by-email?email=kenny@beardedtek.com"
    )
    assert response.status_code == 403

def test_author_get_by_email_bad_apikey():
    response = client.get(
        "/author/get/by-email?email=kenny@beardedtek.com",
        headers = bad_bearer
    )
    assert response.status_code == 400

# /author/get/by-id
def test_author_get_by_id():
    id = 1
    response = client.get(
        f"/author/get/by-id?id={id}",
        headers = good_bearer
    )
    assert response.status_code == 200
    assert schema_check(schemas.Author(**response.json()[0]))

def test_author_get_by_id_bad_id():
    id = 4242
    response = client.get(
        f"/author/get/by-id?id={id}",
        headers = good_bearer
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": f"no records"
    }

def test_author_get_by_id_no_apikey():
    id = 1
    response = client.get(
        f"/author/get/by-id?id={id}",
    )
    assert response.status_code == 403

def test_author_get_by_id_bad_apikey():
    id = 1
    response = client.get(
        f"/author/get/by-id?id={id}",
        headers = bad_bearer
    )
    assert response.status_code == 400

# /site/get/all
def test_site_get_all():
    response = client.get(
        "/site/get/all",
        headers = good_bearer
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
        headers = bad_bearer
    )
    assert response.status_code == 400