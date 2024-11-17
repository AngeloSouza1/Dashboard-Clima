import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import requests
import pandas as pd
from datetime import datetime

# Configurar o aplicativo Dash e adicionar o Font Awesome para ícones
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
])

# Configuração da chave de API para Weatherbit
API_KEY = "78c361ac37d04b068f39cf7edddfd99b"

# Dicionário de tradução para condições climáticas e ícones
condicoes_traducao = {
    "Clear": ("Céu limpo", "fas fa-sun"),
    "Clear Sky": ("Céu limpo", "fas fa-sun"),
    "Partly cloudy": ("Parcialmente nublado", "fas fa-cloud-sun"),
    "Few clouds": ("Poucas nuvens", "fas fa-cloud"),
    "Scattered clouds": ("Nuvens dispersas", "fas fa-cloud"),
    "Broken clouds": ("Nuvens fragmentadas", "fas fa-cloud"),
    "Overcast clouds": ("Nublado", "fas fa-cloud"),
    "Light rain": ("Chuva leve", "fas fa-cloud-rain"),
    "Moderate rain": ("Chuva moderada", "fas fa-cloud-showers-heavy"),
    "Heavy rain": ("Chuva forte", "fas fa-cloud-showers-heavy"),
    "Snow": ("Neve", "far fa-snowflake"),
    "Mist": ("Névoa", "fas fa-smog"),
    "Fog": ("Nevoeiro", "fas fa-smog"),
    "Thunderstorm": ("Trovoada", "fas fa-bolt"),
    # Adicione mais condições conforme necessário
}

# Dicionários de tradução para dias da semana e meses em português
dias_semana = {
    "Monday": "Segunda-feira",
    "Tuesday": "Terça-feira",
    "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira",
    "Friday": "Sexta-feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

meses_ano = {
    "January": "Janeiro",
    "February": "Fevereiro",
    "March": "Março",
    "April": "Abril",
    "May": "Maio",
    "June": "Junho",
    "July": "Julho",
    "August": "Agosto",
    "September": "Setembro",
    "October": "Outubro",
    "November": "Novembro",
    "December": "Dezembro"
}

# Função para formatar a data em português
def formatar_data_em_portugues(data):
    dia_semana = dias_semana[data.strftime("%A")]
    dia = data.strftime("%d")
    mes = meses_ano[data.strftime("%B")]
    return f"{dia_semana}, {dia} de {mes}"

# Função para obter o nome do dia da semana em português
def obter_dia_semana(data):
    return dias_semana[data.strftime("%A")]

# Função para buscar dados de clima da API Weatherbit
def buscar_dados_clima(cidade, dias=5):
    url = f"https://api.weatherbit.io/v2.0/forecast/daily?city={cidade}&key={API_KEY}&days={dias}"
    resposta = requests.get(url)
    if resposta.status_code != 200:
        print("Erro ao acessar a API. Verifique a chave e o nome da cidade.")
        return pd.DataFrame()
    
    dados = resposta.json()
    lista_dados = []

    # Iterar sobre os dados de previsão para criar o DataFrame
    for dia in dados['data']:
        data = dia['datetime']
        temperatura_max = dia['max_temp']
        temperatura_min = dia['min_temp']
        condicao = dia['weather']['description']
        
        # Traduzir a condição climática e obter ícone usando o dicionário
        condicao_traduzida, icone_clima = condicoes_traducao.get(condicao, (condicao, "fas fa-cloud"))
        
        lista_dados.append({
            "Data": data,
            "Temperatura Máxima (°C)": temperatura_max,
            "Temperatura Mínima (°C)": temperatura_min,
            "Condição": condicao_traduzida,
            "Ícone": icone_clima,
            "Dia da Semana": obter_dia_semana(pd.to_datetime(data))
        })
    
    dados_clima = pd.DataFrame(lista_dados)
    # Formatando a data para o formato dia/mês/ano
    dados_clima['Data'] = pd.to_datetime(dados_clima['Data']).dt.strftime('%d/%m/%Y')
    return dados_clima

# CSS personalizado para adicionar efeitos aos cartões
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>Dashboard Climático</title>
    {%favicon%}
    {%css%}
    <style>
        /* Efeitos para os cartões */
        .card-style {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.15);
            border-radius: 15px;
        }
        .card-style:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

