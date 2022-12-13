# dnsmasq-api

A VERY simple API for adding and removing IP addresses from the `dnsmasq` DNS forwarder.

## Requirements
- Python 3.6 or later
- `fastapi`
- `uvicorn`

## Usage
To start the API server, run:
```
uvicorn app:app --reload
```
To add an IP address to the `dnsmasq` configuration, send a `POST` request to the `/ip` endpoint with the following JSON data:
```
{"ip": "1.2.3.4", "domain": "example.com"}
```
To get information about an IP address or domain, send a `GET` request to the corresponding `/ip/{ip}` or `/domain/{domain}` endpoint.

To remove an IP address from the `dnsmasq` configuration, send a `DELETE` request to the `/ip/{ip}` endpoint.

## Endpoints
- `POST /ip`: Add an IP address to the `dnsmasq` configuration.
- `GET /ip/{ip}`: Get information about the specified IP address.
- `GET /domain/{domain}`: Get information about the specified domain.
- `DELETE /ip/{ip}`: Remove the specified IP address from the `dnsmasq` configuration.

## Example with docker
Start with docker
```
docker build -t dnsmasq-api . 
docker run --rm -p 8000:8000 dnsmasq-api
```
Use curl
```
➜ curl -X POST 'http://localhost:8000/ip?ip=1.1.1.1&domain=example.com'
{"status":"success"}

➜ curl -X GET http://localhost:8000/ip/1.1.1.1
{"status":"success","info":"address=/example.com/1.1.1.1\n"}

➜ curl -X DELETE http://localhost:8000/ip/1.1.1.1
{"status":"success"}
```