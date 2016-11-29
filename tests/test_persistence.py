import pytest

from lazysusan import persistence


@pytest.fixture()
def memory():
    return persistence.Memory()


@pytest.fixture()
def dynamo():
    return persistence.DynamoDB()


@pytest.fixture()
def mock_table(mocker):
    resource = mocker.patch("lazysusan.persistence.boto3.resource")
    db = resource.return_value
    table = db.Table.return_value
    table.get_item.return_value = {}
    return table


def test_memory_connect(memory):
    memory.connect()
    assert memory == {}


def test_memory_save(memory):
    memory.save()
    assert memory == {}


def test_memory_putitem(memory):
    memory["name"] = "Lazy Susan"
    memory["end_session"] = True
    assert memory == {"name": "Lazy Susan", "end_session": True}


def test_dynamo_connect_empty_session(dynamo, mock_table):
    dynamo.connect()
    assert dynamo == {}


def test_dynamo_double_connect(dynamo, mock_table):
    dynamo.connect()
    dynamo.connect()
    assert mock_table.get_item.call_count == 1


def test_dynamo_putitem(dynamo):
    dynamo["name"] = "Lazy Dude"
    dynamo["end_session"] = True
    assert dynamo == {"name": "Lazy Dude", "end_session": True}


def test_dynamo_connect_existing_session(dynamo, mock_table):
    mock_table.get_item.return_value = {"Item": {"userId": "DEADBEEF"}}
    dynamo.connect()
    assert dynamo["userId"] == "DEADBEEF"


def test_dynamo_save(dynamo, mock_table):
    dynamo.connect()
    dynamo["test_name"] = "test_dynamo_save"

    dynamo.save()

    assert mock_table.put_item.call_count == 1
    args, kwargs = mock_table.put_item.call_args
    assert args == ()
    assert kwargs == {"Item": {"test_name": "test_dynamo_save"}}
