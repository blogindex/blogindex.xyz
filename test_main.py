from fastapi.testclient import TestClient
import json
import randominfo

from api.main import app
import api.schemas as schemas
from api.helpers.checks import schema_check
from key import credentials

good_bearer = {'Authorization': f"Bearer {credentials['KEY']}"}
bad_bearer = {'Authorization': f"Bearer {credentials['KEY']}-BAD"}
no_bearer = {}

# Generate Random Author / Site / Post Data
author_fn = randominfo.get_first_name()
author_ln = randominfo.get_last_name()
author_topic = randominfo.get_hobbies()[0]
site_url = f"{author_fn.lower()}{author_ln.lower()}.com"
site_name = f"All About {author_topic.title()}"
site_desc = f"This iste will teach you all about {author_topic}."
post_title = f"How to {author_topic}"
post_excerpt = f"Today, we will talk all about {author_topic} and how to get started."
author_email = f"{author_fn.lower()}@{site_url}.com"
author_disp = f"{author_fn} {author_ln}"
author_lnaddr = f"{author_fn.lower()}{author_ln.lower()}@getalby.com"

author_data = {
        "email": author_email,
        "first_name": author_fn,
        "last_name": author_ln,
        "display": author_disp,
        "image": "https://theblogindex.org/img/no-image.svg",
        "avatar": "https://theblogindex.org/img/no-image.svg",
        "flags": [],
        "rating": 100,
        "disabled": False,
        "value": [author_lnaddr]
    }



bad_author_id = 99999
bad_site_id = bad_author_id


client = TestClient(app)

# /author/create
def test_author_create():
    response = client.post(
        "/author/create",
        headers= good_bearer,
        json = author_data
    )
    return_json = json.loads(response.text)
    assert response.status_code == 200
    for key in return_json:
        data = return_json[key]
        if key == "id":
            global author_id
            author_id = data
            assert isinstance(author_id,int)
        else:
            assert data == author_data[key]
    global site_data
    site_data = {
            "url": site_url,
            "name": site_name,
            "description": site_desc,
            "rating": 100,
            "flags": [],
            "disabled": False,
            "value": [author_lnaddr],
            "user_id": author_id
    }

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
        f"/author/get/by-email?email={author_data['email']}",
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
        f"/author/get/by-email?email={author_data['email']}"
    )
    assert response.status_code == 403

def test_author_get_by_email_bad_apikey():
    response = client.get(
        f"/author/get/by-email?email={author_data['email']}",
        headers = bad_bearer
    )
    assert response.status_code == 400

# /author/get/by-id
def test_author_get_by_id():
    response = client.get(
        f"/author/get/by-id?id={author_id}",
        headers = good_bearer
    )
    assert response.status_code == 200
    assert schema_check(schemas.Author(**response.json()[0]))

def test_author_get_by_id_bad_id():
    response = client.get(
        f"/author/get/by-id?id={bad_author_id}",
        headers = good_bearer
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "no records"
    }

def test_author_get_by_id_no_apikey():
    response = client.get(
        f"/author/get/by-id?id={author_id}",
    )
    assert response.status_code == 403

def test_author_get_by_id_bad_apikey():
    response = client.get(
        f"/author/get/by-id?id={author_id}",
        headers = bad_bearer
    )
    assert response.status_code == 400

# /site/create
def test_site_create():
    response = client.post(
        "/site/create",
        headers= good_bearer,
        json = site_data
    )
    return_json = json.loads(response.text)
    
    assert response.status_code == 200
    for key in return_json:
        assert key in return_json
        data = return_json[key]
        if key == "id":
            global site_id
            site_id = data
            assert isinstance(site_id,int)
        else:
            assert data == site_data[key]



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

# /site/get/by-author_email
def test_site_get_by_email():
    response = client.get(
        f"/site/get/by-author_email?author_email={author_data['email']}",
        headers = good_bearer
    )
    assert response.status_code == 200
    assert schema_check(schemas.Site(**response.json()[0]))

def test_site_get_by_email_bad_email():
    response = client.get(
        "/site/get/by-author_email?author_email=invalid@bad.net",
        headers = good_bearer
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "no records"
    }

def test_site_get_by_email_no_apikey():
    response = client.get(
        f"/site/get/by-author_email?author_email={author_data['email']}"
    )
    assert response.status_code == 403

def test_site_get_by_email_bad_apikey():
    response = client.get(
        f"/site/get/by-author_email?author_email={author_data['email']}",
        headers = bad_bearer
    )
    assert response.status_code == 400

# /site/get/by-id
def test_site_get_by_id():
    response = client.get(
        f"/site/get/by-id?id={site_id}",
        headers = good_bearer
    )
    assert response.status_code == 200
    assert schema_check(schemas.Site(**response.json()))

def test_site_get_by_id_bad_id():
    response = client.get(
        f"/site/get/by-id?id={bad_site_id}",
        headers = good_bearer
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "no records"
    }

def test_site_get_by_id_no_apikey():
    response = client.get(
        f"/site/get/by-id?id={site_id}",
    )
    assert response.status_code == 403

def test_site_get_by_id_bad_apikey():
    response = client.get(
        f"/site/get/by-id?id={site_id}",
        headers = bad_bearer
    )
    assert response.status_code == 400