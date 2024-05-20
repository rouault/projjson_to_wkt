projjson_to_wkt - Python library to convert a PROJJSON string to WKT
====================================================================

Converts a [PROJJSON](https://proj.org/specifications/projjson.html) CRS
string into a [WKT CRS](https://www.ogc.org/standards/wkt-crs) string (WKT1
or WKT2:2019 variants supported).
Warning: while the export to WKT1 should be syntaxically correct, datum, projection
method or parameter names will be the one of WKT2, and thus a number of
implementations will in practice fail to understand such WKT1 strings.

This library is a single file with no dependency, that could be easily ported
to other languages. The following languages are available:

- Python (this repository)
- [JavaScript](https://github.com/m-mohr/projjson_to_wkt)

Currently supported object types are: GeodeticCRS, GeographicCRS, ProjectedCRS,
VerticalCRS, CompoundCRS, DerivedGeodeticCRS and DerivedGeographicCRS.

## Usage

```
usage: projjson_to_wkt.py [-h] [--format {WKT2:2019,WKT1}] [--single-line] projjson
```

## Examples

### Command line interface

```shell
$ ./projjson_to_wkt.py '{"$schema":"https://proj.org/schemas/v0.4/projjson.schema.json","type":"CompoundCRS","name":"WGS 84 + EGM96 height","components":[{"type":"GeographicCRS","name":"WGS 84","datum_ensemble":{"name":"World Geodetic System 1984 ensemble","members":[{"name":"World Geodetic System 1984 (Transit)","id":{"authority":"EPSG","code":1166}},{"name":"World Geodetic System 1984 (G730)","id":{"authority":"EPSG","code":1152}},{"name":"World Geodetic System 1984 (G873)","id":{"authority":"EPSG","code":1153}},{"name":"World Geodetic System 1984 (G1150)","id":{"authority":"EPSG","code":1154}},{"name":"World Geodetic System 1984 (G1674)","id":{"authority":"EPSG","code":1155}},{"name":"World Geodetic System 1984 (G1762)","id":{"authority":"EPSG","code":1156}},{"name":"World Geodetic System 1984 (G2139)","id":{"authority":"EPSG","code":1309}}],"ellipsoid":{"name":"WGS 84","semi_major_axis":6378137,"inverse_flattening":298.257223563},"accuracy":"2.0","id":{"authority":"EPSG","code":6326}},"coordinate_system":{"subtype":"ellipsoidal","axis":[{"name":"Geodetic latitude","abbreviation":"Lat","direction":"north","unit":"degree"},{"name":"Geodetic longitude","abbreviation":"Lon","direction":"east","unit":"degree"}]}},{"type":"VerticalCRS","name":"EGM96 height","datum":{"type":"VerticalReferenceFrame","name":"EGM96 geoid"},"coordinate_system":{"subtype":"vertical","axis":[{"name":"Gravity-related height","abbreviation":"H","direction":"up","unit":"metre"}]}}],"scope":"Spatial referencing.","area":"World.","bbox":{"south_latitude":-90,"west_longitude":-180,"north_latitude":90,"east_longitude":180},"id":{"authority":"EPSG","code":9707}}'

COMPOUNDCRS["WGS 84 + EGM96 height",
    GEOGCRS["WGS 84",
        ENSEMBLE["World Geodetic System 1984 ensemble",
            MEMBER["World Geodetic System 1984 (Transit)",
                ID["EPSG",1166]],
            MEMBER["World Geodetic System 1984 (G730)",
                ID["EPSG",1152]],
            MEMBER["World Geodetic System 1984 (G873)",
                ID["EPSG",1153]],
            MEMBER["World Geodetic System 1984 (G1150)",
                ID["EPSG",1154]],
            MEMBER["World Geodetic System 1984 (G1674)",
                ID["EPSG",1155]],
            MEMBER["World Geodetic System 1984 (G1762)",
                ID["EPSG",1156]],
            MEMBER["World Geodetic System 1984 (G2139)",
                ID["EPSG",1309]],
            ELLIPSOID["WGS 84",6378137,298.257223563,
                LENGTHUNIT["metre",1]],
            ENSEMBLEACCURACY[2.0],
            ID["EPSG",6326]],
        CS[ellipsoidal,2],
            AXIS["geodetic latitude (Lat)",north,
                ANGLEUNIT["degree",0.0174532925199433]],
            AXIS["geodetic longitude (Lon)",east,
                ANGLEUNIT["degree",0.0174532925199433]]],
    VERTCRS["EGM96 height",
        VDATUM["EGM96 geoid"],
        CS[vertical,1],
            AXIS["gravity-related height (H)",up,
                LENGTHUNIT["metre",1]]],
    USAGE[
        SCOPE["Spatial referencing."],
        AREA["World."],
        BBOX[-90,-180,90,180]],
    ID["EPSG",9707]]
```

### Programmatic interface

```python
import projjson_to_wkt

json = {
  "$schema": "https://proj.org/schemas/v0.4/projjson.schema.json",
  "type": "CompoundCRS",
  "name": "WGS 84 + EGM96 height",
  "components": [
    {
      "type": "GeographicCRS",
      "name": "WGS 84",
      "datum_ensemble": {
        "name": "World Geodetic System 1984 ensemble",
        "members": [
          {
            "name": "World Geodetic System 1984 (Transit)",
            "id": {
              "authority": "EPSG",
              "code": 1166
            }
          },
          {
            "name": "World Geodetic System 1984 (G730)",
            "id": {
              "authority": "EPSG",
              "code": 1152
            }
          },
          {
            "name": "World Geodetic System 1984 (G873)",
            "id": {
              "authority": "EPSG",
              "code": 1153
            }
          },
          {
            "name": "World Geodetic System 1984 (G1150)",
            "id": {
              "authority": "EPSG",
              "code": 1154
            }
          },
          {
            "name": "World Geodetic System 1984 (G1674)",
            "id": {
              "authority": "EPSG",
              "code": 1155
            }
          },
          {
            "name": "World Geodetic System 1984 (G1762)",
            "id": {
              "authority": "EPSG",
              "code": 1156
            }
          },
          {
            "name": "World Geodetic System 1984 (G2139)",
            "id": {
              "authority": "EPSG",
              "code": 1309
            }
          }
        ],
        "ellipsoid": {
          "name": "WGS 84",
          "semi_major_axis": 6378137,
          "inverse_flattening": 298.257223563
        },
        "accuracy": "2.0",
        "id": {
          "authority": "EPSG",
          "code": 6326
        }
      },
      "coordinate_system": {
        "subtype": "ellipsoidal",
        "axis": [
          {
            "name": "Geodetic latitude",
            "abbreviation": "Lat",
            "direction": "north",
            "unit": "degree"
          },
          {
            "name": "Geodetic longitude",
            "abbreviation": "Lon",
            "direction": "east",
            "unit": "degree"
          }
        ]
      }
    },
    {
      "type": "VerticalCRS",
      "name": "EGM96 height",
      "datum": {
        "type": "VerticalReferenceFrame",
        "name": "EGM96 geoid"
      },
      "coordinate_system": {
        "subtype": "vertical",
        "axis": [
          {
            "name": "Gravity-related height",
            "abbreviation": "H",
            "direction": "up",
            "unit": "metre"
          }
        ]
      }
    }
  ],
  "scope": "Spatial referencing.",
  "area": "World.",
  "bbox": {
    "south_latitude": -90,
    "west_longitude": -180,
    "north_latitude": 90,
    "east_longitude": 180
  },
  "id": {
    "authority": "EPSG",
    "code": 9707
  }
}

options=projjson_to_wkt.Options(
    format = projjson_to_wkt.WKT1, single_line=True)
wkt = projjson_to_wkt.to_wkt(json, options=options)
```

## License

MIT
