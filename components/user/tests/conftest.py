import pytest
from unittest.mock import Mock
from classic.messaging import Publisher
from user.application import dataclasses, interfaces
from user.application.services import UserService


@pytest.fixture
def user():
    return dataclasses.User(
        id=1,
        name='name1',
        password='password1'
    )


@pytest.fixture(scope='function')
def users_repo(user):
    users_repo = Mock(interfaces.UsersRepo)
    users_repo.add_user = Mock(return_value=user)
    users_repo.get_user = Mock(return_value=user)
    users_repo.get_all_users = Mock(return_value=[user])
    users_repo.remove_user = Mock(return_value=None)
    return users_repo


@pytest.fixture(scope='function')
def user_publisher():
    user_publisher = Mock(Publisher)
    user_publisher.plan = Mock(return_value=None)
    return user_publisher


@pytest.fixture(scope='function')
def service(users_repo, user_publisher):
    return UserService(
        users_repo=users_repo,
        publisher=user_publisher,
    )
