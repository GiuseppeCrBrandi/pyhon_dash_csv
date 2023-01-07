import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import numpy as np




def UploadTableCsv():
    columns = ["Matrícula", "Mês", "Valor", "Status"]

    df = pd.read_csv('inad.csv', names=columns, encoding="utf-8", sep = ',')

    
    # Remove eventuais ; das últimas linhas do arquivo CSV
    df[df.columns[-1]] = df[df.columns[-1]].str.strip(";")

    # Obtém o número de linhas e colunas no DataFrame
    n_rows, n_cols = df.shape

    # Garante que os índices das linhas e colunas estão dentro do intervalo do DataFrame
    rows = [i for i in range(n_rows)]
    cols = [i for i in range(n_cols)]

    # Use the modified indices to select the rows and columns
    df = df.iloc[rows,cols].reset_index(drop=True)

    # Renomeia as colunas
    df.columns=['Matrícula','Mês','Valor','Status']

    

 
    
    # Transforma o DataFrame em um dicionário
    data_dict = df.to_dict()

    # Extrai os dados do dicionário e cria uma lista de listas
    table = []
    for i in range(len(df)):
        row = []
        for key, value in data_dict.items():
            row.append(value[i])
        table.append(row)

    # Imprime a tabela resultante
    transformed_data = []
    for row in table:
        try:
            # Separar mês e ano e incluir apenas o mês na lista
            transformed_row = [row[0], row[1].split("-")[1], row[2], row[3]]
        except IndexError:
            transformed_row = row
        transformed_data.append(transformed_row)

    tableInadi = calculate_default_rates(table)
    print(tableInadi)
    columns1 = ['Mês', 'Taxa de Inadimplência']
    af = pd.DataFrame(tableInadi, columns=columns1)


# gera as rows da tabela
    table_rows = generate_table(tableInadi, columns1)



    app = dash.Dash()

# cria o layout do app
    app.layout = html.Div(
    children=[
    
        html.Table(
            style={'margin': 'auto', 'width': '50%'},
            
            children=[
                html.Tr(
                    children=[
                        # por os headers
                        html.Th(col) for col in df.columns
                    ],  style={"border": "2px solid black"}
                )
            ] + [
                # adicionar as fileiras da tabela
                html.Tr(
                    children=[
                        html.Td(df.iloc[i][col], style={"border": "1px solid black"}) for col in df.columns
                    ],  style={
                "border": "1px solid black",
                "background-color": "#f5f5f5" if i % 2 == 0 else "white"
            }
                ) for i in range(len(df))
            ]
        ),
        # adicionar o grafico de barras da tabela 
        dcc.Graph(
            figure=px.bar(df, x="Mês", y="Valor", color="Status", color_discrete_map={"aberto": "red", "pago": "green"})
        ),
        html.Table(
            style={'margin': 'auto', 'width': '50%', 'border': '2px solid black'},
            # Add the table rows
            children=table_rows
        ),
        # adicionar o grafico de barras da inadimplencia
        dcc.Graph(
            figure=px.bar(af, x="Mês", y="Taxa de Inadimplência")
        )

        
    ]
)

    app.run_server(debug=True)



    
    return table

    ###print(transformed_data)
    #print(table)

def generate_table(data, columns):
    return [
        html.Tr([html.Th(col) for col in columns],
        style={"border": "2px solid black"})
    ] + [
        html.Tr([
            html.Td(data[i][col]) for col in range(len(columns))
        ],  style={
                "border": "1px solid black",
                "background-color": "#f5f5f5" if i % 2 == 0 else "white"
            }
        ) for i in range(len(data))
    ]


# calcular a inadimplencia 

def calculate_default_rates(table):
    
    default_rates = {}
    
   # Iterar sobre as linhas da tabela, começando da segunda linha (para pular a linha de cabeçalho)
    for row in table[1:]:
        # Extrair os dados relevantes da linha
        mes = row[1]
        valor = float(row[2])  # Converter o valor para float
        status = row[3]

        #colocar os meses que nao estao no dicionario ainda
        if mes not in default_rates:
            default_rates[mes] = 0
          ##  print(default_rates)

        # se o status for aberto colocar o valor no dicionario e somar 
        if status == "aberto":
            default_rates[mes] += valor
           
        
    # Calcular o valor total para cada mês
    totals = {}
    for row in table[1:]:
        mes = row[1]
        valor = float(row[2]) 

        if mes not in totals:
            totals[mes] = 0
        totals[mes] += valor
       

    # Inicializar dicionário para armazenar as taxas acumuladas de inadimplência
    cumulative_default = {}

   # Inicializar variáveis para acompanhar a taxa acumulada de inadimplência e o valor total acumulado
    cum_default_rate = 0
    cum_total_value = 0

    # Iterar sobre os meses no dicionário de inadimplência
    for mes in default_rates:
          # Adicionar a taxa de inadimplência e o valor total para o mês atual aos valores acumulados
        cum_default_rate += default_rates[mes]
        cum_total_value += totals[mes]

       # Calcular a taxa acumulada de inadimplência para o mês atual
        cum_default = cum_default_rate / cum_total_value

       # Adicionar a taxa acumulada de inadimplência ao dicionário inadimplência_acumulada
        cumulative_default[mes] = cum_default
  
    tabelaInad = []

    for key, value in cumulative_default.items():
        tabelaInad.append([key, value])
    

    return tabelaInad



def PlotarTabela():
    print()


def main():

    
    print("Hello, world!")
    astable= UploadTableCsv()
    dados = calculate_default_rates(astable)
    
    

if __name__ == "__main__":
    main()
