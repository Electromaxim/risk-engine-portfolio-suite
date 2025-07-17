from fastapi import APIRouter
#from .zkp.exposure_verifier import ExposureVerifier
from .sgx.gramine_verifier import SGXExposureVerifier as Verifier

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