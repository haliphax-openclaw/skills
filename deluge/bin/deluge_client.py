#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
# ]
# ///
"""
Deluge WebUI JSON-RPC CLI Client

Usage:
  python deluge_client.py --url URL --password PASSWORD [--verify] COMMAND

Options:
  --url         Deluge WebUI URL (required, e.g. http://deluge.home.arpa:8112)
  --password    WebUI password (required)
  --verify      Verify SSL certificate (default: off)

Commands:
  list                        List all torrents with state and progress
  add <uri>                   Add a torrent by magnet URI or URL
  remove <id> [--with-data]   Remove a torrent; optionally delete data
  pause <id>                  Pause a torrent
  resume <id>                 Resume a paused torrent
  call <method> [params]      Raw RPC call; params as a JSON array

Examples:
  python deluge_client.py --url http://192.168.1.10:8112 --password deluge list
  python deluge_client.py --url http://192.168.1.10:8112 --password deluge add "magnet:?xt=urn:btih:..."
  python deluge_client.py --url http://192.168.1.10:8112 --password deluge remove abc123 --with-data
  python deluge_client.py --url http://192.168.1.10:8112 --password deluge call core.get_config_value '["download_location"]'
"""
import argparse
import json
import os
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DelugeClient:
    def __init__(self, url: str, password: str, verify: bool = False):
        self.url = url.rstrip('/') + '/json'
        self.password = password
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._id = 0

    def _call(self, method: str, params: list = None):
        self._id += 1
        resp = self.session.post(self.url, json={
            "method": method,
            "params": params or [],
            "id": self._id,
        }, verify=self.verify)
        resp.raise_for_status()
        data = resp.json()
        if data.get("error"):
            raise RuntimeError(data["error"])
        return data["result"]

    def connect(self):
        if not self._call("auth.login", [self.password]):
            raise RuntimeError("Authentication failed")
        if not self._call("web.connected"):
            hosts = self._call("web.get_hosts")
            if not hosts:
                raise RuntimeError("No daemon hosts available")
            self._call("web.connect", [hosts[0][0]])

    def get_torrents(self, fields: list = None):
        fields = fields or ["name", "state", "progress", "total_size"]
        return self._call("core.get_torrents_status", [{}, fields])

    def add_magnet(self, uri: str, options: dict = None):
        return self._call("core.add_torrent_magnet", [uri, options or {}])

    def add_torrent_url(self, url: str, options: dict = None):
        return self._call("core.add_torrent_url", [url, options or {}])

    def remove_torrent(self, torrent_id: str, remove_data: bool = False):
        return self._call("core.remove_torrent", [torrent_id, remove_data])

    def pause_torrent(self, torrent_id: str):
        return self._call("core.pause_torrent", [torrent_id])

    def resume_torrent(self, torrent_id: str):
        return self._call("core.resume_torrent", [torrent_id])


def cmd_list(client, args):
    torrents = client.get_torrents()
    if not torrents:
        print("No torrents.")
        return
    for tid, t in torrents.items():
        size_gb = t["total_size"] / 1024**3
        print(f"[{tid[:8]}] {t['name']}  {t['state']}  {t['progress']:.1f}%  {size_gb:.2f} GB")

def cmd_add(client, args):
    if args.uri.startswith("magnet:"):
        tid = client.add_magnet(args.uri)
    else:
        tid = client.add_torrent_url(args.uri)
    print(f"Added: {tid}")

def cmd_remove(client, args):
    client.remove_torrent(args.id, args.with_data)
    print(f"Removed: {args.id}")

def cmd_pause(client, args):
    client.pause_torrent(args.id)
    print(f"Paused: {args.id}")

def cmd_resume(client, args):
    client.resume_torrent(args.id)
    print(f"Resumed: {args.id}")

def cmd_call(client, args):
    params = json.loads(args.params) if args.params else []
    result = client._call(args.method, params)
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Deluge WebUI JSON-RPC client")
    parser.add_argument("--url", required=True, help="Deluge WebUI URL (e.g. http://deluge.home.arpa:8112)")
    parser.add_argument("--password", default=None, help="WebUI password (or set DELUGE_PASSWORD env var)")
    parser.add_argument("--verify", action="store_true", default=False, help="Verify SSL certificate")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List torrents")

    p_add = sub.add_parser("add", help="Add torrent by magnet URI or URL")
    p_add.add_argument("uri")

    p_rm = sub.add_parser("remove", help="Remove a torrent")
    p_rm.add_argument("id", help="Torrent ID (or prefix)")
    p_rm.add_argument("--with-data", action="store_true", default=False)

    p_pause = sub.add_parser("pause", help="Pause a torrent")
    p_pause.add_argument("id", help="Torrent ID")

    p_resume = sub.add_parser("resume", help="Resume a torrent")
    p_resume.add_argument("id", help="Torrent ID")

    p_call = sub.add_parser("call", help="Raw RPC call")
    p_call.add_argument("method")
    p_call.add_argument("params", nargs="?", help="JSON array of params")

    args = parser.parse_args()

    password = os.environ.get("DELUGE_PASSWORD") or args.password
    if not password:
        parser.error("Password required: provide --password or set DELUGE_PASSWORD environment variable")

    client = DelugeClient(args.url, password, args.verify)
    client.connect()

    {"list": cmd_list, "add": cmd_add, "remove": cmd_remove, "pause": cmd_pause, "resume": cmd_resume, "call": cmd_call}[args.command](client, args)


if __name__ == "__main__":
    main()
