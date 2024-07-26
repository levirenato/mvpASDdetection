import streamlit as st
from models_pt import country_of_res as country_pt, who_completed_the_test as who_test_pt, ethnicity as ethnicity_pt
from models_en import country_of_res as country_en, who_completed_the_test as who_test_en, ethnicity as ethnicity_en

# Definir uma função para alternar entre português e inglês
def get_dictionaries(language):
    if language == 'pt':
        return country_pt, who_test_pt, ethnicity_pt
    elif language == 'en':
        return country_en, who_test_en, ethnicity_en

# Definir a interface do usuário
st.title("Previsão de ASD")

# Botão de alternância de idioma
language = st.radio("Escolha o idioma / Choose the language", ('pt', 'en'))

# Obter os dicionários corretos com base no idioma selecionado
country_dict, who_test_dict, ethnicity_dict = get_dictionaries(language)

# Formulário para entrada de dados
with st.form("prediction_form"):
    country = st.selectbox("País de residência / Country of residence", list(country_dict.keys()))
    who_completed = st.selectbox("Quem completou o teste / Who completed the test", list(who_test_dict.keys()))
    ethnicity = st.selectbox("Etnia / Ethnicity", list(ethnicity_dict.keys()))
    age_years = st.number_input("Idade (em anos) / Age (in years)", min_value=0, max_value=100)
    jaundice = st.radio("Icterícia / Jaundice", ("Sim / Yes", "Não / No"))
    family_mem_with_asd = st.radio("Membro da família com ASD / Family member with ASD", ("Sim / Yes", "Não / No"))
    used_app_before = st.radio("Usou o aplicativo antes / Used the app before", ("Sim / Yes", "Não / No"))
    # feminino é 0 masculino é 1
    gender = st.radio("Gênero / Gender", ("Masculino / Male", "Feminino / Female"))

    # Botão de submissão
    submitted = st.form_submit_button("Enviar / Submit")

if submitted:
    st.write("Dados enviados com sucesso! / Data submitted successfully!")