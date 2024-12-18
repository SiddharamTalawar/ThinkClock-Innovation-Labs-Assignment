import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.io as pi

# pi.renderers.default = 'notebook'


# Load the metadata file
metadata_path = "metadata.csv"
metadata_df = pd.read_csv(metadata_path)

# Filter impedance data for relevant columns
impedance_df = metadata_df[metadata_df['type'] == 'impedance'][['start_time', 'Re', 'Rct', 'battery_id']]
dataset_df = metadata_df[metadata_df['type'] == 'impedance'][['start_time', 'filename', 'battery_id']]


# Convert `start_time` to datetime
def parse_start_time(value):
    try:
        if isinstance(value, str):
            value = value.strip("[]").replace(",", "")
            components = [float(x) for x in value.split()]
            if len(components) == 6:
                year, month, day, hour, minute, second = map(int, components[:6])
                return datetime(year, month, day, hour, minute, second)
    except (ValueError, SyntaxError, TypeError):
        return pd.NaT
    return pd.NaT

impedance_df['start_time'] = impedance_df['start_time'].apply(parse_start_time)
dataset_df['start_time'] = dataset_df['start_time'].apply(parse_start_time)

# Drop null values and sort by `start_time`
impedance_df.dropna(subset=['start_time'], inplace=True)
impedance_df.sort_values(by='start_time', inplace=True)

dataset_df.dropna(subset=['start_time'], inplace=True)
dataset_df.sort_values(by='start_time', inplace=True)


# Plot resistance values for each battery ID
for battery_id in impedance_df['battery_id'].unique():
    current_battery_info = impedance_df[impedance_df['battery_id'] == battery_id]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=current_battery_info['start_time'],
        y=current_battery_info['Re'],
        mode='lines',
        name='Re',
        line=dict(color='green'),
        hovertemplate='<b>Time:</b> %{x}<br><b>Re:</b> %{y:.2f} Ohms'
        
    ))
    fig.add_trace(go.Scatter(
        x=current_battery_info['start_time'],
        y=current_battery_info['Rct'],
        mode='lines',
        name='Rct',
        line=dict(color='blue'),
        hovertemplate='<b>Time:</b> %{x}<br><b>Rct:</b> %{y:.2f} Ohms'
    ))
    fig.update_layout(
        title=f"Resistance Battery ID {battery_id}",
        xaxis_title="Start Time",
        yaxis_title="Resistance (Ohms)",
        template="plotly"
    )
    fig.show()