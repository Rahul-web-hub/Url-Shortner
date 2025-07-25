import pytest
from app.main import app, url_store, db_lock

@pytest.fixture(autouse=True)
def client():
    """
    Provides a Flask test client and ensures the in-memory store
    is cleared before and after each test for isolation.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        with db_lock:
            url_store.clear()
        yield client
        with db_lock:
            url_store.clear()


def test_health_check(client):
    """Verify the basic health check endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'


def test_shorten_url_success(client):
    """Ensure shortening a valid URL returns a 6-char code and correct redirect URL."""
    res = client.post('/api/shorten', json={'url': 'https://www.google.com'})
    assert res.status_code == 201
    data = res.get_json()
    assert 'short_code' in data
    assert len(data['short_code']) == 6
    assert data['short_url'].endswith(data['short_code'])


def test_shorten_url_invalid_input(client):
    """Check error handling for malformed or missing URL payloads."""
    # Invalid format
    res_bad = client.post('/api/shorten', json={'url': 'not-a-valid-url'})
    assert res_bad.status_code == 400
    assert b'Invalid URL format' in res_bad.data

    # Missing key
    res_missing = client.post('/api/shorten', json={})
    assert res_missing.status_code == 400
    assert b"Missing 'url'" in res_missing.data


def test_redirect_and_click_tracking(client):
    """Test the full flow: shorten → redirect → stats click increment."""
    long_url = 'https://example.com/resource'
    post_res = client.post('/api/shorten', json={'url': long_url})
    code = post_res.get_json()['short_code']

    redirect_res = client.get(f'/{code}')
    assert redirect_res.status_code == 302
    assert redirect_res.location == long_url

    stats_res = client.get(f'/api/stats/{code}')
    stats = stats_res.get_json()
    assert stats['clicks'] == 1
    assert stats['url'] == long_url


def test_not_found_errors(client):
    """Ensure 404 is returned for unknown codes in both endpoints."""
    # Redirect
    res_redir = client.get('/nosuch')
    assert res_redir.status_code == 404
    assert b'Short code not found' in res_redir.data

    # Stats
    res_stats = client.get('/api/stats/nosuch')
    assert res_stats.status_code == 404
    assert b'Short code not found' in res_stats.data


def test_duplicate_url_returns_same_short_code(client):
    """Shortening the same URL twice should yield the same code."""
    url = 'https://github.com/features/copilot'
    first = client.post('/api/shorten', json={'url': url}).get_json()['short_code']
    second = client.post('/api/shorten', json={'url': url}).get_json()['short_code']
    assert first == second
