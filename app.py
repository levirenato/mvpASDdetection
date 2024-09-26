import streamlit as st
from models_pt import (
    country_of_res as country_pt,
    who_completed_the_test as who_test_pt,
    ethnicity as ethnicity_pt,
    questions as question_pt,
    options as options_pt,
)
from models_en import (
    country_of_res as country_en,
    who_completed_the_test as who_test_en,
    ethnicity as ethnicity_en,
    questions as question_en,
    options as options_en,
)
from predict import ASDPredictor
import pandas as pd
import plotly.express as px

# definir tema
ms = st.session_state
if "themes" not in ms:
    ms.themes = {
        "current_theme": "light",
        "refreshed": True,
        "light": {
            "theme.base": "light",
            "theme.backgroundColor": "white",
            "theme.primaryColor": "#c98bdb",
            "button_face": "🌜",
        },
        "dark": {
            "theme.base": "dark",
            "theme.backgroundColor": "#31363F",
            "theme.primaryColor": "#5591f5",
            "button_face": "🌞",
        },
    }


def ChangeTheme():
    previous_theme = ms.themes["current_theme"]
    tdict = (
        ms.themes["light"]
        if ms.themes["current_theme"] == "light"
        else ms.themes["dark"]
    )
    for vkey, vval in tdict.items():
        if vkey.startswith("theme"):
            st._config.set_option(vkey, vval)

    ms.themes["refreshed"] = False
    if previous_theme == "dark":
        ms.themes["current_theme"] = "light"
    elif previous_theme == "light":
        ms.themes["current_theme"] = "dark"


btn_face = (
    ms.themes["light"]["button_face"]
    if ms.themes["current_theme"] == "light"
    else ms.themes["dark"]["button_face"]
)
st.button(btn_face, on_click=ChangeTheme)

if not ms.themes["refreshed"]:
    ms.themes["refreshed"] = True
    st.rerun()


# Definir uma função para alternar entre português e inglês
def get_dictionaries(language):
    if language == "pt":
        return country_pt, who_test_pt, ethnicity_pt, question_pt
    elif language == "en":
        return country_en, who_test_en, ethnicity_en, question_en


# Botão de alternância de idioma
st.write("#### Escolha o idioma / Choose the language")
language = st.radio(
    label="### Escolha o idioma / Choose the language",
    options=("pt", "en"),
    horizontal=True,
    label_visibility="hidden",
)

# Definir a interface do usuário
st.title("Previsão de TEA" if language == "pt" else "ASD Prediction")

# Obter os dicionários corretos com base no idioma selecionado
country_dict, who_test_dict, ethnicity_dict, question_dict = get_dictionaries(language)

# Inicializar o estado do Streamlit para armazenar os resultados
if "results_pt" not in st.session_state:
    st.session_state["results_pt"] = []
if "results_en" not in st.session_state:
    st.session_state["results_en"] = []

# Mapear traduções das colunas
columns_mapping = {
    "pt": {
        "Age_Years": "Idade (em anos)",
        "Ethnicity": "Etnia",
        "Jaundice": "Icterícia",
        "Family_mem_with_ASD": "Membro da família com TEA",
        "country_of_res": "País de residência",
        "used_app_before": "Usou o aplicativo antes",
        "Who_completed_the_test": "Quem completou o teste",
        "Gender_en": "Gênero",
        "A1": "A1",
        "A2": "A2",
        "A3": "A3",
        "A4": "A4",
        "A5": "A5",
        "A6": "A6",
        "A7": "A7",
        "A8": "A8",
        "A9": "A9",
        "A10": "A10",
        "Resultado": "Resultado",
    },
    "en": {
        "Age_Years": "Age (in years)",
        "Ethnicity": "Ethnicity",
        "Jaundice": "Jaundice",
        "Family_mem_with_ASD": "Family member with ASD",
        "country_of_res": "Country of residence",
        "used_app_before": "Used the app before",
        "Who_completed_the_test": "Who completed the test",
        "Gender_en": "Gender",
        "A1": "A1",
        "A2": "A2",
        "A3": "A3",
        "A4": "A4",
        "A5": "A5",
        "A6": "A6",
        "A7": "A7",
        "A8": "A8",
        "A9": "A9",
        "A10": "A10",
        "Resultado": "Result",
    },
}

