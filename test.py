import geo

wifi = geo.get_wifi()
geo  = geo.get_geo(wifi)
print(geo)
print(f"For Google Maps: {geo["location"]["lat"]}, {geo["location"]["lng"]}")