# Deluge Skill

Use this skill to manage torrents on a remote Deluge WebUI instance via JSON-RPC.

## Requirements

- Python 3 with `requests` installed
- A running Deluge WebUI
- **`--url`** is required; password must be set via the `DELUGE_PASSWORD` environment variable

## Usage

```
uv run bin/deluge_client.py --url <URL> [--verify] COMMAND
```

### Global Options

| Flag | Default | Description |
|------|---------|-------------|
| `--url` | *(required)* | Full Deluge WebUI URL (e.g. `http://deluge.home.arpa:8112`) |
| `--verify` | off | Verify SSL certificate |

SSL is determined automatically from the URL scheme (`http` vs `https`).

## Commands

### list
List all torrents with state, progress, and size.

```
uv run bin/deluge_client.py --url URL list
```

### add
Add a torrent by magnet URI or HTTP URL.

```
uv run bin/deluge_client.py --url URL add "magnet:?xt=urn:btih:..."
uv run bin/deluge_client.py --url URL add "https://example.com/file.torrent"
```

### remove
Remove a torrent by ID (full or 8-char prefix). Use `--with-data` to also delete downloaded files.

```
uv run bin/deluge_client.py --url URL remove <TORRENT_ID>
uv run bin/deluge_client.py --url URL remove <TORRENT_ID> --with-data
```

### pause
Pause a torrent by ID.

```
uv run bin/deluge_client.py --url URL pause <TORRENT_ID>
```

### resume
Resume a paused torrent by ID.

```
uv run bin/deluge_client.py --url URL resume <TORRENT_ID>
```

### call
Make a raw JSON-RPC call to the Deluge API. Params must be a JSON array string.

```
uv run bin/deluge_client.py --url URL call core.get_config_value '["download_location"]'
```

## Notes

- SSL is determined by the URL scheme; certificate verification is off by default (accommodates self-signed certs)
- Torrent IDs shown by `list` are truncated to 8 chars for display; pass the full ID to `remove`
- Use `call` for any Deluge RPC method not covered by the built-in commands
- **Always inject the password via the `exec` tool's `env` parameter** — never inline it in the command string, as that will expose it in command logs and process listings:

```json
{
  "command": "uv run bin/deluge_client.py --url http://deluge.home.arpa:8112 list",
  "env": { "DELUGE_PASSWORD": "<password>" }
}
```
