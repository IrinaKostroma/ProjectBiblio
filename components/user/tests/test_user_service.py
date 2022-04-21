from attr import asdict

data = {
    'name': 'name1',
    'password': 'password1',
}

def test_add_user(service, users_repo):
    service.add_user(data)
    service.users_repo.add.assert_called_once()


def test_get_user(service, users_repo):
    data = {
        'id': 1,
    }
    assert service.get_user(**data) == users_repo.get_by_id()


def test_get_all_users(service, users_repo):
    assert service.get_all_users() == users_repo.get_all()


def test_remove_user(service, users_repo):
    service.remove_user(id=1)
    service.users_repo.remove.assert_called_once()
