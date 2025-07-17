class BrandManager:  
    BRAND_SPEC = {  
        "primary_color": "#003366",  # Rothschild blue  
        "secondary_color": "#C0C0C0",  
        "logo": "templates/rothschild_logo.svg",  
        "fonts": {"heading": "Helvetica", "body": "Arial"}  
    }  

    def apply_branding(self, html_content: str) -> str:  
        return (  
            html_content  
            .replace("{{primary}}", self.BRAND_SPEC["primary_color"])  
            .replace("{{heading_font}}", self.BRAND_SPEC["fonts"]["heading"])  
            .replace("{{logo}}", self.BRAND_SPEC["logo"])  
        )  
        
class BrandStyleInjector:
    BRAND_CSS = """
    :root {
        --primary: #003366;
        --secondary: #C0C0C0;
        --font-heading: "Helvetica Neue", Arial, sans-serif;
        --font-body: "Georgia", serif;
    }
    .header {
        background: linear-gradient(to right, var(--primary), #001a33);
        padding: 15px;
    }
    .risk-metric {
        border-left: 4px solid var(--primary);
    }
    """
    
    def inject_style(self, html_content: str) -> str:
        return html_content.replace(
            "</head>", 
            f"<style>{self.BRAND_CSS}</style></head>"
        )