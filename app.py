from ipaddress import IPv4Address
import re as regex
import subprocess
from fastapi import FastAPI, HTTPException

# Create a new FastAPI instance
app = FastAPI()

@app.post("/ip")
def add_ip_to_dnsmasq(ip: str, domain: str, required=True):
    # Check if the `ip` parameter is a valid IPv4 address.
    try:
        IPv4Address(ip)
    except ValueError as e:
        # If the `ip` parameter is not a valid IPv4 address, raise an HTTP exception with a status code of 400 and a detail message.
        raise HTTPException(status_code=400, detail="Invalid IP address") from e

    # Define a regular expression for matching domain names.
    domain_regex = r"^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$"

    # Check if the `domain` parameter matches the domain name regular expression.
    if not regex.match(domain_regex, domain):
        # If the `domain` parameter does not match the regular expression, raise an HTTP exception with a status code of 400 and a detail message.
        raise HTTPException(status_code=400, detail="Invalid domain name")

    # Open the `/etc/dnsmasq.conf` file in append mode.
    with open("/etc/dnsmasq.conf", "a") as f:
        # Append a line with the `ip` and `domain` parameters to the file.
        f.write(f"address=/{domain}/{ip}\n")

    restart_dnsmasq()
    # Return a JSON object with a "success" status.
    return {"status": "success"}


@app.get("/ip/{ip}")
def get_ip_info(ip: str):
    # Open the dnsmasq configuration file for reading and read all lines into a list
    with open("/etc/dnsmasq.conf", "r") as f:
        lines = f.readlines()
    # Return a dictionary containing status and IP info if a line ending with the given IP address is found,
    # otherwise return a dictionary with a "not found" status
    return next(({"status": "success", "info": line} for line in lines if line.endswith(f"{ip}\n")), {"status": "not found"})


@app.get("/domain/{domain}")
def get_domain_info(domain: str):
    # Open the dnsmasq configuration file for reading and read all lines into a list
    with open("/etc/dnsmasq.conf", "r") as f:
        lines = f.readlines()
    # Return a dictionary containing status and domain info if a line starting with the given domain address is found,
    # otherwise return a dictionary with a "not found" status
    return next(({"status": "success", "info": line} for line in lines if line.startswith(f"address=/{domain}\n")), {"status": "not found"})

@app.delete("/ip/{ip}")
def delete_ip_from_dnsmasq(ip: str):
    # Open the dnsmasq.conf file in read mode
    with open("/etc/dnsmasq.conf", "r") as f:
        lines = f.readlines()

    # Flag to track whether the IP address was found in the file
    ip_found = False

    # Open the dnsmasq.conf file in write mode
    with open("/etc/dnsmasq.conf", "w") as f:
        # Iterate over the lines in the file
        for line in lines:
            # If the line does not end with the given IP address, write it to the file
            if not line.endswith(f"{ip}\n"):
                f.write(line)
            # Otherwise, set the flag to indicate that the IP was found
            else:
                ip_found = True

    # If the IP was not found in the file, raise an exception
    if not ip_found:
        raise HTTPException(status_code=404, detail="IP not found")

    restart_dnsmasq()
    # Return a success message if the IP was found and successfully deleted from the file
    return {"status": "success"}

def restart_dnsmasq():
    """Restart the dnsmasq service."""
    try:
        subprocess.Popen(["service dnsmasq restart"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        return True
    except Exception:
        return False