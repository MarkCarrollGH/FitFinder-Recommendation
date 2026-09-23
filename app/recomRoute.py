from fastapi import FastAPI, APIRouter, Body, Request, Response, HTTPException, status
from dotenv import dotenv_values
from bson import ObjectId
from .models import *
from .config import db
from .publish import get_rabbitmq_publisher
import random

choice = ["pants", "skirt", "dress"]

recomRouter = APIRouter()

@recomRouter.get("/{cloth}/get")
async def get_all(cloth: str):
    try:
        data = list(db[cloth].find())
        return all_items(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching {cloth}: {e}")

@recomRouter.get("/{c1}/{c2}/{c3}/{c4}/getrecom")
async def get_recom(c1: str,c2: str,c3: str,c4: str):
    try:
        recom = collect_items(c1,c2,c3,c4)
        return recom
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendation: {e}")

@recomRouter.post("/dislike")
async def dislike(recom: recomReturn):
    try:
        publisher = get_rabbitmq_publisher()
        publisher.pubRecom(
            "recom_topic",
            "recom_queue",
            pub_recom_return(recom,-1)
        )
        return recom
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendation: {e}")

@recomRouter.post("/like")
async def like(recom: recomReturn):
    try:
        publisher = get_rabbitmq_publisher()
        publisher.pubRecom(
            "recom_topic",
            "recom_queue",
            pub_recom_return(recom,1)
        )
        return recom
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendation: {e}")

def collect_items(c1: str, c2: str, c3: str, c4: str):
    select = random.choice(choice)
    if select == "pants":
        rec1 = retrieveBestItem(c1,c2,c3,c4,"shirts")
        rec2 = retrieveBestItem(c1,c2,c3,c4,"trousers")
        rec3 = retrieveBestItem(c1,c2,c3,c4,"shoes")
        rec4 = retrieveBestItem(c1,c2,c3,c4,"jacket")
        if not all([rec1, rec2, rec3, rec4]):
            return {"error": "No recommendation found"}
        return recom_return(rec1,rec2,rec3,rec4)

    elif select == "skirt":
        rec1 = retrieveBestItem(c1,c2,c3,c4,"shirts")
        rec2 = retrieveBestItem(c1,c2,c3,c4,"skirts")
        rec3 = retrieveBestItem(c1,c2,c3,c4,"shoes")
        rec4 = retrieveBestItem(c1,c2,c3,c4,"jacket")
        if not all([rec1, rec2, rec3, rec4]):
            return {"error": "No recommendation found"}
        return recom_return(rec1,rec2,rec3,rec4)

    elif select == "dress":
        rec1 = retrieveBestItem(c1,c2,c3,c4,"dresses")
        rec2 = retrieveBestItem(c1,c2,c3,c4,"shoes")
        rec3 = retrieveBestItem(c1,c2,c3,c4,"jacket")
        if not all([rec1, rec2, rec3]):
            return {"error": "No recommendation found"}
        return recom_return3(rec1,rec2,rec3)
    
    return {"error": "No recommendation found"}

def retrieveBestItem(c1: str, c2: str, c3: str, c4: str, cloth: str):
    data = list(db[cloth].find())
    greatestValue = 0
    bestItem = None
    for item in data:
        score = (item.get(c1, 0) + item.get(c2, 0) + item.get(c3, 0) + item.get(c4, 0))
        if score > greatestValue:
            greatestValue = score
            bestItem = item_return(item)
    
    return bestItem


    