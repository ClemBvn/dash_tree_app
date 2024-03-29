# Import des librairies
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Lecture du fichier CSV
df = pd.read_csv('arbres10percent.csv')

# Séparation de la colonne 'geo_point_2d' en latitude et longitude
df[['LATITUDE', 'LONGITUDE']] = df['geo_point_2d'].str.split(', ', expand=True).astype(float)

# Initialisation de l'app Dash
app = Dash(__name__)

# Affichage de l'app
app.layout = html.Div([
    # Titre de la page
    html.H1(children='Tree Dash App', style={'textAlign': 'center', 'fontFamily':'Verdana'}),
    
    # Bloc menus déroulants
    html.Div([
        html.P('Sélectionnez un domaine et un stade de développement', style={'textAlign': 'center', 'fontFamily':'Verdana'}),
        dcc.Dropdown(
                id='dom-dropdown',
                options=[{'label': dom, 'value': dom} for dom in df['DOMANIALITE'].unique()],
                style={'width': '50%', 'margin': 'auto'}
            ),
        dcc.Dropdown(
                id='stage-dropdown',
                options=[{'label': stage, 'value': stage} for stage in df['STADE DE DEVELOPPEMENT'].unique() if pd.notnull(stage)],
                style={'width': '50%', 'margin': 'auto'}
            ),
        ]),

    # Bloc histogrammes 
    html.Div([
        # Bloc histogramme hauteur
        html.Div([
            dcc.Graph(id='height-histogram')   
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        # Bloc histogramme circonférence
        html.Div([
            dcc.Graph(id='circumference-histogram')
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),

    # Bloc carte
    html.Div([
        html.P('Sélectionnez un stade de développement', style={'textAlign': 'center', 'fontFamily':'Verdana'}),
        dcc.Dropdown(
            id='map-stage-dropdown',
            options=[{'label': stage, 'value': stage} for stage in df['STADE DE DEVELOPPEMENT'].unique() if pd.notnull(stage)],
            multi=True,
            value=[],
            style={'width': '70%', 'margin': 'auto'}
        ),
        dcc.Graph(id='tree-map', style={'height': '70vh'})
    ])
])

# Callback pour mettre à jour les histogrammes en fonction des menus déroulants
@app.callback(
    [Output('height-histogram', 'figure'),
     Output('circumference-histogram', 'figure')],
    [Input('dom-dropdown', 'value'),
     Input('stage-dropdown', 'value')]
)
def update_histograms(selected_domanialite, selected_stage):
    # Filtre le DataFrame selon les valeurs sélectionnées pour les histogrammes
    filtered_df = df[(df['DOMANIALITE'] == selected_domanialite) & (df['STADE DE DEVELOPPEMENT'] == selected_stage)]
    
    # Histogramme de la hauteur
    height_histogram = px.histogram(filtered_df, x='HAUTEUR (m)', title='Histogramme de la hauteur des arbres')
    height_histogram.update_layout(title_x=0.5)
    
    # Histogramme de la circonférence
    circumference_histogram = px.histogram(filtered_df, x='CIRCONFERENCE (cm)', title='Histogramme de la circonférence des arbres')
    circumference_histogram.update_layout(title_x=0.5)
    
    return height_histogram, circumference_histogram


# Callback pour mettre à jour la carte en fonction du menu déroulant
@app.callback(
    Output('tree-map', 'figure'),
    Input('map-stage-dropdown', 'value')
)
def update_tree_map(selected_map_stages):
    # Filtre le DataFrame selon les valeurs sélectionnées pour la carte
    map_filtered_df = df[df['STADE DE DEVELOPPEMENT'].isin(selected_map_stages)]
    
    # Carte
    tree_map = px.scatter_mapbox(
        map_filtered_df,
        lat='LATITUDE',
        lon='LONGITUDE',
        color='STADE DE DEVELOPPEMENT',
        title='Carte de localisation des arbres',
        mapbox_style='open-street-map',
        zoom=10
    )
    tree_map.update_layout(title_x=0.5)
    
    return tree_map

# Execution de l'app
if __name__ == '__main__':
    app.run_server(debug=True)
