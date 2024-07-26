import streamlit as st
from models_pt import country_of_res as country_pt, who_completed_the_test as who_test_pt, ethnicity as ethnicity_pt, \
    questions as question_pt, options as options_pt
from models_en import country_of_res as country_en, who_completed_the_test as who_test_en, ethnicity as ethnicity_en, \
    questions as question_en, options as options_en


# Definir uma função para alternar entre português e inglês
def get_dictionaries(language):
    if language == 'pt':
        return country_pt, who_test_pt, ethnicity_pt, question_pt
    elif language == 'en':
        return country_en, who_test_en, ethnicity_en, question_en


# Botão de alternância de idioma
st.write("#### Escolha o idioma / Choose the language")
language = st.radio(label="### Escolha o idioma / Choose the language",options=('pt', 'en'), horizontal=True, label_visibility="hidden")

# Definir a interface do usuário
st.title("Previsão de TEA" if language == "pt" else "ASD Prediction")

# Obter os dicionários corretos com base no idioma selecionado
country_dict, who_test_dict, ethnicity_dict, question_dict = get_dictionaries(language)

# Formulário para entrada de dados
with st.form("prediction_form"):
    st.subheader("Dados do paciente" if language == "pt" else "Patient information")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.radio(
            "Gênero" if language == "pt" else "Gender",
            options=[0, 1],
            format_func=lambda
                x: "Feminino" if x == 0 and language == "pt" else "Female"
            if x == 0 else "Masculino" if x == 1 and language == "pt" else "Male",
            horizontal=True,
            key="gender"
        )

        age_years = st.number_input("Idade (em anos)" if language == "pt" else "Age (in years)", min_value=0,
                                    max_value=100, key="age_years")

        country = st.selectbox("País de residência" if language == "pt" else "Country of residence",
                               list(country_dict.keys()), key="country_of_residence")

        who_completed = st.selectbox("Quem completou o teste" if language == "pt" else "Who completed the test",
                                     list(who_test_dict.keys()), key="who_completed")
    with col2:
        ethnicity = st.selectbox("Etnia" if language == "pt" else "Ethnicity", list(ethnicity_dict.keys()),
                                 key="ethnicity")

        jaundice = st.radio(
            "Icterícia" if language == "pt" else "Jaundice",
            options=[1, 0],
            format_func=lambda
                x: "Sim" if x == 1 and language == "pt" else "Yes" if x == 1 else "Não" if x == 0 and language == "pt" else "No",
            horizontal=True,
            key="jaundice"
        )

        used_app_before = st.radio(
            "Usou o aplicativo antes" if language == "pt" else "Used the app before",
            options=[1, 0],
            format_func=lambda
                x: "Sim" if x == 1 and language == "pt" else "Yes" if x == 1 else "Não" if x == 0 and language == "pt" else "No",
            horizontal=True,
            key="used_app_before"
        )

        family_mem_with_asd = st.radio(
            "Membro da família com TEA" if language == "pt" else "Family member with ASD",
            options=[1, 0],
            format_func=lambda
                x: "Sim" if x == 1 and language == "pt" else "Yes" if x == 1 else "Não" if x == 0 and language == "pt" else "No",
            horizontal=True,
            key="family_mem_with_asd"
        )

    st.html("<br/>")
    st.subheader("Perguntas" if language == "pt" else "Questions")


    # Questions
    def map_response(question, response):
        if question in ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9"]:
            return 1 if response in ["Às vezes", "Raramente", "Nunca", "Sometimes", "Rarely", "Never"] else 0
        elif question == "A10":
            return 1 if response in ["Sempre", "Normalmente", "Às vezes", "Always", "Usually", "Sometimes"] else 0


    if language == "pt":
        options = options_pt
    else:
        options = options_en

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([i for i in question_dict.keys()])

    with tab1:
        A1 = map_response("A1", st.radio(label=f"#### {question_dict.get('A1')}", options=options, horizontal=True, key="A1",
                                         ))

    with tab2:
        A2 = map_response("A2", st.radio(label=f"#### {question_dict.get('A2')}", options=options, horizontal=True, key="A2",
                                         ))

    with tab3:
        A3 = map_response("A3", st.radio(label=f"#### {question_dict.get('A3')}", options=options, horizontal=True, key="A3",
                                         ))

    with tab4:
        A4 = map_response("A4", st.radio(label=f"#### {question_dict.get('A4')}", options=options, horizontal=True, key="A4",
                                         ))

    with tab5:
        A5 = map_response("A5", st.radio(label=f"#### {question_dict.get('A5')}", options=options, horizontal=True, key="A5",
                                         ))

    with tab6:
        A6 = map_response("A6", st.radio(label=f"#### {question_dict.get('A6')}", options=options, horizontal=True, key="A6",
                                         ))

    with tab7:
        A7 = map_response("A7", st.radio(label=F"#### {question_dict.get('A7')}", options=options, horizontal=True, key="A7",
                                         ))

    with tab8:
        A8 = map_response("A8", st.radio(label=f"#### {question_dict.get('A8')}", options=options, horizontal=True, key="A8",
                                         ))

    with tab9:
        A9 = map_response("A9", st.radio(label=f"#### {question_dict.get('A9')}", options=options, horizontal=True, key="A9",
                                         ))

    with tab10:
        A10 = map_response("A10", st.radio(label=f"#### {question_dict.get('A10')}", options=options, horizontal=True, key="A10",
                                           ))

    # Botão de submissão
    submitted = st.form_submit_button("Enviar" if language == "pt" else "Submit")

if submitted:
    st.write({
        "Age_Years": age_years,
        "Ethnicity": ethnicity_dict.get(ethnicity),
        "Jaundice": jaundice,
        "Family_mem_with_ASD": family_mem_with_asd,
        "country_of_res": country_dict.get(country),
        "used_app_before": used_app_before,
        "Who_completed_the_test": who_test_dict.get(who_completed),
        "Gender_en": gender,
        "A1": A1,
        "A2": A2,
        "A3": A3,
        "A4": A4,
        "A5": A5,
        "A6": A6,
        "A7": A7,
        "A8": A8,
        "A9": A9,
        "A10": A10,
    })
