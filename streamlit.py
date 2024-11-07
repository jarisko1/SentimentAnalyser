import streamlit as st
import pandas as pd
import importlib

import openai_lib as oai

importlib.reload(oai)


# Define Streamlit UI
st.set_page_config(layout = 'wide') #, initial_sidebar_state = 'collapsed')
column_middle, padding, column_right = st.columns((23,1,3))

# Initialize OpenAI Client
client = st.session_state.get("client")
if client is None:
    client = oai.get_client()
    st.session_state.client = client

### Define sidebar

st.sidebar.header("Settings")

### Define input
text_input = st.text_area(label="Enter text", value="""[16:45, 03/11/2024] Peter: Plus minus nieco za 15k bez dph
[16:45, 03/11/2024] Peter: Este bedna chyba😂
[16:45, 03/11/2024] Peter: Ale neviem ci teku predavaju
[16:46, 03/11/2024] Peter: Rentovanie niecoho podobneho na full mesiac vychadza asi 700-900 Usd
[17:34, 03/11/2024] Pavol: Toto je zbytocne Peter
[17:34, 03/11/2024] Pavol: 2 grafiky mozno ma zmysel mat u seba
[17:35, 03/11/2024] Pavol: Ale viac asi ne
[17:41, 03/11/2024] Peter: No oki jak povies
[17:41, 03/11/2024] Peter: Ale to potom ked pozeram lama requirements rpzbehame asi tak ten najmensi model
[17:42, 03/11/2024] Peter: Zajtra mozme Pavol pokecat
[21:51, 03/11/2024] Denis: ja by som zas povedal ze ked mame 30k na server tak spravme future proof ready a najebme tam co to da😂
[09:48, 04/11/2024] Peter: Caute
[09:48, 04/11/2024] Peter: Na stredu dam nas meeting skusim aj Matildu zlanarit nan
[09:49, 04/11/2024] Peter: Jeden topic co zatial nemam sajnu neviete okrem Denisa nejaky tool nacom by sme vedeli nasimulovat mock/demo pre ten sentiment check?
[09:49, 04/11/2024] Peter: Nejaky video editor alebo nieco co aluzi na vytvaranie takychto demo videi
[09:51, 04/11/2024] Pavol: Caves. Ja v stredu nemozem, ibaze by sme si dali meeting v ofise""", )
file_input = st.file_uploader(label="Enter file", accept_multiple_files=True)

button_input = st.button(label="Analyse sentiment")


# Process input
if button_input and (text_input or file_input):

    text_to_analyze = ""

    if text_input:
        text_to_analyze += text_input
    
    if file_input:
        for file in file_input:

            if file.type == "text/plain":
                text_file = file.read().decode("utf-8")

            if file.type == "text/csv":
                csv_df = pd.read_csv(file, header=None)
                
            if file.type == "image/jpeg":
                # TODO: implement OCR
                image_file = file.read()

            if file.type == "application/pdf":
                # TODO: implement
                pass



    st.write(oai.analyze_sentiment(client, text_to_analyze))
    # st.markdown(oai.analyze_sentiment(client, text_to_analyze), unsafe_allow_html=True)