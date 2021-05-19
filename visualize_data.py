import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Event callback
def on_pick(event):
    global graphs, fig_ser
    print(event)
    event_legend = event.artist
    is_visible = event_legend.get_visible()
    graphs[legend].set_visible(not is_visible)
    event_legend.set_visible(not is_visible)
    fig_ser.canvas.draw()


# Reading cleaned data
data = pd.read_csv('clean_data.csv')

# Group by decade, applying different aggregation functions per column
decade_data = data.groupby((data.year//10)*10).agg({
    'acousticness': 'mean',
    'danceability': 'mean',
    'duration_ms': 'mean',
    'energy': 'mean',
    'instrumentalness': 'mean',
    'liveness': 'mean',
    'loudness': 'mean',
    'year': 'count'
})
decade_data.index.name = 'decade'
decade_data = decade_data.reset_index()
labels = decade_data['decade'].tolist()
# Plot pie chart of total songs per decade
values = decade_data['year'].tolist()
fig, ax = plt.subplots()
fig.canvas.set_window_title('Figura 1 de 3')
ax.pie(values, labels=labels, autopct='%1.1f%%')
ax.title.set_text('Distribución de canciones por década')
plt.show()

# Plot features time series per decade
values = decade_data['year'].tolist()
fig_ser, ax = plt.subplots()
fig_ser.canvas.set_window_title('Figura 2 de 3')
acous = ax.plot(labels, decade_data['acousticness'], 'b-o', label='acousticness')
danc = ax.plot(labels, decade_data['danceability'], 'r-o', label='danceability')
ener = ax.plot(labels, decade_data['energy'], 'g-o', label='energy')
ins = ax.plot(labels, decade_data['instrumentalness'], 'm-o', label='instrumentalness')
liv = ax.plot(labels, decade_data['liveness'], 'y-o', label='liveness')
legend = plt.legend()
acous_legend, danc_legend, ener_legend, ins_legend, liv_legend = legend.get_lines()
acous_legend.set_picker(True)
acous_legend.set_pickradius(10)
danc_legend.set_picker(True)
danc_legend.set_pickradius(10)
ener_legend.set_picker(True)
ener_legend.set_pickradius(10)
ins_legend.set_picker(True)
ins_legend.set_pickradius(10)
liv_legend.set_picker(True)
liv_legend.set_pickradius(10)
graphs = {
    acous_legend: acous,
    danc_legend: danc,
    ener_legend: ener,
    ins_legend: ins,
    liv_legend: liv
}
plt.connect('pick_event', on_pick)
ax.title.set_text('Evolución de las características por década')
plt.show()

# Plot loudness
fig, ax = plt.subplots()
fig.canvas.set_window_title('Figura 3 de 3')
ax.bar(labels, decade_data['loudness'], width=30)
ax.invert_yaxis()

ax.title.set_text('Volumen en decibelios por década')
plt.show()
