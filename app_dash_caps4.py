# 1. Import Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
# import statistics 
# from statistics import mode
import plotly.express as px

# 2. Create a Dash app instance
app = dash.Dash(
    external_stylesheets=[dbc.themes.UNITED],
    name = 'Covid-19'
)

app.title = 'Covid-19 Dashbord Analytics'

# Jumbotron
jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("Covid-19 Dashbord Analytics", className="display-3"),
            html.P(
                "Exploratory Data Analytics Coronavirus (COVID-19) Dashboard",
                className="lead",
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
)


## --- Import Dataset Covid
df=pd.read_csv('COVID-19_Coronavirus.csv')

### CARD CONTENT
total_country = [
    dbc.CardHeader('Number of Country'),
    dbc.CardBody([
        html.H1([df['Country'].nunique()])
    ]),
]

total_continent = [
    dbc.CardHeader('Number of Continent'),
    dbc.CardBody([
        html.H1(df['Continent'].nunique())
    ]),
]

total_cases = [
    dbc.CardHeader('Total Cases'),
    dbc.CardBody([
        html.H1(df['Total Cases'].sum())
    ]),
]

total_deaths = [
    dbc.CardHeader('Total Deaths'),
    dbc.CardBody([
        html.H1(df['Total Deaths'].sum())
    ]),
]

###### --- Visualization

### CHOROPLETH
# Data aggregation
aggx = pd.crosstab(
    index=[df['Country'],df['ISO 3166-1 alpha-3 CODE']],
    columns='No of Deaths',
    values=df['Total Deaths'],
    aggfunc='sum'
).reset_index()


# Visualization
plot_map = px.choropleth(aggx,
             locations='ISO 3166-1 alpha-3 CODE',
             color_continuous_scale='fall',
             color='No of Deaths',
             template='seaborn')

### BARPLOT: RANKING
# Data aggregation
Europe=df[df['Continent']=='Europe']
top_Europe = Europe.sort_values('Total Deaths').tail(5)

# Visualize ranking of total deaths
bar_deaths = px.bar(
    top_Europe,
    x = 'Total Deaths',
    y = 'Country',
    template = 'seaborn',
    title = 'Rangking of Total Deaths in Europe'
)

# Data aggregation
Europe=df[df['Continent']=='Europe']
top_Europe2 = Europe.sort_values('Total Cases').tail(5)

# Visualize ranking of total cases
# bar_cases = px.bar(
#     top_Europe2,
#     x = 'Total Cases',
#     y = 'Country',
#     template = 'seaborn',
#     title = 'Rangking of Total Cases in Europe'
# )

### PIEPLOT
# aggregation
agg2=pd.crosstab(
    index=df['Continent'],
    columns='Total Deaths'
).reset_index()

# visualize
pie = px.pie(
    agg2,
    values='Total Deaths',
    names='Continent',
    color_discrete_sequence=['lightblue','grey', 'salmon', 'pink', 'lightgreen', 'aqua'],
    template='seaborn',
    hole=0.4,
    labels={
        'Continent': 'Continent'
    }
)

# --------------------------------------------------------------------------

#### -----LAYOUT-----

app.layout = html.Div([
    jumbotron,
    
    html.Br(),
    
    ## --Component Main Page---

    html.Div([

        ## --ROW1--
        dbc.Row
        ([
            # COL 1
            dbc.Col
            ([
                dbc.Card
                ([
                    html.H2('Covid-19'),
                    dbc.CardBody
                        ([
                            html.P('Coronavirus disease 2019 (COVID-19) is a contagious disease caused by a virus, the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). The first known case was identified in Wuhan, China, in December 2019.The disease spread worldwide, leading to the COVID-19 pandemic.'),
                            html.P("COVID‑19 transmits when people breathe in air contaminated by droplets and small airborne particles containing the virus. Several COVID-19 testing methods have been developed to diagnose the disease. The standard diagnostic method is by detection of the virus's nucleic acid by real-time reverse transcription polymerase chain reaction (rRT-PCR), transcription-mediated amplification (TMA), or by reverse transcription loop-mediated isothermal amplification (RT-LAMP) from a nasopharyngeal swab."),
                        ]),
                ]),
            ], width = 4),

            #COL 2
            dbc.Col(
                    [
                    dbc.Card(total_continent, color='lightgreen',),
                    html.Br(),
                    dbc.Card(total_cases, color='secondary',),
                    html.Br(),
                    dbc.Card(total_deaths, color='light',),
                    ],
                    width=2),

            # COL 3
            dbc.Col
            ([
                dbc.Card([
                html.H2('Maps Covid-19'),
                dcc.Graph(figure=plot_map)

                ])
            ], 
            width = 6)

        ]),

        html.Hr(),

        ## --ROW2--
        dbc.Row
        ([
            ### COLUMN 2
            dbc.Col
            ([
                dbc.Card
                ([
                    dbc.CardHeader('Select Continent'),
                    dbc.CardBody
                    (
                        dcc.Dropdown
                        (
                            id='choose_continent',
                            options=df['Continent'].unique(),
                            value='Europe',
                        ),
                    ),
                
                dcc.Graph
                (
                    id='plotpie',
                    figure=pie,
                ),
                ]),
            ], 
            width=6),

            ### COLUMN 1
            dbc.Col
            ([
                dbc.Card([
                    html.H2('Analysis by Continent'),
                dbc.Tabs
                ([
                    ## --- TAB 1: CASES
                    dbc.Tab
                    (
                        dcc.Graph
                        (
                            id='plotcases',
                        ),
                        label='Cases'),

                    ## --- TAB 2: DEATHS
                    dbc.Tab
                    (
                        dcc.Graph
                        (
                            id='plotdeaths',
                            figure=bar_deaths,
                        ),
                        label='Deaths'),
                ]),

                ])
                
            ], width=6),

        ]),

    ], style={
        'paddingLeft':'30px',
        'paddingRight':'30px',
    }),

     #ROW7
    dbc.Col([
        dbc.Card([
            html.H6('Create By : tyasrindhu')
        ]),
    ])

])

### Callback Plot Cases
@app.callback(
    Output(component_id='plotcases', component_property='figure'),
    Input(component_id='choose_continent', component_property='value')
)

def update_plot1(continent_name):
    # Data aggregation
    Europe=df[df['Continent']== continent_name]

    top_Europe = Europe.sort_values('Total Cases').tail(5)

    # Visualize
    bar_cases = px.bar(
        top_Europe,
        x = 'Total Cases',
        y = 'Country',
        template = 'seaborn',
        title = f'Rangking of Total Cases in {str(continent_name)}'
    )
    return  bar_cases

### Callback Plot Deaths
@app.callback(
    Output(component_id='plotdeaths', component_property='figure'),
    Input(component_id='choose_continent', component_property='value')
)
def update_plot1(continent_name):
    Europe=df[df['Continent']== continent_name].sort_values('Total Deaths').tail(5)
    bar_deaths = px.bar(
        Europe,
        x = 'Total Deaths',
        y = 'Country',
        template = 'seaborn',
        title = f'Rangking of Total Deaths in {str(continent_name)}'
    )

    return bar_deaths

# 3. Start the Dash server
if __name__ == "__main__":
    app.run_server()