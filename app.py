# Import des librairies
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv('arbres10percent.csv')

# Initialisation de l'app Dash
app = Dash(__name__)

# Affichage de l'app
app.layout = html.Div([
    html.H1(children='Tree Dash App', style={'textAlign': 'center', 'fontFamily':'Verdana'}),
    
    # Menu déroulant pour DOMANIALITE
    dcc.Dropdown(
        id='dom-dropdown',
        options=[{'label': dom, 'value': dom} for dom in df['DOMANIALITE'].unique()],
    ),
    
    # Menu déroulant pour STADE DE DEVELOPPEMENT
    dcc.Dropdown(
        id='stage-dropdown',
        options=[{'label': stage, 'value': stage} for stage in df['STADE DE DEVELOPPEMENT'].unique() if pd.notnull(stage)],
    ),
    
    # Graphiques
    dcc.Graph(id='height-histogram'),
    dcc.Graph(id='circumference-histogram')
])

# Callback pour mettre à jour les histogrammes en fonction des menus déroulants
@app.callback(
    [Output('height-histogram', 'figure'),
     Output('circumference-histogram', 'figure')],
    [Input('dom-dropdown', 'value'),
     Input('stage-dropdown', 'value')]
)
def update_histograms(selected_domanialite, selected_stage):
    # Filtre le DataFrame selon les valeurs sélectionnées
    filtered_df = df[(df['DOMANIALITE'] == selected_domanialite) & (df['STADE DE DEVELOPPEMENT'] == selected_stage)]
    
    # Histogramme de la hauteur
    height_histogram = px.histogram(filtered_df, x='HAUTEUR (m)', title='Histogramme de la hauteur des arbres')
    height_histogram.update_layout(title_x=0.5)
    
    # Histogramme de la circonférence
    circumference_histogram = px.histogram(filtered_df, x='CIRCONFERENCE (cm)', title='Histogramme de la circonférence des arbres')
    circumference_histogram.update_layout(title_x=0.5)
    
    return height_histogram, circumference_histogram

# Execution de l'app
if __name__ == '__main__':
    app.run_server(debug=True)
