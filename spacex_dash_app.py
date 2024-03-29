# Import required libraries
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
spacex_df.rename(columns={'Payload Mass (kg)':'PayloadMass'},inplace=True)
# Create a dash application
app = dash.Dash(__name__)

launch_site = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_site = launch_site['Launch Site'].to_list()

launch_options = [{'label': 'All Sites', 'value': 'ALL'}]
for site in launch_site:
    launch_options.append({'label':site,'value':site})
# print(launch_options)


 #Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='Launch Site',
        title='Total Success By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class').count()
        print(filtered_df)
        fig = px.pie(filtered_df, values='Launch Site',
        names=[1,0],
        title='Total Success Launches for '+entered_site)
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def scatter_plot(entered_site,payload_mass):
    print(payload_mass)
    filtered_df = spacex_df.query("""{}< PayloadMass <{}""".format(payload_mass[0],payload_mass[1]))
    if entered_site == 'ALL':
        fig=px.scatter(x=filtered_df['PayloadMass'],y=filtered_df['class'],color=filtered_df['Booster Version Category']
                       )
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig=px.scatter(x=filtered_df['PayloadMass'],y=filtered_df['class'],color=filtered_df['Booster Version Category']
                       )
    return fig
        
    
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                      options=launch_options,
                                                      value='ALL',
                                                      placeholder="Launch Sites",
                                                      searchable=True
                                                      )),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                min=0, max=16000, step=1000,
                marks={0:'0',
                       100:'100'},
                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
