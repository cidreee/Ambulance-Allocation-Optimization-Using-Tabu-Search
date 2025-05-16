import pandas as pd
import folium
import branca

# Cargar los datos
filtered_data = pd.read_csv('filtered_accidentes_Ags_2019.csv', encoding='ISO-8859-1', low_memory=False)

# Agrupar por LONGITUD y LATITUD y contar el número de accidentes
grouped_data = filtered_data.groupby(['LONGITUD', 'LATITUD']).size().reset_index(name='count')

# Crear una escala de colores basada en el valor de count
color_scale = branca.colormap.LinearColormap(colors=['blue', 'red'], index=[min(grouped_data['count']), max(grouped_data['count'])], vmin=min(grouped_data['count']), vmax=max(grouped_data['count']) )

# Crear el mapa
m_grouped = folium.Map(location=[filtered_data['LATITUD'].mean(), filtered_data['LONGITUD'].mean()], zoom_start=12)

# Agregar puntos al mapa con el número de accidentes y color basado en count
for _, row in grouped_data.iterrows():
    folium.CircleMarker(
        location=(row['LATITUD'], row['LONGITUD']),
        radius=5,
        color=color_scale(row['count']),
        fill=True,
        fill_color=color_scale(row['count']),
        fill_opacity=0.6,
        popup=str(row['count'])
    ).add_to(m_grouped)

# Lista de puntos específicos con 3 ambulancias 
specific_points = [
    {'lat': 21.91431, 'lon': -102.24805, 'label': 'Ambulancia 1'},  # Ambulancia 1
    {'lat': 21.832320000000003, 'lon': -102.29015, 'label': 'Ambulancia 2'},  # Ambulancia 2
    {'lat': 21.86018, 'lon': -102.28198, 'label': 'Ambulancia 3'},  # Ambulancia 3
    {'lat': 21.8661, 'lon': -102.29827, 'label': 'Ambulancia 4'},  # Ambulancia 4
]



# Agregar estos puntos al mapa
for point in specific_points:
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=point['label'],
        icon=folium.Icon(color='green', icon='info-sign')  
    ).add_to(m_grouped)

# Guardar el mapa en un archivo HTML
m_grouped.save('ej_2019_ambulancias_BAS.html')
