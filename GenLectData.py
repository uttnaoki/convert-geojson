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

    this_type = feature["geometry"]["type"]

    # マルチポリゴンを単一ポリゴンに変換する関数
    def Multi2Mono(multi_polygon):
        mono_polygon = [[]]
        for polygon in multi_polygon:
            mono_polygon[0].extend(polygon[0])
        return mono_polygon

    # ポリゴンを取得
    if this_type == "MultiPolygon":
        this_polygon = Multi2Mono(feature["geometry"]["coordinates"])
        result["geometry"]["type"] = "Polygon"
    else:
        this_polygon = feature["geometry"]["coordinates"]

    # ポリゴンの座標について、最小と最大を取得（x_min, x_max, y_min, y_max）
    corners = get_corner(this_polygon[0])
    result["geometry"]["coordinates"] = [[
        [corners[0], corners[3]],
        [corners[1], corners[3]],
        [corners[1], corners[2]],
        [corners[0], corners[2]]
    ]]
    return result

if __name__ == "__main__":
    with open("source/20200401_fukuoka_park.geojson") as f:
    # with open("source/fukuoka_park.geojson") as f:
        geojson = json.load(f)
    
    lect_features = [
        conv_lect_feature(f) for f in geojson["features"]
        if len(f["geometry"]["coordinates"]) > 0 ]
    geojson["features"] = lect_features

    with open("output/fukuoka_park_lect.json", "w", encoding='utf8') as f:
        json.dump(geojson, f, ensure_ascii=False)

