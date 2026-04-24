import urllib.parse
import src.app as app_module


def test_get_activities(client):
    r = client.get('/activities')
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_success(client):
    activity = 'Chess Club'
    email = 'new@mergington.edu'
    path = f"/activities/{urllib.parse.quote(activity)}/signup"
    r = client.post(path, params={'email': email})
    assert r.status_code == 200
    assert email in app_module.activities[activity]['participants']


def test_signup_duplicate(client):
    activity = 'Chess Club'
    email = 'dup@mergington.edu'
    path = f"/activities/{urllib.parse.quote(activity)}/signup"
    r1 = client.post(path, params={'email': email})
    assert r1.status_code == 200
    r2 = client.post(path, params={'email': email})
    assert r2.status_code == 400


def test_signup_nonexistent_activity(client):
    path = f"/activities/{urllib.parse.quote('No Club')}/signup"
    r = client.post(path, params={'email': 'a@b.com'})
    assert r.status_code == 404


def test_remove_participant_success(client):
    activity = 'Programming Class'
    email = 'temp@mergington.edu'
    signup_path = f"/activities/{urllib.parse.quote(activity)}/signup"
    client.post(signup_path, params={'email': email})
    delete_path = f"/activities/{urllib.parse.quote(activity)}/participants"
    r = client.delete(delete_path, params={'email': email})
    assert r.status_code == 200
    assert email not in app_module.activities[activity]['participants']


def test_remove_participant_not_found(client):
    activity = 'Programming Class'
    delete_path = f"/activities/{urllib.parse.quote(activity)}/participants"
    r = client.delete(delete_path, params={'email': 'nobody@mergington.edu'})
    assert r.status_code == 404


def test_root_redirect(client):
    r = client.get('/', follow_redirects=False)
    assert r.status_code in (301,302,307)
    assert r.headers.get('location') == '/static/index.html'
