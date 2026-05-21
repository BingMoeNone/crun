"""GitHub release version check."""
import json
import logging
from urllib.request import Request, urlopen
from urllib.error import URLError

log = logging.getLogger(__name__)

_REPO = "BingMoeNone/crun"
_API_URL = f"https://api.github.com/repos/{_REPO}/releases/latest"
_TIMEOUT = 5

_cached_tag: str | None = None
_checked: bool = False


def _normalize(tag: str) -> str:
    return tag[1:] if tag.startswith("v") else tag


def _parse_semver(version: str) -> tuple[int, ...]:
    """Parse a version string into a comparable tuple. Returns empty tuple on failure."""
    try:
        return tuple(int(x) for x in version.split("."))
    except (ValueError, TypeError):
        return ()


def _is_newer(remote: str, local: str) -> bool:
    """Return True if remote version is strictly greater than local."""
    r = _parse_semver(remote)
    l = _parse_semver(local)
    if not r or not l:
        # Fallback: string compare (1.0.0 > 0.9.0 lexicographically for equal-length strings)
        return remote != local
    return r > l


def fetch_latest_tag() -> str | None:
    """Fetch latest release tag_name from GitHub. Cached per session."""
    global _checked, _cached_tag
    if _checked:
        return _cached_tag
    _checked = True

    try:
        req = Request(_API_URL, headers={"Accept": "application/vnd.github+json"})
        with urlopen(req, timeout=_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
            _cached_tag = data.get("tag_name", "")
    except (URLError, OSError, ValueError, KeyError) as e:
        log.debug("Failed to check latest version: %s", e)
        return None

    return _cached_tag


def check_version(local: str) -> str | None:
    """
    Compare local version against GitHub latest release.

    Returns the latest tag ONLY if it's strictly newer than local.
    Returns None if up-to-date, network error, or local is ahead (dev version).
    """
    latest = fetch_latest_tag()
    if not latest:
        return None
    remote = _normalize(latest)
    local_norm = _normalize(local)
    if _is_newer(remote, local_norm):
        return latest
    return None
