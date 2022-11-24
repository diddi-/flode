from inspect import signature
from typing import cast, Callable, Dict

from flode.di.container import Container
from flode.di.exceptions.missing_dependency_exception import MissingDependencyException
from flode.middleware.endpoint.endpoint import Endpoint
from flode.middleware.endpoint.endpoint_result import EndpointResult
from flode.http_context import HttpContext
from flode.middleware.middleware import Middleware
from flode.middleware.no_options import NoOptions
from flode.middleware.router.placeholder.string_placeholder import StringPlaceholder


class EndpointMiddleware(Middleware[NoOptions]):
    """ This class is responsible for calling the endpoint registered for a specific path.
        This will *always* be the last middleware in the chain. """

    def __init__(self, container: Container) -> None:
        super().__init__()
        self._container = container

    def handle_request(self, context: HttpContext) -> None:
        endpoint = context.get_endpoint()

        # NOTE: This needs better checking of the return type at runtime but also ensure static typing works.
        result = self._invoke_endpoint(context, endpoint)
        context.response.body = result.content
        context.response.status = result.status

    def _invoke_endpoint(self, context: HttpContext, endpoint: Endpoint) -> EndpointResult:
        placeholders: Dict[str, StringPlaceholder] = {}
        for placeholder in endpoint.route.pattern.get_placeholders():
            placeholders[placeholder.name] = placeholder

        sig = signature(endpoint.fn)
        args = []
        kwargs = {}
        for param in sig.parameters.values():
            # Filter *args and **kwargs. NOTE: We may want to support these in the future.
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            if self._container.has_service(param.annotation):
                instance = self._container.get_service(param.annotation)
                if param.kind in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY):
                    args.append(instance)
                else:
                    kwargs[param.name] = instance
            else:
                if param.name in placeholders:
                    # This is incredibly brittle. We rely on the fact that locations in a RoutePattern and UrlPath
                    # match perfectly.
                    if param.kind in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY):
                        args.append(context.request.path[placeholders[param.name].location])
                    else:
                        kwargs[param.name] = context.request.path[placeholders[param.name].location]
                else:
                    raise MissingDependencyException(endpoint.fn.__qualname__, param)
        return endpoint.fn(*args, **kwargs)
