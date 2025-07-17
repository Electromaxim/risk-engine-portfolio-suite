from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from lib_utils.logger import get_logger
from models.portfolio_models import Portfolio, Position
from cache.redis_cache import get_cached_portfolio
from database import get_db
import auth

app = FastAPI(title="Portfolio Service API", version="1.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = get_logger(__name__)

@app.get("/portfolios/{portfolio_id}", response_model=Portfolio)
async def get_portfolio(
    portfolio_id: int,
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Verify JWT token and permissions
    user = auth.verify_token(token)
    if not auth.check_portfolio_access(user, portfolio_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Check Redis cache first
    if cached := get_cached_portfolio(portfolio_id):
        logger.info(f"Cache hit for portfolio {portfolio_id}")
        return cached
    
    # Fetch from database
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Apply data masking based on role
    masked_portfolio = auth.apply_data_masking(user, portfolio)
    return masked_portfolio

@app.post("/positions/validate")
async def validate_positions(positions: list[Position]):
    # FX and position sanity checks
    from validation import exposure_checks
    return exposure_checks.validate_position_concentrations(positions)