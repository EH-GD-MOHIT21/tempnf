import pandas as pd
from django.conf import settings
import os

def create_csv_base_data(users,marks,emails,id):
    df = pd.DataFrame([users,emails,marks])
    df = df.T
    df.columns = ["user","email","marks"]
    df.to_excel(os.path.join(settings.BASE_DIR,f'media/{id}.xlsx'),index=False)
