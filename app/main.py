from fastapi import FastAPI, HTTPException, Depends
from fastapi_utils.tasks import repeat_every

from typing import Annotated, List
from fastapi.middleware.cors import CORSMiddleware
from moexalgo import Ticker
from pydantic import BaseModel
import models
from sqlalchemy.sql import text
from datetime import datetime, timedelta, date
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import asyncio, time, random

app = FastAPI()

origins = [
    # "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)

table_models = {
    "gazp": models.GAZP_Ticker,
    "sber": models.SBER_Ticker,
    "lkoh": models.LKOH_Ticker,
    "sngs": models.SNGS_Ticker,
    "chmf": models.CHMF_Ticker,
    "yndx": models.YNDX_Ticker,
    "gmkn": models.GMKN_Ticker,
    "moex": models.MOEX_Ticker,
    "mtss": models.MTSS_Ticker,
    "tcsg": models.TCSG_Ticker,
    "rosn": models.ROSN_Ticker,
    "alrs": models.ALRS_Ticker,
    "phor": models.PHOR_Ticker,
    "plzl": models.PLZL_Ticker,
    "rual": models.RUAL_Ticker,
    "tatn": models.TATN_Ticker,
    "poly": models.POLY_Ticker,
    "nvtk": models.NVTK_Ticker
}


@app.get("/api/v1/{ticker}")
async def get_data(*, ticker: str, date: str = datetime.now().strftime("%Y-%m-%d"), till_date: str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), db: Session = Depends(get_db)):
    if ticker.lower() not in table_models:
        raise HTTPException(status_code=404, detail="Tikcer not found")
    
    substraction = datetime.strptime(till_date, "%Y-%m-%d") - datetime.strptime(date, "%Y-%m-%d")

    my_query = f"""
    SELECT t.*
FROM (
  SELECT *, row_number() OVER(ORDER BY id ASC) AS row
  FROM public."{ticker.lower()}"
) t
WHERE t.row % {int((substraction.days) ** 0.5)} = 0 and t.tradedate between '{date}' and '{till_date}'
"""
    ticker_model = table_models[ticker.lower()]
    result = db.execute(text(my_query)).mappings().all()
    print(db.query(ticker_model).order_by(ticker_model.id.desc()).first().tradedate)
    return result

        
async def reconnect():
    db = SessionLocal()
    for key, ticker in table_models.items():
        last_record = db.query(ticker).order_by(ticker.id.desc()).first()
        # days = daterange(last_record.tradedate, date.today())
        last_stock = list(Ticker(key.upper()).tradestats(latest=True))[0]
        if(last_stock.ts == last_record.time_stamp):
            continue
        db_new_stock = ticker(
                ticker=last_stock.secid,
                pr_open=last_stock.pr_open,
                pr_high=last_stock.pr_high,
                pr_low=last_stock.pr_low,
                pr_close=last_stock.pr_close,
                pr_std=last_stock.pr_std,
                vol=last_stock.vol,
                val=last_stock.val,
                trades=last_stock.trades,
                pr_vwap=last_stock.pr_vwap,
                pr_change=last_stock.pr_change,
                trades_b=last_stock.trades_b,
                trades_s=last_stock.trades_s,
                val_b=last_stock.val_b,
                val_s=last_stock.val_s,
                vol_b=last_stock.vol_b,
                vol_s=last_stock.vol_s,
                disb=last_stock.disb,
                pr_vwap_b=last_stock.pr_vwap_b,
                pr_vwap_s=last_stock.pr_vwap_s,
                tradedate=last_stock.ts.date(),
                tradetime=last_stock.ts.time(),
                time_stamp=last_stock.ts
                )
        db.add(db_new_stock)
        db.commit()
    db.close()
    
@app.on_event("startup")
def update_tickers_in_tables():
    asyncio.create_task(auto_reconnect())

async def auto_reconnect():
    while True:
        await reconnect()
        await asyncio.sleep(180)   

