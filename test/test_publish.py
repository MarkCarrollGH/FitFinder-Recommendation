import pytest
from unittest.mock import MagicMock, patch
from app.publish import RabbitMQPublisher, get_rabbitmq_publisher


@pytest.fixture
def publisher():
    return RabbitMQPublisher(rabbitmq_url="amqp://guest:guest@localhost/")


@pytest.fixture
def publisher_no_url():
    return RabbitMQPublisher(rabbitmq_url=None)


# ── connect ───────────────────────────────────────────────────────────────────

def test_connect_success(publisher):
    mock_conn = MagicMock()
    mock_channel = MagicMock()
    mock_conn.channel.return_value = mock_channel

    with patch("app.publish.pika.BlockingConnection", return_value=mock_conn):
        result = publisher.connect()

    assert result is True
    mock_channel.exchange_declare.assert_called_once()


def test_connect_no_url(publisher_no_url, monkeypatch):
    monkeypatch.delenv("RABBIT_URL", raising=False)
    publisher_no_url.rabbitmq_url = None
    result = publisher_no_url.connect()
    assert result is False


def test_connect_exception(publisher):
    with patch("app.publish.pika.BlockingConnection", side_effect=Exception("refused")):
        result = publisher.connect()
    assert result is False


# ── close ─────────────────────────────────────────────────────────────────────

def test_close_open_connection(publisher):
    mock_conn = MagicMock()
    mock_conn.is_closed = False
    publisher.connection = mock_conn
    publisher.close()
    mock_conn.close.assert_called_once()


def test_close_no_connection(publisher):
    publisher.connection = None
    publisher.close()  # should not raise


def test_close_exception(publisher):
    mock_conn = MagicMock()
    mock_conn.is_closed = False
    mock_conn.close.side_effect = Exception("fail")
    publisher.connection = mock_conn
    publisher.close()  # should not raise


# ── publish_event ─────────────────────────────────────────────────────────────

def test_publish_event_success(publisher):
    mock_conn = MagicMock()
    mock_channel = MagicMock()
    mock_conn.channel.return_value = mock_channel

    with patch("app.publish.pika.BlockingConnection", return_value=mock_conn):
        result = publisher.publish_event("recom_topic", "recom_queue", {"key": "val"})

    assert result is True
    mock_channel.basic_publish.assert_called_once()


def test_publish_event_no_url(publisher_no_url, monkeypatch):
    monkeypatch.delenv("RABBIT_URL", raising=False)
    publisher_no_url.rabbitmq_url = None
    result = publisher_no_url.publish_event("recom_topic", "recom_queue", {})
    assert result is False


def test_publish_event_exception(publisher):
    with patch("app.publish.pika.BlockingConnection", side_effect=Exception("fail")):
        result = publisher.publish_event("recom_topic", "recom_queue", {})
    assert result is False


# ── pubRecom ──────────────────────────────────────────────────────────────────

def test_pub_recom_calls_publish_event(publisher):
    with patch.object(publisher, "publish_event", return_value=True) as mock_pub:
        result = publisher.pubRecom("recom_topic", "recom_queue", {"feedback": 1})
    assert result is True
    mock_pub.assert_called_once()


# ── get_rabbitmq_publisher ────────────────────────────────────────────────────

def test_get_rabbitmq_publisher_returns_instance():
    pub = get_rabbitmq_publisher()
    assert isinstance(pub, RabbitMQPublisher)
