from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import StringIO
import pandas as pd
import requests


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
    # url_rozvrh = "https://ws.ujep.cz/ws/services/rest2/rozvrhy/getRozvrhByMistnost"

    # for mistnost in df_mistnosti["cisloMistnosti"]:
    #     with st.sidebar:
    #         st.markdown(
    #             f"<a href = #{mistnost} style='text-decoration: none; font-size: 1.5em;'><span style='transition: color 0.3s;'>{mistnost}</span></a>",
    #             unsafe_allow_html=True,
    #         )

    #     vars_rozvrh = {
    #         "semestr": "%",
    #         "mistnost": mistnost,
    #         "vsechnyCasyKonani": "true",
    #         "budova": "CP",
    #         "jenRozvrhoveAkce": "false",
    #         "vsechnyAkce": "true",
    #         "jenBudouciAkce": "false",
    #         "rok": "2023",
    #         "lang": "cs",
    #         "outputFormatEncoding": "utf-8",
    #         "outputFormat": "CSV",
    #     }
        
    #     response = httpx.get(url_rozvrh, params=vars_rozvrh)
    #     df_rozvrh = pd.read_csv(StringIO(response.text), sep=";")
    
    return templates.TemplateResponse("index.html", {"request": request, "df_mistnosti": df_mistnosti})