### 2. Portfolio Service - SQLAlchemy Models
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel

class PortfolioDB(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(64), nullable=False)  # Tokenized client ID
    base_currency = Column(String(3), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    positions = relationship("PositionDB", back_populates="portfolio")

class PositionDB(Base):
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    asset_id = Column(String(20), nullable=False)  # ISIN or Bloomberg ID
    quantity = Column(Float, nullable=False)
    notional = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    portfolio = relationship("PortfolioDB", back_populates="positions")

# Pydantic models for API
class Position(BaseModel):
    asset_id: str
    quantity: float
    notional: float
    currency: str

class Portfolio(BaseModel):
    id: int
    client_id: str
    base_currency: str
    positions: list[Position]
    
    class Config:
        orm_mode = True