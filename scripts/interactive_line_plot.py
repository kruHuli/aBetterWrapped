from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

dfS = pd.read_csv('/Users/kruthikhulisandra/Desktop/SpotifyProject/dfSCleaned.csv')




# Prepare the data
ms_played_by_day = (
    dfS.groupby(pd.to_datetime(dfS['date'], errors='coerce'))['ms_played']
    .sum()
    .reset_index(name='ms_played')
)

# Add a column for hours played
ms_played_by_day['hours_played'] = ms_played_by_day['ms_played'] / 3_600_000

# Ensure the date column is in datetime format
ms_played_by_day['date'] = pd.to_datetime(ms_played_by_day['date'])

# Filter the data to exclude days with less than 0.05 hours played
filtered_data = ms_played_by_day[ms_played_by_day['hours_played'] >= 0.05]

# Initialize the Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    dcc.Graph(id='line-plot', style={'height': '800px'}),  # Make the plot taller
    dcc.RangeSlider(
        id='date-range-slider',
        min=0,
        max=len(filtered_data) - 1,
        value=[0, len(filtered_data) - 1],
        marks={i: str(date) for i, date in enumerate(filtered_data['date'].dt.strftime('%Y-%m-%d'))},
        step=1
    )
])

# Callback to update the graph
@app.callback(
    Output('line-plot', 'figure'),
    Input('date-range-slider', 'value')
)
def update_plot(date_range):
    # Filter data based on the selected date range
    date_filtered_data = filtered_data.iloc[date_range[0]:date_range[1] + 1]

    # Calculate the dynamic average
    dynamic_average = date_filtered_data['hours_played'].mean()

    # Create the plot
    fig = px.line(
        date_filtered_data,
        x='date',
        y='hours_played',
        title='Daily Aggregation of Hours Played (Excluding < 0.05 Hours)',
        labels={'date': 'Date', 'hours_played': 'Hours Played'},
        markers=True  # Add markers for each data point
    )

    # Customize marker style
    fig.update_traces(marker=dict(symbol='circle', size=6))  # Use dots as markers

    # Add the dynamic average line
    fig.add_scatter(
        x=[date_filtered_data['date'].min(), date_filtered_data['date'].max()],
        y=[dynamic_average, dynamic_average],
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name=f'Average: {dynamic_average:.2f} Hours'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)