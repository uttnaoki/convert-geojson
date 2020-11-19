import json

def get_corner(coors):
    x_min = y_min = 400
    x_max = y_max = -400
    for c in coors:
        if c[0] < x_min:
            x_min = c[0]
        if c[0] > x_max:
            x_max = c[0]
        if c[1] < y_min:
            y_min = c[1]
        if c[1] > y_max:
            y_max = c[1]
    return (x_min, x_max, y_min, y_max)

def conv_lect_feature(feature):
    this_polygon = feature["geometry"]["coordinates"]
    corners = get_corner(this_polygon[0])
    lect_polygon = this_polygon
    lect_polygon[0] = [
        [corners[0], corners[3]],
        [corners[1], corners[3]],
        [corners[1], corners[2]],
        [corners[0], corners[2]]
    ]
    return lect_polygon

if __name__ == "__main__":
    with open("source/fukuoka_park.geojson") as f:
        geojson = json.load(f)
    
    lect_features = [conv_lect_feature(f) for f in geojson["features"]]
    geojson["features"] = lect_features

    with open("output/fukuoka_park_lect.geojson", "w") as f:
        json.dump(geojson, f)
