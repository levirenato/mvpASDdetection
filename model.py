import pickle
import pandas as pd

# Carregar o modelo treinado
with open('best_model.pkl', 'rb') as file:
    best_model = pickle.load(file)

# Definir a função de previsão
def predict_asd(input_data):
    """
    input_data: dicionário contendo os parâmetros de entrada, 
                onde as chaves são os nomes das colunas e os valores são os valores das colunas.
    
    Retorna: 0 ou 1, indicando se a previsão é negativa ou positiva para ASD.
    """
    # Converter o dicionário de entrada em um DataFrame
    input_df = pd.DataFrame([input_data])

    # Certifique-se de que as colunas estejam na ordem correta e correspondam às colunas usadas no treinamento
    input_df = input_df[best_model.feature_names_in_]

    # Fazer a previsão
    prediction = best_model.predict(input_df)

    return prediction[0]

# Exemplo de uso da função de previsão
new_data = {
    'A1': 1,
    'A2': 1,
    'A3': 0,
    'A4': 0,
    'A5': 1,
    'A6': 1,
    'A7': 0,
    'A8': 1,
    'A9': 0,
    'A10': 0,
    'Age_Years': 6.0,
    'Ethnicity': 0.047945,
    'Jaundice': 0,
    'Family_mem_with_ASD': 0,
    'contry_of_res': 0.068493,
    'used_app_before': 0,
    'Q10-Result': 5,
    'Who completed the test': 0.732877,
    'Gender_en': 1.0
}

# Realizar a previsão
resultado = predict_asd(new_data)
print(f'A previsão é: {resultado}')
