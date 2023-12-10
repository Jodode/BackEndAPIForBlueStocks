from sqlalchemy import DateTime, Float, Boolean, Column, ForeignKey, Integer, String, BigInteger, Date, Time
from database import Base

class Default_Ticker():
    id = Column(BigInteger, primary_key=True, index=True)
    ticker = Column(String)
    tradedate = Column(Date)
    tradetime = Column(Time)
    pr_open = Column(Float)
    pr_high = Column(Float)
    pr_low = Column(Float)
    pr_close = Column(Float)
    pr_std = Column(Float)
    vol = Column(BigInteger)
    val = Column(Float)
    trades = Column(BigInteger)
    pr_vwap = Column(Float)
    pr_change = Column(Float)
    trades_b = Column(BigInteger)
    trades_s = Column(BigInteger)
    val_b = Column(Float)
    val_s = Column(Float)
    vol_b = Column(BigInteger)
    vol_s = Column(BigInteger)
    disb = Column(Float)
    pr_vwap_b = Column(Float)
    pr_vwap_s = Column(Float)
    time_stamp = Column(DateTime)

class GAZP_Ticker(Base, Default_Ticker):
    __tablename__ = "gazp"

class SBER_Ticker(Base, Default_Ticker):
    __tablename__ = "sber"

class LKOH_Ticker(Base, Default_Ticker):
    __tablename__ = "lkoh"

class SNGS_Ticker(Base, Default_Ticker):
    __tablename__ = "sngs"

class CHMF_Ticker(Base, Default_Ticker):
    __tablename__ = "chmf"

class YNDX_Ticker(Base, Default_Ticker):
    __tablename__ = "yndx"

class GMKN_Ticker(Base, Default_Ticker):
    __tablename__ = "gmkn"

class MOEX_Ticker(Base, Default_Ticker):
    __tablename__ = "moex"

class MTSS_Ticker(Base, Default_Ticker):
    __tablename__ = "mtss"

class TCSG_Ticker(Base, Default_Ticker):
    __tablename__ = "tcsg"

class ROSN_Ticker(Base, Default_Ticker):
    __tablename__ = "rosn"

class ALRS_Ticker(Base, Default_Ticker):
    __tablename__ = "alrs"

class PHOR_Ticker(Base, Default_Ticker):
    __tablename__ = "phor"

class PLZL_Ticker(Base, Default_Ticker):
    __tablename__ = "plzl"

class RUAL_Ticker(Base, Default_Ticker):
    __tablename__ = "rual"

class TATN_Ticker(Base, Default_Ticker):
    __tablename__ = "tatn"

class POLY_Ticker(Base, Default_Ticker):
    __tablename__ = "poly"

class NVTK_Ticker(Base, Default_Ticker):
    __tablename__ = "nvtk"



