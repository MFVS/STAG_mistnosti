from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import StringIO
import pandas as pd
import requests

from .routers import ws


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def read_root(request: Request):
    url_mistnosti_info = "https://ws.ujep.cz/ws/services/rest2/mistnost/getMistnostiInfo"
    vars_mistnosti = {
        "zkrBudovy": "CP",
        "pracoviste": "%",
        "typ": "%",
        "cisloMistnosti": "%",
        "outputFormatEncoding": "utf-8",
        "outputFormat": "CSV",
    }

    response = requests.get(url_mistnosti_info, params=vars_mistnosti)

    df_mistnosti = pd.read_csv(StringIO(response.text), sep=";")

    # df_mistnosti = df_mistnosti[df_mistnosti["cisloMistnosti"].str.startswith(("6.", "7."))]
    # order by cisloMistnosti
    df_mistnosti.sort_values(by=["cisloMistnosti"], inplace=True)

    # df_mistnosti["typ"] is Učebna or Laboratoř
    df_mistnosti = df_mistnosti[df_mistnosti["typ"].isin(["Učebna", "Laboratoř"])]
    
    print(df_mistnosti.columns)
    
    return templates.TemplateResponse("index.html", {"request": request, "df_mistnosti": df_mistnosti,}) # "df_rozvrh": df_rozvrh


app.include_router(ws.router)