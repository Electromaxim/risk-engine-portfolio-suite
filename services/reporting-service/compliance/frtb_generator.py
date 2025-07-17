"""
FRTB Regulatory Report Generator
Produces FINMA-compliant SA-TBT and IMA-QIS reports
"""
import pyxb
from pyxb import BIND
from lib_frtb import ns  # FRTB XBRL namespace
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import datetime

class FRTBReporter:
    def generate_sa_tbt_report(self, portfolio_data: dict) -> bytes:
        """Generate Standardized Approach Template"""
        # Create XBRL document root
        doc = ns.FRTB_Document()
        
        # Entity information
        doc.Entity = BIND(
            Identifier="CH123456789ROTHSCHILD",
            Scheme="http://www.finma.ch/lei"
        )
        
        # Portfolio data
        for position in portfolio_data["positions"]:
            item = ns.SA_TBT_PositionItem(
                InstrumentIdentifier=position["id"],
                ExposureAmount=position["notional"],
                RiskCategory=self._map_risk_category(position["asset_class"])
            )
            doc.append(item)
            
        # Convert to XML
        xml_bytes = doc.toxml("utf-8")
        
        # Digital signature (HSM integration)
        return self._sign_report(xml_bytes, "SA-TBT")
    
    def generate_ima_qis_report(self, risk_metrics: dict) -> bytes:
        """Internal Models Approach Template"""
        doc = ns.FRTB_Document()
        doc.Entity = BIND(Identifier="CH123456789ROTHSCHILD")
        
        # Risk metrics
        doc.append(ns.IMA_QIS_VarItem(
            ObservationDate=datetime.date.today(),
            ConfidenceLevel=99,
            Value=risk_metrics["var_99"]
        ))
        
        doc.append(ns.IMA_QIS_ESItem(
            ObservationDate=datetime.date.today(),
            ConfidenceLevel=97.5,
            Value=risk_metrics["expected_shortfall"]
        ))
        
        return self._sign_report(doc.toxml("utf-8"), "IMA-QIS")
    
    def _sign_report(self, xml: bytes, report_type: str) -> bytes:
        """Sign with hardware security module"""
        from hsm_client import sign  # Import HSM client
        
        signature = sign(
            data=xml,
            key_id="frtb_signing_key",
            algorithm="rsa-pkcs1-sha256"
        )
        
        # FINMA requires detached signature
        return xml + b"\n<!-- SIGNATURE: " + signature + b" -->"
    
    def _map_risk_category(self, asset_class: str) -> str:
        """Map to FRTB risk categories"""
        mapping = {
            "equity": "EQ",
            "fx": "FX",
            "commodity": "CO",
            "credit": "CR"
        }
        return mapping.get(asset_class, "OT")