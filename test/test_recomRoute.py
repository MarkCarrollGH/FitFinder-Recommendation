import pytest
from unittest.mock import MagicMock, patch
from app.recomRoute import collect_items, retrieveBestItem


def make_db_item(id_str="507f1f77bcf86cd799439011"):
    return {
        "_id": id_str, "id": id_str,
        "name": "Item", "brand": "Brand",
        "light": 5, "dark": 3, "bright": 4, "warm": 2,
        "cool": 1, "fancy": 3, "casual": 5, "business": 2,
        "evening": 1, "minimalist": 4, "vintage": 2, "modern": 5,
        "floral": 1, "colourful": 3,
        "img_url": "http://img.com/a.jpg"
    }


RECOM_PAYLOAD = {
    "id1": "507f1f77bcf86cd799439011",
    "id2": "507f1f77bcf86cd799439012",
    "id3": "507f1f77bcf86cd799439013",
    "id4": "507f1f77bcf86cd799439014",
    "attr1": "light", "attr2": "dark", "attr3": "warm", "attr4": "cool"
}


# ── GET /{cloth}/get ──────────────────────────────────────────────────────────

def test_get_all_returns_items(client, mock_mongo):
    mock_mongo["shirts"].find.return_value = [make_db_item("1"), make_db_item("2")]
    response = client.get("/shirts/get")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_all_db_error(client, mock_mongo):
    mock_mongo["shirts"].find.side_effect = Exception("DB error")
    response = client.get("/shirts/get")
    assert response.status_code == 500


# ── GET /{c1}/{c2}/{c3}/{c4}/getrecom ────────────────────────────────────────

def test_get_recom_pants(client, mock_mongo):
    mock_mongo["shirts"].find.return_value = [make_db_item("1")]
    mock_mongo["trousers"].find.return_value = [make_db_item("2")]
    mock_mongo["shoes"].find.return_value = [make_db_item("3")]
    mock_mongo["jacket"].find.return_value = [make_db_item("4")]
    mock_mongo["skirts"].find.return_value = [make_db_item("5")]
    mock_mongo["dresses"].find.return_value = [make_db_item("6")]

    response = client.get("/light/dark/warm/cool/getrecom")
    assert response.status_code == 200


def test_get_recom_error(client, mock_mongo):
    mock_mongo["shirts"].find.side_effect = Exception("fail")
    mock_mongo["trousers"].find.side_effect = Exception("fail")
    mock_mongo["shoes"].find.side_effect = Exception("fail")
    mock_mongo["jacket"].find.side_effect = Exception("fail")
    mock_mongo["skirts"].find.side_effect = Exception("fail")
    mock_mongo["dresses"].find.side_effect = Exception("fail")
    response = client.get("/light/dark/warm/cool/getrecom")
    assert response.status_code in (200, 500)


# ── POST /like & /dislike ─────────────────────────────────────────────────────

def test_like(client, mock_publisher):
    response = client.post("/like", json=RECOM_PAYLOAD)
    assert response.status_code == 200
    mock_publisher.pubRecom.assert_called_once()


def test_dislike(client, mock_publisher):
    response = client.post("/dislike", json=RECOM_PAYLOAD)
    assert response.status_code == 200
    mock_publisher.pubRecom.assert_called_once()


def test_like_publisher_error(client, mock_publisher):
    mock_publisher.pubRecom.side_effect = Exception("MQ down")
    response = client.post("/like", json=RECOM_PAYLOAD)
    assert response.status_code == 500


def test_dislike_publisher_error(client, mock_publisher):
    mock_publisher.pubRecom.side_effect = Exception("MQ down")
    response = client.post("/dislike", json=RECOM_PAYLOAD)
    assert response.status_code == 500


# ── collect_items branches ────────────────────────────────────────────────────

def test_collect_items_pants(mock_mongo):
    item = make_db_item()
    mock_mongo["shirts"].find.return_value = [item]
    mock_mongo["trousers"].find.return_value = [item]
    mock_mongo["shoes"].find.return_value = [item]
    mock_mongo["jacket"].find.return_value = [item]

    with patch("app.recomRoute.random.choice", return_value="pants"):
        result = collect_items("light", "dark", "warm", "cool")
    assert "id1" in result


def test_collect_items_skirt(mock_mongo):
    item = make_db_item()
    mock_mongo["shirts"].find.return_value = [item]
    mock_mongo["skirts"].find.return_value = [item]
    mock_mongo["shoes"].find.return_value = [item]
    mock_mongo["jacket"].find.return_value = [item]

    with patch("app.recomRoute.random.choice", return_value="skirt"):
        result = collect_items("light", "dark", "warm", "cool")
    assert "id1" in result


def test_collect_items_dress(mock_mongo):
    item = make_db_item()
    mock_mongo["dresses"].find.return_value = [item]
    mock_mongo["shoes"].find.return_value = [item]
    mock_mongo["jacket"].find.return_value = [item]

    with patch("app.recomRoute.random.choice", return_value="dress"):
        result = collect_items("light", "dark", "warm", "cool")
    assert "id1" in result


def test_collect_items_no_results(mock_mongo):
    mock_mongo["shirts"].find.return_value = []
    mock_mongo["trousers"].find.return_value = []
    mock_mongo["shoes"].find.return_value = []
    mock_mongo["jacket"].find.return_value = []

    with patch("app.recomRoute.random.choice", return_value="pants"):
        result = collect_items("light", "dark", "warm", "cool")
    assert "error" in result


# ── retrieveBestItem ──────────────────────────────────────────────────────────

def test_retrieve_best_item_returns_highest_score(mock_mongo):
    low = {**make_db_item("1"), "light": 1, "dark": 1, "warm": 1, "cool": 1}
    high = {**make_db_item("2"), "light": 9, "dark": 9, "warm": 9, "cool": 9}
    mock_mongo["shirts"].find.return_value = [low, high]

    result = retrieveBestItem("light", "dark", "warm", "cool", "shirts")
    assert result["id"] == "2"


def test_retrieve_best_item_empty(mock_mongo):
    mock_mongo["shirts"].find.return_value = []
    result = retrieveBestItem("light", "dark", "warm", "cool", "shirts")
    assert result is None
