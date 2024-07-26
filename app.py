import streamlit as st
from models_pt import country_of_res as country_pt, who_completed_the_test as who_test_pt, ethnicity as ethnicity_pt
from models_en import country_of_res as country_en, who_completed_the_test as who_test_en, ethnicity as ethnicity_en


# Definir uma função para alternar entre português e inglês
def get_dictionaries(language):
    if language == 'pt':
        return country_pt, who_test_pt, ethnicity_pt
    elif language == 'en':
        return country_en, who_test_en, ethnicity_en


# Botão de alternância de idioma
language = st.radio("Escolha o idioma / Choose the language", ('pt', 'en'),horizontal=True)

# Definir a interface do usuário
st.title("Previsão de ASD" if language == "pt" else "ASD Prediction")

# Obter os dicionários corretos com base no idioma selecionado
country_dict, who_test_dict, ethnicity_dict = get_dictionaries(language)

# Formulário para entrada de dados
with st.form("prediction_form"):
    country = st.selectbox("País de residência" if language == "pt" else "Country of residence",
                           list(country_dict.keys()))
    who_completed = st.selectbox("Quem completou o teste" if language == "pt" else "Who completed the test",
                                 list(who_test_dict.keys()))
    ethnicity = st.selectbox("Etnia" if language == "pt" else "Ethnicity", list(ethnicity_dict.keys()))
    age_years = st.number_input("Idade (em anos)" if language == "pt" else "Age (in years)", min_value=0, max_value=100)
    jaundice = st.radio("Icterícia" if language == "pt" else "Jaundice",
                        ("Sim" if language == "pt" else "Yes", "Não" if language == "pt" else "No"))
    family_mem_with_asd = st.radio("Membro da família com ASD" if language == "pt" else "Family member with ASD",
                                   ("Sim" if language == "pt" else "Yes", "Não" if language == "pt" else "No"))
    used_app_before = st.radio("Usou o aplicativo antes" if language == "pt" else "Used the app before",
                               ("Sim" if language == "pt" else "Yes", "Não" if language == "pt" else "No"))
    gender = st.radio("Gênero" if language == "pt" else "Gender",
                      ("Masculino" if language == "pt" else "Male", "Feminino" if language == "pt" else "Female"))

    # Botão de submissão
    submitted = st.form_submit_button("Enviar" if language == "pt" else "Submit")

if submitted:
    st.write(f"{gender}")
