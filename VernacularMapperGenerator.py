# This file is originally taken from The Python Mega Course: Building 10 Real World Application on Udemy
# It has been adapted for use on the Vernacular Mapper

import folium
import pandas

data = pandas.read_csv("data/usa.csv")
lat = list(data["lat"])
lon = list(data["lon"])
station = list(data["station_name"])

#def color_producer(elevation):
#    if elevation < 1000:
#        return 'green'
#    elif 1000 <= elevation < 3000:
#        return 'orange'
#    else:
#        return 'red'

def get_frame(url,width,height):
    html = """ 
            <!doctype html>
        <html>
        <iframe id="myIFrame" width="{}" height="{}" src={}""".format(width,height,url) + """ frameborder="0"></iframe>
        <script type="text/javascript">
        var resizeIFrame = function(event) {
            var loc = document.location;
            if (event.origin != loc.protocol + '//' + loc.host) return;

            var myIFrame = document.getElementById('myIFrame');
            if (myIFrame) {
                myIFrame.style.height = event.data.h + "px";
                myIFrame.style.width  = event.data.w + "px";
            }
        };
        if (window.addEventListener) {
            window.addEventListener("message", resizeIFrame, false);
        } else if (window.attachEvent) {
            window.attachEvent("onmessage", resizeIFrame);
        }
        </script>
        </html>"""

    popup = get_frame(url,
                      width,
                      height)

    marker = folium.CircleMarker([lat,lon],
                                 radius=radius,
                                 color='#3186cc',
                                 fill_color = '#3186cc',
                                 popup=popup)

    marker.add_to(map)



    iframe = folium.element.IFrame(html=html,width=width,height=height)
    popup = folium.Popup(iframe,max_width=width)
    return popup

map = folium.Map(location=[38.903477, -77.065231], zoom_start=6, tiles="Mapbox Bright")

fgv = folium.FeatureGroup(name="Weather Stations")

for lt, ln, stat in zip(lat, lon, station):
    fgv.add_child(folium.CircleMarker(location=[lt, ln],
                                      radius = 6, tooltip=str(stat),
                                      popup=folium.Popup(html="""
                                                            <h2>Weather Averages</h2>
                                                            <a href='https://www.google.com/'>Google Link</a>
                                                            """),  # get_frame('https://www.google.com/', 150, 150),
                                      fill_color='grey',
                                      fill=True, fill_opacity=0.7))

#fgp = folium.FeatureGroup(name="Population")

#fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
#style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
#else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
#map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("VernacularMapper.html")
