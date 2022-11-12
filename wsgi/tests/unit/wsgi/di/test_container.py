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
        container.add_service(HttpClient).using(HttpClient)
        container.add_service(Service).using(Service)

        instance = container.resolve(Service)
        self.assertIsInstance(instance, Service)
        self.assertIsInstance(instance.http, HttpClient)

    def test_container_can_resolve_instances_with_custom_arguments(self) -> None:
        class Service:
            def __init__(self, name: str = "default") -> None:
                self.name = name

        expected_name = "custom_name"
        container = Container()
        container.add_service(Service).using(Service, {"name": expected_name})

        instance = container.resolve(Service)
        self.assertIsInstance(instance, Service)
        self.assertEqual(expected_name, instance.name)

    def test_singleton_instances_can_be_added(self) -> None:
        class MySingleton: pass

        container = Container()
        container.add_service(MySingleton).using_singleton(MySingleton)

        instance1 = container.resolve(MySingleton)
        instance2 = container.resolve(MySingleton)
        self.assertEqual(instance1, instance2)
