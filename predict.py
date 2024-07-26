import pickle
import pandas as pd


class ASDPredictor:
    def __init__(self, model_path, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, Age_Years, Ethnicity, Jaundice,
                 Family_mem_with_ASD, country_of_res, used_app_before, Q10_Result, Who_completed_the_test, Gender_en):
        # Carregar o modelo treinado
        with open(model_path, 'rb') as file:
            self.best_model = pickle.load(file)

        # Inicializar as propriedades
        self.A1 = A1
        self.A2 = A2
        self.A3 = A3
        self.A4 = A4
        self.A5 = A5
        self.A6 = A6
        self.A7 = A7
        self.A8 = A8
        self.A9 = A9
        self.A10 = A10
        self.Age_Years = Age_Years
        self.Ethnicity = Ethnicity
        self.Jaundice = Jaundice
        self.Family_mem_with_ASD = Family_mem_with_ASD
        self.country_of_res = country_of_res
        self.used_app_before = used_app_before
        self.Q10_Result = Q10_Result
        self.Who_completed_the_test = Who_completed_the_test
        self.Gender_en = Gender_en

    def predict_asd(self):
        """
        Retorna: 0 ou 1, indicando se a previsão é negativa ou positiva para ASD.
        """
        # Criar o dicionário de entrada
        input_data = {
            'A1': self.A1,
            'A2': self.A2,
            'A3': self.A3,
            'A4': self.A4,
            'A5': self.A5,
            'A6': self.A6,
            'A7': self.A7,
            'A8': self.A8,
            'A9': self.A9,
            'A10': self.A10,
            'Age_Years': self.Age_Years,
            'Ethnicity': self.Ethnicity,
            'Jaundice': self.Jaundice,
            'Family_mem_with_ASD': self.Family_mem_with_ASD,
            'contry_of_res': self.country_of_res,
            'used_app_before': self.used_app_before,
            'Q10-Result': self.Q10_Result,
            'Who completed the test': self.Who_completed_the_test,
            'Gender_en': self.Gender_en
        }

        # Converter o dicionário de entrada em um DataFrame
        input_df = pd.DataFrame([input_data])

        # Certifique-se de que as colunas estejam na ordem correta e correspondam às colunas usadas no treinamento
        input_df = input_df[self.best_model.feature_names_in_]

        # Fazer a previsão
        prediction = self.best_model.predict(input_df)

        return prediction[0]

    def print_prediction(self):
        resultado = self.predict_asd()
        print(f'A previsão é: {resultado}')


# Exemplo de uso da classe ASDPredictor
predictor = ASDPredictor(
    model_path='best_model.pkl',
    A1=1,
    A2=1,
    A3=0,
    A4=0,
    A5=1,
    A6=1,
    A7=0,
    A8=1,
    A9=0,
    A10=0,
    Age_Years=6.0,
    Ethnicity=0.047945,
    Jaundice=0,
    Family_mem_with_ASD=0,
    country_of_res=0.068493,
    used_app_before=0,
    Q10_Result=5,
    Who_completed_the_test=0.732877,
    Gender_en=1.0
)

# Realizar a previsão
predictor.print_prediction()
print(predictor.country_of_res)