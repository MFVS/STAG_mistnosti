import streamlit as st
import httpx
from io import StringIO
import pandas as pd


st.set_page_config(layout="wide", page_title="STAG Místnosti", page_icon="🏫")
st.title("STAG Místnosti")

st.header("Seznam místností")

url_mistnosti_info = "https://ws.ujep.cz/ws/services/rest2/mistnost/getMistnostiInfo"
vars_mistnosti = {
    "zkrBudovy": "CP",
    "pracoviste": "%",
    "typ": "%",
    "cisloMistnosti": "%",
    "outputFormatEncoding": "utf-8",
    "outputFormat": "CSV",
}


response = httpx.get(url_mistnosti_info, params=vars_mistnosti)

df_mistnosti = pd.read_csv(StringIO(response.text), sep=";")
# cisloMistnosti starts with 6. or 7.

df_mistnosti = df_mistnosti[df_mistnosti["cisloMistnosti"].str.startswith(("6.", "7."))]

st.write(df_mistnosti)

st.header("Rozvrhy místností")

# df_mistnosti["typ"] is Učebna or Laboratoř
df_mistnosti = df_mistnosti[df_mistnosti["typ"].isin(["Učebna", "Laboratoř"])]

url_rozvrh = "https://ws.ujep.cz/ws/services/rest2/rozvrhy/getRozvrhByMistnost"
# semestr=%25&vsechnyCasyKonani=true&budova=CP&jenRozvrhoveAkce=false&vsechnyAkce=true&jenBudouciAkce=false&lang=cs&mistnost=6.13&outputFormat=CSV&rok=2023

for mistnost in df_mistnosti["cisloMistnosti"]:
    st.subheader(mistnost, anchor=mistnost)
    with st.sidebar:
        st.markdown(
            f"<a href = #{mistnost} style='text-decoration: none; font-size: 1.5em;'><span style='transition: color 0.3s;'>{mistnost}</span></a>",
            unsafe_allow_html=True,
        )

    vars_rozvrh = {
        "semestr": "%",
        "mistnost": mistnost,
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
    
    response = httpx.get(url_rozvrh, params=vars_rozvrh)
    df_rozvrh = pd.read_csv(StringIO(response.text), sep=";")
    
    st.write(df_rozvrh)