from typing import List

from flode.http_method import HttpMethod
from flode.middleware.endpoint.class_endpoint import ClassEndpoint
from flode.middleware.router.route_pattern import RoutePattern
from flode.middleware.router.url_path import UrlPath


class EndpointCollection:
    def __init__(self) -> None:
        self._endpoints: List[ClassEndpoint] = []

    def add(self, endpoint: ClassEndpoint) -> None:
        self._endpoints.append(endpoint)

    def get_all_routes(self) -> List[RoutePattern]:
        routes: List[RoutePattern] = []
        for endpoint in self._endpoints:
            routes.append(endpoint.route.pattern)

        return routes

    def has_endpoint(self, path: UrlPath, http_method: HttpMethod) -> bool:
        try:
            self.get_endpoint(path, http_method)
            return True
        except ValueError:
            return False

    def get_endpoint(self, path: UrlPath, http_method: HttpMethod) -> ClassEndpoint:
        for endpoint in self._endpoints:
            if endpoint.route.pattern.matches(path) and http_method in endpoint.route.http_methods:
                return endpoint
        raise ValueError(f"No endpoint matches {http_method} {path}")
