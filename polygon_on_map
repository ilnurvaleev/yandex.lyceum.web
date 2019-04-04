import folium
import json
import os



def party_color(feature):
    return {
        "fillColor": feature['properties']['fill'],
        "fillOpacity": feature['properties']['fill-opacity'],
        "opacity": 0.8
    }


def popup_html(feature):
    html = '<h5> Название {}</h5>'.format(feature['properties']['name'])
    html += '<b>{}</b>'.format(feature['properties']['inf'])

    return html


m = folium.Map(
    location=[55.74759843942743, 48.742733001708984],
    # tiles='Mapbox Bright',
    zoom_start=14
)
data = open("kek.geojson", 'r').read()
# print(data)
lol = json.loads(data)
for mo in data['features']:
    gj = folium.GeoJson(
        data=mo,
        style_function=party_color,
        control=False,
        highlight_function=lambda x: {
            "fillOpacity": 0.2,
            "opacity": 1
        },
        smooth_factor=0)

    folium.Popup(popup_html(mo)).add_to(gj)
    gj.add_to(m)


folium.LayerControl().add_to(m)

m.save(os.path.join('results', 'inno.html'))
