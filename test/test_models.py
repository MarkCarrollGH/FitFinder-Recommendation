from app.models import (
    pub_recom_return, recom_return, recom_return3,
    item_return, all_items, recomReturn
)


def make_item(id_str="abc123"):
    return {
        "_id": id_str, "id": id_str,
        "name": "Shirt", "brand": "Brand",
        "light": 1, "dark": 2, "bright": 3, "warm": 4,
        "cool": 5, "fancy": 1, "casual": 2, "business": 3,
        "evening": 4, "minimalist": 5, "vintage": 1, "modern": 2,
        "floral": 3, "colourful": 4,
        "img_url": "http://img.com/a.jpg"
    }


def test_item_return():
    item = make_item()
    result = item_return(item)
    assert result["id"] == "abc123"
    assert result["name"] == "Shirt"
    assert result["img_url"] == "http://img.com/a.jpg"


def test_recom_return():
    i1, i2, i3, i4 = make_item("1"), make_item("2"), make_item("3"), make_item("4")
    result = recom_return(i1, i2, i3, i4)
    assert result["id1"] == "1"
    assert result["id4"] == "4"
    assert result["name2"] == "Shirt"


def test_recom_return3():
    i1, i2, i3 = make_item("1"), make_item("2"), make_item("3")
    result = recom_return3(i1, i2, i3)
    assert result["id1"] == "1"
    assert result["id3"] == "3"
    assert "id4" not in result


def test_pub_recom_return():
    recom = recomReturn(
        id1="1", id2="2", id3="3", id4="4",
        attr1="light", attr2="dark", attr3="warm", attr4="cool"
    )
    result = pub_recom_return(recom, 1)
    assert result["rec1_id"] == "1"
    assert result["feedback"] == 1
    assert result["attr1"] == "light"


def test_all_items():
    items = [make_item("1"), make_item("2")]
    result = all_items(items)
    assert len(result) == 2
    assert result[0]["id"] == "1"


def test_recom_return_model_optional_fields():
    recom = recomReturn(
        id1="1", id2="2",
        attr1="light", attr2="dark", attr3="warm", attr4="cool"
    )
    assert recom.id3 is None
    assert recom.id4 is None
