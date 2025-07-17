from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import os
from lib_utils.logger import get_logger

logger = get_logger(__name__)

class PDFReportBuilder:
    def __init__(self, template_dir: str = "templates/"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template("risk_report.html")

    def generate_pdf(self, report_data: dict, output_path: str) -> None:
        """Generate PDF report from structured data"""
        # Render HTML
        html_content = self.template.render(
            report=report_data,
            logo=os.path.abspath("templates/rothschild_logo.png")
        )
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_path)
        logger.info(f"Generated PDF report at {output_path}")

# Sample template structure (templates/risk_report.html)
"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { display: flex; align-items: center; }
        .logo { height: 50px; margin-right: 20px; }
        .section { margin-bottom: 25px; }
        .risk-metric { background-color: #f5f5f5; padding: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <img src="{{ logo }}" class="logo">
        <h1>Portfolio Risk Report</h1>
    </div>
    
    <div class="section">
        <h2>Market Commentary</h2>
        <p>{{ report.narrative.market_commentary }}</p>
    </div>
    
    <div class="section">
        <h2>Risk Metrics</h2>
        <div class="risk-metric">
            <p><strong>1-Day 99% VaR:</strong> {{ report.metrics.var_99 | format_currency }}</p>
            <p><strong>Expected Shortfall:</strong> {{ report.metrics.es_99 | format_currency }}</p>
        </div>
    </div>
    
    <div class="section">
        <h2>Recommended Actions</h2>
        <ul>
            {% for action in report.narrative.recommended_actions %}
            <li>{{ action }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""