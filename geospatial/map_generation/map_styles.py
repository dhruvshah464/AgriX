MAP_STYLE = {
    "version": 8,
    "name": "AgriX Productivity",
    "sources": {"basemap": {"type": "raster"}},
    "layers": [
        {"id": "background", "type": "background", "paint": {"background-color": "#f0f4e8"}},
        {"id": "yield-points", "type": "circle", "source": "productivity"},
    ],
}