# Formulário para entrada de dados
with st.form("prediction_form"):
    st.subheader("Dados do paciente" if language == "pt" else "Patient information")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.radio(
            "Gênero" if language == "pt" else "Gender",
            options=[0, 1],
            format_func=lambda x: (
                "Feminino"
                if x == 0 and language == "pt"
                else (
                    "Female"
                    if x == 0
                    else "Masculino" if x == 1 and language == "pt" else "Male"
                )
            ),
            horizontal=True,
            key="gender",
        )

        age_years = st.number_input(
            "Idade (em anos)" if language == "pt" else "Age (in years)",
            min_value=0,
            max_value=100,
            key="age_years",
        )

        country = st.selectbox(
            "País de residência" if language == "pt" else "Country of residence",
            list(country_dict.keys()),
            key="country_of_residence",
        )

        who_completed = st.selectbox(
            "Quem completou o teste" if language == "pt" else "Who completed the test",
            list(who_test_dict.keys()),
            key="who_completed",
        )
    with col2:
        ethnicity = st.selectbox(
            "Etnia" if language == "pt" else "Ethnicity",
            list(ethnicity_dict.keys()),
            key="ethnicity",
        )

        jaundice = st.radio(
            "Icterícia" if language == "pt" else "Jaundice",
            options=[1, 0],
            format_func=lambda x: (
                "Sim"
                if x == 1 and language == "pt"
                else "Yes" if x == 1 else "Não" if x == 0 and language == "pt" else "No"
            ),
            horizontal=True,
            key="jaundice",
        )

        used_app_before = st.radio(
            "Usou o aplicativo antes" if language == "pt" else "Used the app before",
            options=[1, 0],
            format_func=lambda x: (
                "Sim"
                if x == 1 and language == "pt"
                else "Yes" if x == 1 else "Não" if x == 0 and language == "pt" else "No"
            ),
            horizontal=True,
            key="used_app_before",
        )

        family_mem_with_asd = st.radio(
            (
                "Membro da família com TEA"
                if language == "pt"
                else "Family member with ASD"
            ),
            options=[1, 0],
            format_func=lambda x: (
                "Sim"
                if x == 1 and language == "pt"
                else "Yes" if x == 1 else "Não" if x == 0 and language == "pt" else "No"
            ),
            horizontal=True,
            key="family_mem_with_asd",
        )

    st.html("<br/>")
    st.subheader("Perguntas" if language == "pt" else "Questions")

    # Questions
    def map_response(question, response):
        if question in ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]:
            return (
                1
                if response
                in ["Às vezes", "Raramente", "Nunca", "Sometimes", "Rarely", "Never"]
                else 0
            )
        elif question == "A10":
            return (
                1
                if response
                in [
                    "Sempre",
                    "Normalmente",
                    "Às vezes",
                    "Always",
                    "Usually",
                    "Sometimes",
                ]
                else 0
            )

    if language == "pt":
        options = options_pt
    else:
        options = options_en

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(
        [i for i in question_dict.keys()]
    )

    with tab1:
        A1 = map_response(
            "A1",
            st.radio(
                label=f"#### {question_dict.get('A1')}",
                options=options,
                horizontal=True,
                key="A1",
            ),
        )

    with tab2:
        A2 = map_response(
            "A2",
            st.radio(
                label=f"#### {question_dict.get('A2')}",
                options=options,
                horizontal=True,
                key="A2",
            ),
        )

    with tab3:
        A3 = map_response(
            "A3",
            st.radio(
                label=f"#### {question_dict.get('A3')}",
                options=options,
                horizontal=True,
                key="A3",
            ),
        )

    with tab4:
        A4 = map_response(
            "A4",
            st.radio(
                label=f"#### {question_dict.get('A4')}",
                options=options,
                horizontal=True,
                key="A4",
            ),
        )

    with tab5:
        A5 = map_response(
            "A5",
            st.radio(
                label=f"#### {question_dict.get('A5')}",
                options=options,
                horizontal=True,
                key="A5",
            ),
        )

    with tab6:
        A6 = map_response(
            "A6",
            st.radio(
                label=f"#### {question_dict.get('A6')}",
                options=options,
                horizontal=True,
                key="A6",
            ),
        )

    with tab7:
        A7 = map_response(
            "A7",
            st.radio(
                label=f"#### {question_dict.get('A7')}",
                options=options,
                horizontal=True,
                key="A7",
            ),
        )

    with tab8:
        A8 = map_response(
            "A8",
            st.radio(
                label=f"#### {question_dict.get('A8')}",
                options=options,
                horizontal=True,
                key="A8",
            ),
        )

    with tab9:
        A9 = map_response(
            "A9",
            st.radio(
                label=f"#### {question_dict.get('A9')}",
                options=options,
                horizontal=True,
                key="A9",
            ),
        )

    with tab10:
        A10 = map_response(
            "A10",
            st.radio(
                label=f"#### {question_dict.get('A10')}",
                options=options,
                horizontal=True,
                key="A10",
            ),
        )

    st.divider()
    # Botão de submissão
    submitted = st.form_submit_button("Enviar" if language == "pt" else "Submit")

