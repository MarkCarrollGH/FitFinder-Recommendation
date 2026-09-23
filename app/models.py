# app/schemas.py
from pydantic import BaseModel, EmailStr, constr, conint
from typing import Optional

#----------------------------------Recom Models------------------------------------------------

def pub_recom_return(recom,feedback):
    return{
        "rec1_id": str(recom.id1),
        "rec2_id": str(recom.id2),
        "rec3_id": str(recom.id3),
        "rec4_id": str(recom.id4),
        "attr1": recom.attr1,
        "attr2": recom.attr2,
        "attr3": recom.attr3,
        "attr4": recom.attr4,
        "feedback": feedback
    }

def recom_return(rec1,rec2,rec3,rec4):
    return{
        "id1": str(rec1["id"]),
        "name1": rec1["name"],
        "img_url1": rec1["img_url"],
        "id2": str(rec2["id"]),
        "name2": rec2["name"],
        "img_url2": rec2["img_url"],
        "id3": str(rec3["id"]),
        "name3": rec3["name"],
        "img_url3": rec3["img_url"],
        "id4": str(rec4["id"]),
        "name4": rec4["name"],
        "img_url4": rec4["img_url"],
    }

def recom_return3(rec1,rec2,rec3):
    return{
        "id1": str(rec1["id"]),
        "name1": rec1["name"],
        "img_url1": rec1["img_url"],
        "id2": str(rec2["id"]),
        "name2": rec2["name"],
        "img_url2": rec2["img_url"],
        "id3": str(rec3["id"]),
        "name3": rec3["name"],
        "img_url3": rec3["img_url"],
    }



#----------------------------------------------------------------- Clothes Read -------------------------------------------------------------------

class ItemClass(BaseModel):
    name:str
    brand:str
    light:      Optional[int] = None
    dark:       Optional[int] = None
    bright:     Optional[int] = None
    warm:       Optional[int] = None
    cool:       Optional[int] = None
    fancy:      Optional[int] = None
    casual:     Optional[int] = None
    business:   Optional[int] = None
    evening:    Optional[int] = None
    minimalist: Optional[int] = None
    vintage:    Optional[int] = None
    modern:     Optional[int] = None
    floral:     Optional[int] = None
    colourful:  Optional[int] = None
    img_url:str

def item_return(item):
    return{
        "id": str(item["_id"]),
        "name": item["name"],
        "brand": item["brand"],
        "light": item["light"],
        "dark": item["dark"],
        "bright": item["bright"],
        "warm": item["warm"],
        "cool": item["cool"],
        "fancy": item["fancy"],
        "casual": item["casual"],
        "business": item["business"],
        "evening": item["evening"],
        "minimalist": item["minimalist"],
        "vintage": item["vintage"],
        "modern": item["modern"],
        "floral": item["floral"],
        "colourful": item["colourful"],
        "img_url": item["img_url"]
    }

class recomReturn(BaseModel):
    id1: str
    id2: str
    id3: Optional[str] = None
    id4: Optional[str] = None
    attr1: str
    attr2: str 
    attr3: str
    attr4: str

def return_total(c1,c2,c3,c4):
    return [item_return(item) for item in all_items if ()]

def all_items(all_items):
    return [item_return(item) for item in all_items]