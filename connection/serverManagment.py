import socket
import json
from pathlib import Path

def savedServers(dirPath: str) -> list[dict]:
    results: list[dict] = []
    root = Path(dirPath)
    if not root.exists():
        return results

    for path in root.rglob("*.json"):
        # print(path)
        if not path.is_file():
            continue
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            # skip unreadable or invalid json files
            continue

        if isinstance(data, dict):
            results.append(data)
        elif isinstance(data, list):
            results.extend(item for item in data if isinstance(item, dict))

    return results

def getServerInfo(sameHost: bool = False):
    hostname = socket.gethostname()

    servers: list[dict] = savedServers("/home/superstrika/cubie-1/Superstrika/connection/savedServers")
    # servers = list(filter(lambda server: server["hostname"].removesuffix(".local") != hostname if not sameHost else server["hostname"].removesuffix(".local") == hostname, servers))
    tempServers = servers
    servers: list[dict] = []
    for server in tempServers:
        if sameHost:
            if server["hostname"].removesuffix(".local") == hostname:
                servers.append(server)
        else:
            if server["hostname"].removesuffix(".local") != hostname:
                servers.append(server)     

    print(servers)

    if len(servers) == 0:
        print("No saved servers found.")
        return None

    if len(servers) == 1:
        return servers[0]

    print(f"{len(servers)} saved servers found:")
    for i in range(len(servers)):
        print(f"- {i+1}: {servers[i]["hostname"]}: {servers[i]['port']}")

    try:
        option = int(input("Enter server number: "))
        return servers[option-1]

    except IndexError:
        print("Invalid server number.\n\n")
        getServerInfo()

    except Exception as e:
        print(f"ERROR: {e}")
        return None