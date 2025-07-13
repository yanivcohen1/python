# pip install python-docx docxtpl
import os
import pandas as pd
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

todos_df = pd.DataFrame(
    {
        "title": [
            "Buy Domain",
            "Buy Web Hosting",
            "Set Up Wordpress",
            "Setup Payment Options",
        ],
        "description": [
            "Buy domain for company",
            "Buy web hosting service",
            "Set up wordpress for website",
            "Setup payment methods like Stripe and PayPal",
        ],
        "notes": ["", "", "Also MySQL", "Compare alternatives"],
    }
)

current_path = os.path.dirname(os.path.abspath(__file__))
doc = DocxTemplate(current_path+"\\template.docx")
Logo = InlineImage(doc, current_path+"\\image.png", width=Mm(30))
context = {
    "project_name": "Tutorial Project",
    "project_deadline": "01-04-2025",
    "person_in_charge": "Mike Smith",
    "dedicated_budget": "$5,000",
    # convert dataframe to list of dicts array
    # records = [{'title': 'Buy Domain', 'description': 'Buy domain for company', 'notes': ''}, ...]
    "todos": todos_df.to_dict(orient="records"),
    "logo": Logo,
}

# template.docx need to be closed before run this code
doc.render(context)
doc.save(current_path+"\\output.docx")
