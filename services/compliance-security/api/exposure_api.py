from fastapi import APIRouter
from .zkp.exposure_verifier import ExposureVerifier

router = APIRouter()
verifier = ExposureVerifier()

@router.post("/verify-exposure")
async def verify_exposure(portfolio: PortfolioSchema):
    return {
        "verified": verifier.verify_portfolio_exposure(
            portfolio.dict(), 
            portfolio.max_exposure
        )
    }