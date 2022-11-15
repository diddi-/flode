from unittest import TestCase

from wsgi.di.container import Container
from wsgi.di.exceptions.missing_dependency_exception import MissingDependencyException
from wsgi.di.exceptions.service_not_configured_exception import ServiceNotConfiguredException
from wsgi.di.provider.lifetime import Lifetime
from wsgi.di.type_check import TypeCheck


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
        container.register(Service)
        self.assertIsInstance(container.get_service(Service), Service)

    def test_container_can_resolve_single_dependency(self) -> None:
        class HttpClient:
            pass

        class Service:
            def __init__(self, http: HttpClient):
                self.http = http

        container = Container()
        container.register(HttpClient)
        container.register(Service)

        instance = container.get_service(Service)
        self.assertIsInstance(instance, Service)
        self.assertIsInstance(instance.http, HttpClient)

    def test_container_can_resolve_instances_with_custom_arguments(self) -> None:
        # THIS WILL FAIL FOR NOW
        class Service:
            def __init__(self, name: str = "default") -> None:
                self.name = name

        expected_name = "custom_name"
        container = Container()
        container.register(Service)

        instance = container.get_service(Service)
        self.assertIsInstance(instance, Service)
        self.assertEqual(expected_name, instance.name)

    def test_singleton_instances_can_be_added(self) -> None:
        class MySingleton: pass

        container = Container()
        container.register(MySingleton, lifetime=Lifetime.SINGLETON)

        instance1 = container.get_service(MySingleton)
        instance2 = container.get_service(MySingleton)
        self.assertEqual(instance1, instance2)

    def test_methods_without_dependencies_can_be_invoked(self) -> None:
        class Service:
            def do_work(self) -> str:
                return "Works"

        container = Container()
        container.register(Service)
        service = container.get_service(Service)
        self.assertEqual("Works", container.invoke(service.do_work))

    def test_methods_with_dependencies_can_be_invoked(self) -> None:
        class Dependency: pass
        class Service:
            def do_work(self, dep: Dependency) -> Dependency:
                return dep

        container = Container()
        container.register(Dependency)
        container.register(Service)

        instance = container.get_service(Service)
        dependency = container.invoke(instance.do_work)
        self.assertIsInstance(dependency, Dependency)

    def test_missing_dependency_exception_is_raised_when_no_dependency_could_be_found_for_instance(self) -> None:
        class Dependency: pass
        class Service:
            def __init__(self, _dep: Dependency) -> None: pass

        container = Container()
        container.register(Service)

        with self.assertRaises(MissingDependencyException) as err:
            container.get_service(Service)

        self.assertRegex(str(err.exception),
                         r"Parameter '_dep: .*\.Dependency' could not be resolved for '.*\.Service'")

    def test_missing_dependency_exception_is_raised_when_no_dependency_could_be_found_for_static_method(self) -> None:
        class Dependency: pass
        class Service:
            @staticmethod
            def do_work(dep: Dependency) -> None: pass

        container = Container()
        container.register(Service)

        with self.assertRaises(MissingDependencyException) as err:
            container.invoke(Service.do_work)

        self.assertRegex(str(err.exception),
                         r"Parameter 'dep: .*\.Dependency' could not be resolved for '.*\.Service.do_work'")

    def test_missing_dependency_exception_is_raised_when_no_dependency_could_be_found_for_method(self) -> None:
        class Dependency: pass
        class Service:
            def do_work(self, dep: Dependency) -> None: pass

        container = Container()
        container.register(Service)

        with self.assertRaises(MissingDependencyException) as err:
            container.invoke(Service().do_work)

        self.assertRegex(str(err.exception),
                         r"Parameter 'dep: .*\.Dependency' could not be resolved for '.*\.Service.do_work'")
    def test_missing_dependency_exception_is_raised_when_no_dependency_could_be_found_for_function(self) -> None:
        class Dependency: pass
        def do_work(_dep: Dependency) -> None: pass

        container = Container()
        with self.assertRaises(MissingDependencyException) as err:
            container.invoke(do_work)

        self.assertRegex(str(err.exception),
                         r"Parameter '_dep: .*\.Dependency' could not be resolved for '.*\.do_work'")

    def test_implementing_class_must_be_of_same_type_as_service_when_in_strict_mode(self) -> None:
        class Service: pass
        class NotConcrete: pass

        container = Container()
        with self.assertRaises(ValueError) as err:
            container.register(Service, NotConcrete)
        self.assertRegex(str(err.exception), r"'.*\.NotConcrete' can't be registered")

    def test_implementing_class_does_not_have_to_be_same_type_as_service_when_in_strict_mode(self) -> None:
        class Service: pass
        class NotConcrete: pass

        container = Container()
        container.register(Service, NotConcrete, type_check=TypeCheck.LOOSE)
        self.assertTrue(container.has_service(Service))
        self.assertIsInstance(container.get_service(Service), NotConcrete)

    def test_service_can_be_registered_by_service_type_only(self) -> None:
        class Service: pass
        container = Container()
        container.register(Service)

        self.assertTrue(container.has_service(Service))

    def test_service_can_be_registered_with_concrete_class(self) -> None:
        class Service: pass
        class Concrete(Service): pass

        container = Container()
        container.register(Service, Concrete)

        self.assertTrue(container.has_service(Service))