# Layout do aplicativo Dash com campo de entrada de cidade
app.layout = html.Div(style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center', 'minHeight': '100vh'}, children=[
    # Campo de entrada para cidade com botão de atualização
    html.Div([
        dcc.Input(
            id="cidade-input",
            type="text",
            value="São Paulo",
            placeholder="Digite a cidade",
            style={
                'width': '300px',
                'padding': '10px',
                'borderRadius': '25px',
                'border': '2px solid #007bff',
                'outline': 'none',
                'textAlign': 'center',
                'fontSize': '16px',
                'marginRight': '10px',
                'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.1)',
            }
        ),
        dbc.Button("Atualizar", id="update-button", color="primary", style={
            'padding': '10px 20px',
            'borderRadius': '25px',
            'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.2)',
            'fontSize': '16px'
        }),
    ], style={'marginBottom': '20px'}),
    
    # Hora e Data com Ícone de Meteorologia
    html.Div([
        html.Div([
            html.I(className="fas fa-cloud-sun", style={'marginRight': '10px', 'color': '#ffa500', 'fontSize': '2.5em'}),
            html.Span(datetime.now().strftime("%H:%M"), style={'fontSize': '2.5em'})
        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
        
        html.Div(formatar_data_em_portugues(datetime.now()), className="date", style={'fontSize': '1.5em', 'textAlign': 'center'}),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),

    # Seção de Condições Climáticas Atuais
    html.Div(id="current-weather", className="card-style", style={'padding': '30px', 'backgroundColor': 'rgba(255, 255, 255, 0.85)', 'textAlign': 'center', 'width': '400px'}),
    
    # Previsão da Semana
    html.Div(className="forecast-container", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'marginTop': '20px'}, children=[
        html.H3("Previsão para os Próximos Dias", style={'textAlign': 'center', 'color': '#004c8c', 'marginBottom': '20px', 'fontSize': '1.8em'}),
        html.Div(id="forecast-cards", style={'display': 'flex', 'justifyContent': 'center'})
    ])
])

# Callback para atualizar os dados de clima com base na cidade inserida
@app.callback(
    [Output("current-weather", "children"), Output("forecast-cards", "children")],
    [Input("update-button", "n_clicks")],
    [dash.dependencies.State("cidade-input", "value")]
)
def atualizar_dados(n_clicks, cidade):
    if not cidade:
        return html.Div("Cidade não encontrada"), []
    
    dados_clima = buscar_dados_clima(cidade)
    if dados_clima.empty:
        return html.Div("Dados indisponíveis para esta cidade"), []
    
    # Exibir clima atual
    clima_atual = html.Div([
        html.Div(f"Hoje em {cidade}", style={'fontSize': '1.8em', 'fontWeight': 'bold'}),
        html.I(className=dados_clima['Ícone'].iloc[0], style={'fontSize': '3em', 'color': '#ffa500', 'marginTop': '10px'}),
        html.Div(dados_clima['Condição'].iloc[0], style={'fontSize': '1.5em', 'marginTop': '10px'}),
        
        # Temperaturas Máxima e Mínima com formato melhorado
        html.Div(f"Máx: {dados_clima['Temperatura Máxima (°C)'].iloc[0]:.1f}°C", style={'fontSize': '1.4em', 'color': '#ff5733', 'marginTop': '10px'}),
        html.Div(f"Mín: {dados_clima['Temperatura Mínima (°C)'].iloc[0]:.1f}°C", style={'fontSize': '1.4em', 'color': '#1e90ff', 'marginTop': '5px'})
    ])
    
    # Exibir previsão dos próximos dias
    previsao_cards = [
        html.Div([
            html.H4(dados_clima['Data'].iloc[i], style={'fontSize': '1em', 'marginBottom': '4px', 'color': '#555'}),
            html.P(dados_clima['Dia da Semana'].iloc[i], style={'fontSize': '0.9em', 'color': '#777'}),
            html.I(className=dados_clima['Ícone'].iloc[i], style={'fontSize': '3em', 'color': '#ffa500', 'marginBottom': '8px'}),
            html.Div(f"{dados_clima['Temperatura Máxima (°C)'].iloc[i]:.1f}°C", style={'fontSize': '1.5em', 'fontWeight': 'bold'})
        ], className="card-style", style={
            'padding': '25px', 
            'backgroundColor': 'rgba(255, 255, 255, 0.9)', 
            'textAlign': 'center', 
            'width': '150px', 
            'height': '230px',
            'margin': '10px'
        }) for i in range(min(len(dados_clima), 5))
    ]
    
    return clima_atual, previsao_cards

# if __name__ == '__main__':
#     app.run_server(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)