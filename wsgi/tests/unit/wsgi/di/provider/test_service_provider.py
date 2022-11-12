from unittest import TestCase

from wsgi.di.provider.service_provider import ServiceProvider


class TestServiceProvider(TestCase):

    def test_provides_type_return_the_type_it_provides_for(self) -> None:
        class MyInterface: pass

        class MyService(MyInterface): pass

        provider = ServiceProvider[MyInterface](MyInterface, MyService)

        self.assertEqual(MyInterface, provider.provides_type)

    def test_provider_returns_the_implementing_class_type(self) -> None:
        class MyInterface: pass

        class MyService(MyInterface): pass

        provider = ServiceProvider[MyInterface](MyInterface, MyService)

        self.assertEqual(MyService, provider.provider)

    def test_get_parameters_return_a_list_of_constructor_parameters(self) -> None:
        class MyDependency: pass

        class MyService:
            def __init__(self, name: str, amount: int, dependency: MyDependency) -> None: pass

        provider = ServiceProvider[MyService](MyService, MyService)
        params = provider.get_parameters()

        self.assertEqual(3, len(params))
        name_param = params[0]
        amount_param = params[1]
        dependency_param = params[2]
        self.assertEqual("name", name_param.name)
        self.assertEqual(str, name_param.annotation)
        self.assertEqual("amount", amount_param.name)
        self.assertEqual(int, amount_param.annotation)
        self.assertEqual("dependency", dependency_param.name)
        self.assertEqual(MyDependency, dependency_param.annotation)

    def test_new_instance_is_returned_each_time_the_service_is_instantiated(self) -> None:
        class MyClass: pass

        provider = ServiceProvider[MyClass](MyClass, MyClass)
        instance1 = provider.instantiate([], {})
        instance2 = provider.instantiate([], {})
        self.assertNotEqual(instance1, instance2)
