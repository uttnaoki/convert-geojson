import json
import itertools

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
    result = feature
    this_polygon = feature["geometry"]["coordinates"]

    # 配列の深さが位置段階深い場合があるので修正
    if len(this_polygon) > 1:
        this_polygon = list(itertools.chain.from_iterable(this_polygon))


    corners = get_corner(this_polygon[0])
    result["geometry"]["coordinates"][0] = [
        [corners[0], corners[3]],
        [corners[1], corners[3]],
        [corners[1], corners[2]],
        [corners[0], corners[2]]
    ]
    return result

if __name__ == "__main__":
    with open("source/20200401_fukuoka_park.geojson") as f:
    # with open("source/fukuoka_park.geojson") as f:
        geojson = json.load(f)
    
    lect_features = [
        conv_lect_feature(f) for f in geojson["features"]
        if len(f["geometry"]["coordinates"]) > 0 ]
    geojson["features"] = lect_features

    with open("output/fukuoka_park_lect.geojson", "w", encoding='utf8') as f:
        json.dump(geojson, f, ensure_ascii=False)

