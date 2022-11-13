from unittest import TestCase

from wsgi.di.container import Container
from wsgi.di.exceptions.missing_dependency_exception import MissingDependencyException
from wsgi.di.exceptions.service_not_configured_exception import ServiceNotConfiguredException
from wsgi.di.provider.lifetime import Lifetime


class TestContainer(TestCase):

    def test_service_not_configured_is_raised_when_attempting_to_get_service_not_in_the_container(self) -> None:
        class Service: pass
        container = Container()
        with self.assertRaises(ServiceNotConfiguredException) as err:
            self.assertIsInstance(container.get_service(Service), Service)

        self.assertRegex(str(err.exception), r"No service has been configured for '.*\.Service'")

    def test_container_can_resolve_service_without_dependencies(self) -> None:
        class Service: pass
        container = Container()
        container.add_service(Service).using(Service)
        self.assertIsInstance(container.get_service(Service), Service)

    def test_container_can_resolve_single_dependency(self) -> None:
        class HttpClient:
            pass

        class Service:
            def __init__(self, http: HttpClient):
                self.http = http

        container = Container()
        container.add_service(HttpClient).using(HttpClient)
        container.add_service(Service).using(Service)

        instance = container.get_service(Service)
        self.assertIsInstance(instance, Service)
        self.assertIsInstance(instance.http, HttpClient)

    def test_container_can_resolve_instances_with_custom_arguments(self) -> None:
        class Service:
            def __init__(self, name: str = "default") -> None:
                self.name = name

        expected_name = "custom_name"
        container = Container()
        container.add_service(Service).using(Service, kwargs={"name": expected_name})

        instance = container.get_service(Service)
        self.assertIsInstance(instance, Service)
        self.assertEqual(expected_name, instance.name)

    def test_singleton_instances_can_be_added(self) -> None:
        class MySingleton: pass

        container = Container()
        container.add_service(MySingleton).using(MySingleton, Lifetime.SINGLETON)

        instance1 = container.get_service(MySingleton)
        instance2 = container.get_service(MySingleton)
        self.assertEqual(instance1, instance2)

    def test_methods_without_dependencies_can_be_invoked(self) -> None:
        class Service:
            def do_work(self) -> str:
                return "Works"

        container = Container()
        container.add_service(Service).using(Service)
        service = container.get_service(Service)
        self.assertEqual("Works", container.invoke(service.do_work))

    def test_methods_with_dependencies_can_be_invoked(self) -> None:
        class Dependency: pass
        class Service:
            def do_work(self, dep: Dependency) -> Dependency:
                return dep

        container = Container()
        container.add_service(Dependency).using(Dependency)
        container.add_service(Service).using(Service)
        instance = container.get_service(Service)

        dependency = container.invoke(instance.do_work)
        self.assertIsInstance(dependency, Dependency)

    def test_missing_dependency_exception_is_raised_when_no_dependency_could_be_found_for_instance(self) -> None:
        class Dependency: pass
        class Service:
            def __init__(self, dep: Dependency) -> None: pass

        container = Container()
        container.add_service(Service).using(Service)

        with self.assertRaises(MissingDependencyException) as err:
            container.get_service(Service)

        self.assertRegex(str(err.exception),
                         r"Parameter 'dep: .*\.Dependency' could not be resolved for '.*\.Service'")

    def test_missing_dependency_exception_is_raised_when_no_dependency_could_be_found_for_static_method(self) -> None:
        class Dependency: pass
        class Service:
            @staticmethod
            def do_work(dep: Dependency) -> None: pass

        container = Container()
        container.add_service(Service).using(Service)

        with self.assertRaises(MissingDependencyException) as err:
            container.invoke(Service.do_work)

        self.assertRegex(str(err.exception),
                         r"Parameter 'dep: .*\.Dependency' could not be resolved for '.*\.Service.do_work'")

    def test_missing_dependency_exception_is_raised_when_no_dependency_could_be_found_for_method(self) -> None:
        class Dependency: pass
        class Service:
            def do_work(self, dep: Dependency) -> None: pass

        container = Container()
        container.add_service(Service).using(Service)

        with self.assertRaises(MissingDependencyException) as err:
            container.invoke(Service().do_work)

        self.assertRegex(str(err.exception),
                         r"Parameter 'dep: .*\.Dependency' could not be resolved for '.*\.Service.do_work'")
    def test_missing_dependency_exception_is_raised_when_no_dependency_could_be_found_for_function(self) -> None:
        class Dependency: pass
        def do_work(dep: Dependency) -> None: pass

        container = Container()
        with self.assertRaises(MissingDependencyException) as err:
            container.invoke(do_work)

        self.assertRegex(str(err.exception),
                         r"Parameter 'dep: .*\.Dependency' could not be resolved for '.*\.do_work'")
