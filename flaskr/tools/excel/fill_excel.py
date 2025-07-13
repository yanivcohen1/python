import os
from datetime import date
import pandas as pd
from xltpl.writerx import BookWriter

# 1) Load the template
current_path = os.path.dirname(os.path.abspath(__file__))
writer = BookWriter(current_path + "\\template.xlsx")

# 2) Prepare your data context
context_old = {
    "report_date": date.today().strftime("%Y-%m-%d"),
    "products": [
        {"name": "Apple",  "qty": 10, "price": 0.50},
        {"name": "Banana", "qty": 20, "price": 0.20},
        {"name": "Cherry", "qty": 15, "price": 1.00},
    ],
}

contex_df = pd.DataFrame(
    {
        "name": [
            "Apple",
            "Banana",
            "Cherry",
        ],
        "qty": [10, 20, 15],
        "price": [0.5, 0.2, 1.0,],
    }
)

context = {
    "report_date": date.today().strftime("%Y-%m-%d"),
    "products": contex_df.to_dict(orient="records"),
    "total": contex_df["price"].sum(),
}

# 3) Render & save
writer.render_book([context])
writer.save(current_path + "\\filled_report.xlsx")

print("✓ Saved → filled_report.xlsx")
