from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import requests
from io import StringIO
import pandas as pd
import numpy as np


router = APIRouter(prefix="/ws", tags=["ws"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/schedule/{room_id}")
def get_schedule(room_id: float, request: Request):
    url_rozvrh = "https://ws.ujep.cz/ws/services/rest2/rozvrhy/getRozvrhByMistnost"
    
    vars_rozvrh = {
        "semestr": "%",
        "mistnost": room_id,
        "vsechnyCasyKonani": "true",
        "budova": "CP",
        "jenRozvrhoveAkce": "false",
        "vsechnyAkce": "true",
        "jenBudouciAkce": "false",
        "rok": "2023",
        "lang": "cs",
        "outputFormatEncoding": "utf-8",
        "outputFormat": "CSV",
    }

    response = requests.get(url_rozvrh, params=vars_rozvrh)
    df = pd.read_csv(StringIO(response.text), sep=";")
    
    df["obsazeni"] = df["obsazeni"].apply(lambda x: int(x) if not pd.isna(x) else "—")
    df["planObsazeni"] = df["planObsazeni"].apply(lambda x: int(x) if not pd.isna(x) else "—")
    
    print(df.columns)
    
    return templates.TemplateResponse("components/schedule_modal.html", {"request": request, "df_rozvrh": df})