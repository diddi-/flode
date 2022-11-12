from unittest import TestCase

from wsgi.di.container import Container


class TestContainer(TestCase):
    def test_container_can_resolve_single_dependency(self) -> None:
        class HttpClient:
            pass

        class Service:
            def __init__(self, http: HttpClient):
                self.http = http

        container = Container()
        container.resolve(HttpClient).using(HttpClient)
        container.resolve(Service).using(Service)

        instance = container.get_instance(Service)
        self.assertIsInstance(instance, Service)
        self.assertIsInstance(instance.http, HttpClient)

    def test_container_can_resolve_instances_with_custom_arguments(self) -> None:
        class Service:
            def __init__(self, name: str = "default") -> None:
                self.name = name

        expected_name = "custom_name"
        container = Container()
        container.resolve(Service).using(Service, {"name": expected_name})

        instance = container.get_instance(Service)
        self.assertIsInstance(instance, Service)
        self.assertEqual(expected_name, instance.name)
