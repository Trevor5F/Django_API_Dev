from pytest_factoryboy import register

from factories import AdFactory, CategoryFactory, UserFactory
from tests.fixtures import user_token

pytest_plugins = "fixtures"

register(AdFactory)
register(CategoryFactory)
register(UserFactory)
