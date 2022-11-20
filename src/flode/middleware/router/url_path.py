import re
from typing import List

from flode.middleware.router.exceptions.invalid_path_exception import InvalidPathException


class UrlPath:
    """ Represents the portion of a URL that comes after the host.
    For http://my.server.com/user/1/profile, the UrlPath represents /user/1/profile

    Paths always begin with and never ends with a slash.
    """
    _PATH_REGEX = re.compile(r"^/[-/A-Za-z0-9_]*[^/]?$")

    def __init__(self, path: str) -> None:
        if not path.startswith("/"):
            raise InvalidPathException(f"URL paths must begin with a '/'")
        if len(path) > 1 and path.endswith("/"):
            raise InvalidPathException(f"URL paths can't end with a '/'")
        if not self._PATH_REGEX.match(path):
            raise InvalidPathException(f"'{path}' is not a valid URL path")

        self._raw_path = path
        self._path_parts: List[str] = path.split("/")[1:]  # There's never anything left of the first '/'

    def __len__(self) -> int:
        return len(self._path_parts)

    def __getitem__(self, index: int) -> str:
        return self._path_parts[index]

    def __str__(self) -> str:
        return self._raw_path
