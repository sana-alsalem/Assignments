#Dashboard final code 

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_site = spacex_df['Launch Site'].unique()
site_df = {site: spacex_df[spacex_df['Launch Site'] == site] for site in launch_site}
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(id='site-dropdown',
             options=[
                 {'label': 'All Sites', 'value': 'All'}
             ] + [{'label': site, 'value': site} for site in site_df],
             value='All',
             placeholder="Select a Launch Site",
             searchable=True
             ),


    html.Br(),
    
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 10000: '10000'},
                    value=[min_payload, max_payload]),

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for success-pie-chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'All':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, names='Launch Site', values='class',
                     title='Total Success Launches per Launch Site',
                     color_discrete_sequence=px.colors.sequential.RdBu)
    else:
        choosen_site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_launches = choosen_site_df['class'].sum()
        failed_launches = choosen_site_df['class'].count() - success_launches
        labels = ['Successful Launches', 'Failed Launches']
        sizes = [success_launches, failed_launches]
        colors = ['green', 'red']
        fig = px.pie(names=labels, values=sizes,
                     title=f"Launch Success Rate for {entered_site}",
                     color_discrete_sequence=colors)
    return fig

# Callback for success-payload-scatter-chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if entered_site != 'All':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                     color="Booster Version Category",
                     title=f"Success Payload Mass for {'All Sites' if entered_site == 'All' else entered_site}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

