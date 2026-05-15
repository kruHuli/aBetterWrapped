from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

dfS = pd.read_csv('/Users/kruthikhulisandra/Desktop/SpotifyProject/dfSCleaned.csv')



# Prepare the data
daily_streamed = (
    dfS.groupby([pd.to_datetime(dfS['date'], errors='coerce'), 'platform'])['ms_played']
    .sum()
    .reset_index(name='daily_ms_played')
)

# Convert milliseconds to hours
daily_streamed['daily_hours_played'] = daily_streamed['daily_ms_played'] / 3_600_000

# Initialize the Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Interactive Histogram of Daily Hours Played by Platform"),
    dcc.Dropdown(
        id='platform-dropdown',
        options=[
            {'label': platform, 'value': platform}
            for platform in daily_streamed['platform'].unique()
        ],
        value=daily_streamed['platform'].unique()[0],  # Default selection
        clearable=False
    ),
    dcc.Graph(id='histogram-plot')
])

# Callback to update the histogram
@app.callback(
    Output('histogram-plot', 'figure'),
    Input('platform-dropdown', 'value')
)
def update_histogram(selected_platform):
    # Filter data based on the selected platform
    filtered_data = daily_streamed[daily_streamed['platform'] == selected_platform]

    # Create the histogram with defined bins
    fig = px.histogram(
        filtered_data,
        x='daily_hours_played',
        nbins=24,  # 24 bins for each hour
        title=f'Daily Hours Played for {selected_platform}',
        labels={'daily_hours_played': 'Daily Hours Played'},
        range_x=[0, 24],  # Ensure bins start at 0 and end at 24
        marginal='box'  # Optional: add a box plot on top for summary statistics
    )

    # Customize layout for better readability
    fig.update_layout(
        xaxis_title='Daily Hours Played',
        yaxis_title='Frequency',
        title_x=0.5  # Center the title
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