if submitted:
    predict = ASDPredictor(
        Age_Years=age_years,
        Ethnicity=ethnicity_dict.get(ethnicity),
        Jaundice=jaundice,
        Family_mem_with_ASD=family_mem_with_asd,
        country_of_res=country_dict.get(country),
        used_app_before=used_app_before,
        Who_completed_the_test=who_test_dict.get(who_completed),
        Gender_en=gender,
        A1=A1,
        A2=A2,
        A3=A3,
        A4=A4,
        A5=A5,
        A6=A6,
        A7=A7,
        A8=A8,
        A9=A9,
        A10=A10,
    )
    result = predict.print_prediction()
    result_text = "Positivo" if result == 1 else "Negativo"

    # Dados para DataFrame
    data = {
        "Age_Years": age_years,
        "Ethnicity": ethnicity,
        "Jaundice": (
            "Sim"
            if jaundice == 1 and language == "pt"
            else (
                "Yes"
                if jaundice == 1
                else "Não" if jaundice == 0 and language == "pt" else "No"
            )
        ),
        "Family_mem_with_ASD": (
            "Sim"
            if family_mem_with_asd == 1 and language == "pt"
            else (
                "Yes"
                if family_mem_with_asd == 1
                else "Não" if family_mem_with_asd == 0 and language == "pt" else "No"
            )
        ),
        "country_of_res": country,
        "used_app_before": (
            "Sim"
            if used_app_before == 1 and language == "pt"
            else (
                "Yes"
                if used_app_before == 1
                else "Não" if used_app_before == 0 and language == "pt" else "No"
            )
        ),
        "Who_completed_the_test": who_completed,
        "Gender_en": (
            "Feminino"
            if gender == 0 and language == "pt"
            else (
                "Female"
                if gender == 0
                else "Masculino" if gender == 1 and language == "pt" else "Male"
            )
        ),
        "A1": (
            "Sim"
            if A1 == 1 and language == "pt"
            else "Yes" if A1 == 1 else "Não" if A1 == 0 and language == "pt" else "No"
        ),
        "A2": (
            "Sim"
            if A2 == 1 and language == "pt"
            else "Yes" if A2 == 1 else "Não" if A2 == 0 and language == "pt" else "No"
        ),
        "A3": (
            "Sim"
            if A3 == 1 and language == "pt"
            else "Yes" if A3 == 1 else "Não" if A3 == 0 and language == "pt" else "No"
        ),
        "A4": (
            "Sim"
            if A4 == 1 and language == "pt"
            else "Yes" if A4 == 1 else "Não" if A4 == 0 and language == "pt" else "No"
        ),
        "A5": (
            "Sim"
            if A5 == 1 and language == "pt"
            else "Yes" if A5 == 1 else "Não" if A5 == 0 and language == "pt" else "No"
        ),
        "A6": (
            "Sim"
            if A6 == 1 and language == "pt"
            else "Yes" if A6 == 1 else "Não" if A6 == 0 and language == "pt" else "No"
        ),
        "A7": (
            "Sim"
            if A7 == 1 and language == "pt"
            else "Yes" if A7 == 1 else "Não" if A7 == 0 and language == "pt" else "No"
        ),
        "A8": (
            "Sim"
            if A8 == 1 and language == "pt"
            else "Yes" if A8 == 1 else "Não" if A8 == 0 and language == "pt" else "No"
        ),
        "A9": (
            "Sim"
            if A9 == 1 and language == "pt"
            else "Yes" if A9 == 1 else "Não" if A9 == 0 and language == "pt" else "No"
        ),
        "A10": (
            "Sim"
            if A10 == 1 and language == "pt"
            else "Yes" if A10 == 1 else "Não" if A10 == 0 and language == "pt" else "No"
        ),
        "Resultado": result_text,
    }

    # Atualiza os DataFrames
    st.session_state["results_pt"].append(data)
    st.session_state["results_en"].append(data)

    st.subheader(
        f"{'Hipótese Diagnóstica' if language == 'pt' else 'Diagnostic hypothesis'}: {result_text}"
    )

    # Exibir o DataFrame
    df_t = pd.DataFrame(
        st.session_state["results_pt"]
        if language == "pt"
        else st.session_state["results_en"]
    )
    df_t.columns = [columns_mapping[language][col] for col in df_t.columns]
    st.dataframe(df_t)

    # Gráficos
    st.subheader("Visualizações")

    # Gráfico de Idades Colorido
    fig_age = px.histogram(
        df_t,
        x="Idade (em anos)" if language == "pt" else "Age (in years)",
        nbins=10,
        title="Distribuição das Idades",
        color=(
            "Resultado" if language == "pt" else "Result"
        ),  # Adiciona cor com base na coluna de resultado
        color_discrete_map={
            "Positivo": "red",
            "Negativo": "blue",
        },  # Mapeia cores específicas para os resultados
    )
    fig_age.update_layout(
        xaxis_title="Idade (em anos)" if language == "pt" else "Age (in years)",
        yaxis_title="Número de Pacientes",
        legend_title="Resultado" if language == "pt" else "Result",
    )

    st.plotly_chart(fig_age)

    # Gráfico de Gênero
    fig_gender = px.pie(
        df_t,
        names="Resultado" if language == "pt" else "Result",
        title="Distribuição por Gênero",
    )
    st.plotly_chart(fig_gender)

    # Gráfico de Resultados
    fig_result = px.pie(
        df_t,
        names="Resultado" if language == "pt" else "Result",
        title="Distribuição dos Resultados",
    )
    st.plotly_chart(fig_result)

    # Gráfico de Idade x Resultado como Dispersão
    fig_age_result = px.scatter(
        df_t,
        x="Idade (em anos)" if language == "pt" else "Age (in years)",
        y="Resultado" if language == "pt" else "Result",
        color=(
            "Resultado" if language == "pt" else "Result"
        ),  # Adiciona cores baseadas na coluna Resultado
        title="Distribuição da Idade por Resultado",
        color_discrete_map={
            "Positivo": "red",
            "Negativo": "blue",
        },  # Mapeia cores específicas para os resultados
    )

    # Ajustes de Layout
    fig_age_result.update_layout(
        xaxis_title="Idade (em anos)" if language == "pt" else "Age (in years)",
        yaxis_title="Resultado" if language == "pt" else "Result",
        legend_title="Resultado" if language == "pt" else "Result",
    )

    st.plotly_chart(fig_age_result)

    # Gráfico de Etnia
    fig_ethnicity = px.pie(
        df_t,
        names="Etnia" if language == "pt" else "Ethnicity",
        title="Distribuição por Etnia",
    )
    st.plotly_chart(fig_ethnicity)
