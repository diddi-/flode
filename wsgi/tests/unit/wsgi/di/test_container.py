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

        instance = container.get_instance(Service)
        self.assertIsInstance(instance, Service)
        self.assertIsInstance(instance.http, HttpClient)

    def test_container_can_resolve_instances_with_custom_arguments(self) -> None:
        class Service:
            def __init__(self, name: str = "default") -> None:
                self.name = name

        expected_name = "custom_name"
        container = Container()
        container.add_service(Service).using(Service, {"name": expected_name})

        instance = container.get_instance(Service)
        self.assertIsInstance(instance, Service)
        self.assertEqual(expected_name, instance.name)

    def test_singleton_instances_can_be_added(self) -> None:
        class MySingleton: pass

        container = Container()
        container.add_service(MySingleton).using_singleton(MySingleton)

        instance1 = container.get_instance(MySingleton)
        instance2 = container.get_instance(MySingleton)
        self.assertEqual(instance1, instance2)

    def test_method_arguments_can_be_resolved(self) -> None:
        class Dependency: pass
        class Service:
            def do_work(self, dep: Dependency) -> Dependency:
                return dep

        container = Container()
        container.add_service(Dependency).using(Dependency)
        container.add_service(Service).using(Service)
        instance = container.get_instance(Service)

        dependency = container.invoke(instance.do_work)
        self.assertIsInstance(dependency, Dependency)
