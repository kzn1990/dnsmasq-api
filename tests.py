from fastapi.testclient import TestClient
from app import app

# Create a new TestClient instance using the FastAPI app instance
client = TestClient(app)

def _wrapper_from_test(method, url, code, key, value):
    # Call the appropriate method on the TestClient instance
    # depending on the value of the `method` parameter
    if method == "post":
        result = client.post(url)
    elif method == "delete":
        result = client.delete(url)

    # Assert that the HTTP response code is as expected
    assert result.status_code == code
    # Assert that the JSON response is as expected
    assert result.json() == {key: value}
    # Return the response
    return result


def test_add_ip_to_dnsmasq():
    # Test adding a valid IP and domain to dnsmasq
    response = _wrapper_from_test("post", "/ip?ip=1.1.1.1&domain=example.com", 200, "status", "success")
    # Test adding an invalid domain name to dnsmasq
    response = _wrapper_from_test("post", "/ip?ip=25.1.1.1&domain=example", 400, "detail", "Invalid domain name")
    # Test adding an invalid IP address to dnsmasq
    response = _wrapper_from_test("post", "/ip?ip=256.1.1.1&domain=example.com", 400, "detail", "Invalid IP address")



def test_get_ip_info():
    response = client.get("/ip/1.1.1.1")
    assert response.status_code == 200
    response = client.get("/ip/1.1.1.99")
    assert response.json() == {"status": "not found"}
    
def test_get_domain_info():
    response = client.get("/domain/example.com")
    assert response.status_code == 200
    response = client.get("/domain/example.co.uk")
    assert response.json() == {"status": "not found"}

def test_delete_ip_from_dnsmasq():
    # Test deleting a exist IP and domain from dnsmasq
    response = _wrapper_from_test("delete", "/ip/1.1.1.1", 200, "status", "success")
    # Test deleting a unexist IP and domain from dnsmasq
    response = _wrapper_from_test("delete", "/ip/1.1.1.99", 404, "detail", "IP not found")