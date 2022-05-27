#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# Copyright 2022, Even Rouault

import pytest
from projjson_to_wkt import to_wkt, Options, WKT1


def test_geog_crs_epsg_4326():
    j = {"$schema": "https://proj.org/schemas/v0.4/projjson.schema.json", "type": "GeographicCRS", "name": "WGS 84", "datum_ensemble": {"name": "World Geodetic System 1984 ensemble", "members": [{"name": "World Geodetic System 1984 (Transit)", "id": {"authority": "EPSG", "code": 1166}}, {"name": "World Geodetic System 1984 (G730)", "id": {"authority": "EPSG", "code": 1152}}, {"name": "World Geodetic System 1984 (G873)", "id": {"authority": "EPSG", "code": 1153}}, {"name": "World Geodetic System 1984 (G1150)", "id": {"authority": "EPSG", "code": 1154}}, {"name": "World Geodetic System 1984 (G1674)", "id": {"authority": "EPSG", "code": 1155}}, {"name": "World Geodetic System 1984 (G1762)", "id": {"authority": "EPSG", "code": 1156}}, {
        "name": "World Geodetic System 1984 (G2139)", "id": {"authority": "EPSG", "code": 1309}}], "ellipsoid": {"name": "WGS 84", "semi_major_axis": 6378137, "inverse_flattening": 298.257223563}, "accuracy": "2.0", "id": {"authority": "EPSG", "code": 6326}}, "coordinate_system": {"subtype": "ellipsoidal", "axis": [{"name": "Geodetic latitude", "abbreviation": "Lat", "direction": "north", "unit": "degree"}, {"name": "Geodetic longitude", "abbreviation": "Lon", "direction": "east", "unit": "degree"}]}, "scope": "Horizontal component of 3D system.", "area": "World.", "bbox": {"south_latitude": -90, "west_longitude": -180, "north_latitude": 90, "east_longitude": 180}, "id": {"authority": "EPSG", "code": 4326}}

    wkt = to_wkt(j)
    assert wkt == """GEOGCRS["WGS 84",
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
            ANGLEUNIT["degree",0.0174532925199433]],
    USAGE[
        SCOPE["Horizontal component of 3D system."],
        AREA["World."],
        BBOX[-90,-180,90,180]],
    ID["EPSG",4326]]"""

    wkt = to_wkt(j, options=Options(format=WKT1))
    assert wkt == """GEOGCS["WGS 84",
    DATUM["World Geodetic System 1984",
        SPHEROID["WGS 84",6378137,298.257223563],
        AUTHORITY["EPSG","6326"]],
    PRIMEM["Greenwich",0],
    UNIT["degree",0.0174532925199433],
    AXIS["Geodetic latitude (Lat)",NORTH],
    AXIS["Geodetic longitude (Lon)",EAST],
    AUTHORITY["EPSG","4326"]]"""


def test_geog_crs_epsg_4269():
    j = {"$schema": "https://proj.org/schemas/v0.4/projjson.schema.json", "type": "GeographicCRS", "name": "NAD83", "datum": {"type": "GeodeticReferenceFrame", "name": "North American Datum 1983", "ellipsoid": {"name": "GRS 1980", "semi_major_axis": 6378137, "inverse_flattening": 298.257222101}}, "coordinate_system": {"subtype": "ellipsoidal", "axis": [{"name": "Geodetic latitude", "abbreviation": "Lat", "direction": "north", "unit": "degree"}, {
        "name": "Geodetic longitude", "abbreviation": "Lon", "direction": "east", "unit": "degree"}]}, "scope": "Geodesy.", "area": "North America - onshore and offshore: Canada - Alberta; British Columbia; Manitoba; New Brunswick; Newfoundland and Labrador; Northwest Territories; Nova Scotia; Nunavut; Ontario; Prince Edward Island; Quebec; Saskatchewan; Yukon. Puerto Rico. United States (USA) - Alabama; Alaska; Arizona; Arkansas; California; Colorado; Connecticut; Delaware; Florida; Georgia; Hawaii; Idaho; Illinois; Indiana; Iowa; Kansas; Kentucky; Louisiana; Maine; Maryland; Massachusetts; Michigan; Minnesota; Mississippi; Missouri; Montana; Nebraska; Nevada; New Hampshire; New Jersey; New Mexico; New York; North Carolina; North Dakota; Ohio; Oklahoma; Oregon; Pennsylvania; Rhode Island; South Carolina; South Dakota; Tennessee; Texas; Utah; Vermont; Virginia; Washington; West Virginia; Wisconsin; Wyoming. US Virgin Islands. British Virgin Islands.", "bbox": {"south_latitude": 14.92, "west_longitude": 167.65, "north_latitude": 86.45, "east_longitude": -40.73}, "id": {"authority": "EPSG", "code": 4269}}

    wkt = to_wkt(j)
    assert wkt == """GEOGCRS["NAD83",
    DATUM["North American Datum 1983",
        ELLIPSOID["GRS 1980",6378137,298.257222101,
            LENGTHUNIT["metre",1]]],
    CS[ellipsoidal,2],
        AXIS["geodetic latitude (Lat)",north,
            ANGLEUNIT["degree",0.0174532925199433]],
        AXIS["geodetic longitude (Lon)",east,
            ANGLEUNIT["degree",0.0174532925199433]],
    USAGE[
        SCOPE["Geodesy."],
        AREA["North America - onshore and offshore: Canada - Alberta; British Columbia; Manitoba; New Brunswick; Newfoundland and Labrador; Northwest Territories; Nova Scotia; Nunavut; Ontario; Prince Edward Island; Quebec; Saskatchewan; Yukon. Puerto Rico. United States (USA) - Alabama; Alaska; Arizona; Arkansas; California; Colorado; Connecticut; Delaware; Florida; Georgia; Hawaii; Idaho; Illinois; Indiana; Iowa; Kansas; Kentucky; Louisiana; Maine; Maryland; Massachusetts; Michigan; Minnesota; Mississippi; Missouri; Montana; Nebraska; Nevada; New Hampshire; New Jersey; New Mexico; New York; North Carolina; North Dakota; Ohio; Oklahoma; Oregon; Pennsylvania; Rhode Island; South Carolina; South Dakota; Tennessee; Texas; Utah; Vermont; Virginia; Washington; West Virginia; Wisconsin; Wyoming. US Virgin Islands. British Virgin Islands."],
        BBOX[14.92,167.65,86.45,-40.73]],
    ID["EPSG",4269]]"""

    wkt = to_wkt(j, options=Options(format=WKT1))
    assert wkt == """GEOGCS["NAD83",
    DATUM["North American Datum 1983",
        SPHEROID["GRS 1980",6378137,298.257222101]],
    PRIMEM["Greenwich",0],
    UNIT["degree",0.0174532925199433],
    AXIS["Geodetic latitude (Lat)",NORTH],
    AXIS["Geodetic longitude (Lon)",EAST],
    AUTHORITY["EPSG","4269"]]"""


def test_dynamic_geog_crs_epsg_9990():
    j = {"$schema":"https://proj.org/schemas/v0.4/projjson.schema.json","type":"GeographicCRS","name":"ITRF2020","datum":{"type":"DynamicGeodeticReferenceFrame","name":"International Terrestrial Reference Frame 2020","frame_reference_epoch":2015,"ellipsoid":{"name":"GRS 1980","semi_major_axis":6378137,"inverse_flattening":298.257222101}},"coordinate_system":{"subtype":"ellipsoidal","axis":[{"name":"Geodetic latitude","abbreviation":"Lat","direction":"north","unit":"degree"},{"name":"Geodetic longitude","abbreviation":"Lon","direction":"east","unit":"degree"}]},"scope":"Geodesy.","area":"World.","bbox":{"south_latitude":-90,"west_longitude":-180,"north_latitude":90,"east_longitude":180},"id":{"authority":"EPSG","code":9990}}

    wkt = to_wkt(j)
    assert wkt == """GEOGCRS["ITRF2020",
    DYNAMIC[
        FRAMEEPOCH[2015]],
    DATUM["International Terrestrial Reference Frame 2020",
        ELLIPSOID["GRS 1980",6378137,298.257222101,
            LENGTHUNIT["metre",1]]],
    CS[ellipsoidal,2],
        AXIS["geodetic latitude (Lat)",north,
            ANGLEUNIT["degree",0.0174532925199433]],
        AXIS["geodetic longitude (Lon)",east,
            ANGLEUNIT["degree",0.0174532925199433]],
    USAGE[
        SCOPE["Geodesy."],
        AREA["World."],
        BBOX[-90,-180,90,180]],
    ID["EPSG",9990]]"""

    wkt = to_wkt(j, options=Options(format=WKT1))
    assert wkt == """GEOGCS["ITRF2020",
    DATUM["International Terrestrial Reference Frame 2020",
        SPHEROID["GRS 1980",6378137,298.257222101]],
    PRIMEM["Greenwich",0],
    UNIT["degree",0.0174532925199433],
    AXIS["Geodetic latitude (Lat)",NORTH],
    AXIS["Geodetic longitude (Lon)",EAST],
    AUTHORITY["EPSG","9990"]]"""


def test_proj_crs_epsg_32631():
    j = {"$schema": "https://proj.org/schemas/v0.4/projjson.schema.json", "type": "ProjectedCRS", "name": "WGS 84 / UTM zone 31N", "base_crs": {"name": "WGS 84", "datum_ensemble": {"name": "World Geodetic System 1984 ensemble", "members": [{"name": "World Geodetic System 1984 (Transit)", "id": {"authority": "EPSG", "code": 1166}}, {"name": "World Geodetic System 1984 (G730)", "id": {"authority": "EPSG", "code": 1152}}, {"name": "World Geodetic System 1984 (G873)", "id": {"authority": "EPSG", "code": 1153}}, {"name": "World Geodetic System 1984 (G1150)", "id": {"authority": "EPSG", "code": 1154}}, {"name": "World Geodetic System 1984 (G1674)", "id": {"authority": "EPSG", "code": 1155}}, {"name": "World Geodetic System 1984 (G1762)", "id": {"authority": "EPSG", "code": 1156}}, {"name": "World Geodetic System 1984 (G2139)", "id": {"authority": "EPSG", "code": 1309}}], "ellipsoid": {"name": "WGS 84", "semi_major_axis": 6378137, "inverse_flattening": 298.257223563}, "accuracy": "2.0", "id": {"authority": "EPSG", "code": 6326}}, "coordinate_system": {"subtype": "ellipsoidal", "axis": [{"name": "Geodetic latitude", "abbreviation": "Lat", "direction": "north", "unit": "degree"}, {"name": "Geodetic longitude", "abbreviation": "Lon", "direction": "east", "unit": "degree"}]}, "id": {"authority": "EPSG", "code": 4326}}, "conversion": {"name": "UTM zone 31N", "method": {
        "name": "Transverse Mercator", "id": {"authority": "EPSG", "code": 9807}}, "parameters": [{"name": "Latitude of natural origin", "value": 0, "unit": "degree", "id": {"authority": "EPSG", "code": 8801}}, {"name": "Longitude of natural origin", "value": 3, "unit": "degree", "id": {"authority": "EPSG", "code": 8802}}, {"name": "Scale factor at natural origin", "value": 0.9996, "unit": "unity", "id": {"authority": "EPSG", "code": 8805}}, {"name": "False easting", "value": 500000, "unit": "metre", "id": {"authority": "EPSG", "code": 8806}}, {"name": "False northing", "value": 0, "unit": "metre", "id": {"authority": "EPSG", "code": 8807}}]}, "coordinate_system": {"subtype": "Cartesian", "axis": [{"name": "Easting", "abbreviation": "E", "direction": "east", "unit": "metre"}, {"name": "Northing", "abbreviation": "N", "direction": "north", "unit": "metre"}]}, "scope": "Engineering survey, topographic mapping.", "area": "Between 0°E and 6°E, northern hemisphere between equator and 84°N, onshore and offshore. Algeria. Andorra. Belgium. Benin. Burkina Faso. Denmark - North Sea. France. Germany - North Sea. Ghana. Luxembourg. Mali. Netherlands. Niger. Nigeria. Norway. Spain. Togo. United Kingdom (UK) - North Sea.", "bbox": {"south_latitude": 0, "west_longitude": 0, "north_latitude": 84, "east_longitude": 6}, "id": {"authority": "EPSG", "code": 32631}}

    wkt = to_wkt(j)
    assert wkt == """PROJCRS["WGS 84 / UTM zone 31N",
    BASEGEOGCRS["WGS 84",
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
        ID["EPSG",4326]],
    CONVERSION["UTM zone 31N",
        METHOD["Transverse Mercator",
            ID["EPSG",9807]],
        PARAMETER["Latitude of natural origin",0,
            ANGLEUNIT["degree",0.0174532925199433],
            ID["EPSG",8801]],
        PARAMETER["Longitude of natural origin",3,
            ANGLEUNIT["degree",0.0174532925199433],
            ID["EPSG",8802]],
        PARAMETER["Scale factor at natural origin",0.9996,
            SCALEUNIT["unity",1],
            ID["EPSG",8805]],
        PARAMETER["False easting",500000,
            LENGTHUNIT["metre",1],
            ID["EPSG",8806]],
        PARAMETER["False northing",0,
            LENGTHUNIT["metre",1],
            ID["EPSG",8807]]],
    CS[Cartesian,2],
        AXIS["easting (E)",east,
            LENGTHUNIT["metre",1]],
        AXIS["northing (N)",north,
            LENGTHUNIT["metre",1]],
    USAGE[
        SCOPE["Engineering survey, topographic mapping."],
        AREA["Between 0°E and 6°E, northern hemisphere between equator and 84°N, onshore and offshore. Algeria. Andorra. Belgium. Benin. Burkina Faso. Denmark - North Sea. France. Germany - North Sea. Ghana. Luxembourg. Mali. Netherlands. Niger. Nigeria. Norway. Spain. Togo. United Kingdom (UK) - North Sea."],
        BBOX[0,0,84,6]],
    ID["EPSG",32631]]"""

    wkt = to_wkt(j, options=Options(format=WKT1))
    assert wkt == """PROJCS["WGS 84 / UTM zone 31N",
    GEOGCS["WGS 84",
        DATUM["World Geodetic System 1984",
            SPHEROID["WGS 84",6378137,298.257223563],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0],
        UNIT["degree",0.0174532925199433],
        AXIS["Geodetic latitude (Lat)",NORTH],
        AXIS["Geodetic longitude (Lon)",EAST],
        AUTHORITY["EPSG","4326"]],
    PROJECTION["Transverse Mercator"],
    PARAMETER["Latitude of natural origin",0],
    PARAMETER["Longitude of natural origin",3],
    PARAMETER["Scale factor at natural origin",0.9996],
    PARAMETER["False easting",500000],
    PARAMETER["False northing",0],
    UNIT["metre",1],
    AXIS["Easting (E)",EAST],
    AXIS["Northing (N)",NORTH],
    AUTHORITY["EPSG","32631"]]"""


def test_compound_crs_epsg_9707():

    j = {"$schema": "https://proj.org/schemas/v0.4/projjson.schema.json", "type": "CompoundCRS", "name": "WGS 84 + EGM96 height", "components": [{"type": "GeographicCRS", "name": "WGS 84", "datum_ensemble": {"name": "World Geodetic System 1984 ensemble", "members": [{"name": "World Geodetic System 1984 (Transit)", "id": {"authority": "EPSG", "code": 1166}}, {"name": "World Geodetic System 1984 (G730)", "id": {"authority": "EPSG", "code": 1152}}, {"name": "World Geodetic System 1984 (G873)", "id": {"authority": "EPSG", "code": 1153}}, {"name": "World Geodetic System 1984 (G1150)", "id": {"authority": "EPSG", "code": 1154}}, {"name": "World Geodetic System 1984 (G1674)", "id": {"authority": "EPSG", "code": 1155}}, {"name": "World Geodetic System 1984 (G1762)", "id": {"authority": "EPSG", "code": 1156}}, {"name": "World Geodetic System 1984 (G2139)", "id": {"authority": "EPSG", "code": 1309}}], "ellipsoid": {
        "name": "WGS 84", "semi_major_axis": 6378137, "inverse_flattening": 298.257223563}, "accuracy": "2.0", "id": {"authority": "EPSG", "code": 6326}}, "coordinate_system": {"subtype": "ellipsoidal", "axis": [{"name": "Geodetic latitude", "abbreviation": "Lat", "direction": "north", "unit": "degree"}, {"name": "Geodetic longitude", "abbreviation": "Lon", "direction": "east", "unit": "degree"}]}}, {"type": "VerticalCRS", "name": "EGM96 height", "datum": {"type": "VerticalReferenceFrame", "name": "EGM96 geoid"}, "coordinate_system": {"subtype": "vertical", "axis": [{"name": "Gravity-related height", "abbreviation": "H", "direction": "up", "unit": "metre"}]}}], "scope": "Spatial referencing.", "area": "World.", "bbox": {"south_latitude": -90, "west_longitude": -180, "north_latitude": 90, "east_longitude": 180}, "id": {"authority": "EPSG", "code": 9707}}

    wkt = to_wkt(j)
    assert wkt == """COMPOUNDCRS["WGS 84 + EGM96 height",
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
    ID["EPSG",9707]]"""

    wkt = to_wkt(j, options=Options(format=WKT1))
    assert wkt == """COMPD_CS["WGS 84 + EGM96 height",
    GEOGCS["WGS 84",
        DATUM["World Geodetic System 1984",
            SPHEROID["WGS 84",6378137,298.257223563],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0],
        UNIT["degree",0.0174532925199433],
        AXIS["Geodetic latitude (Lat)",NORTH],
        AXIS["Geodetic longitude (Lon)",EAST]],
    VERT_CS["EGM96 height",
        VERT_DATUM["EGM96 geoid",2005],
        UNIT["metre",1],
        AXIS["Gravity-related height (H)",UP]],
    AUTHORITY["EPSG","9707"]]"""


def test_vertical_crs_with_datum_ensemble_epsg_9451():

    j = {"$schema":"https://proj.org/schemas/v0.4/projjson.schema.json","type":"VerticalCRS","name":"BI height","datum_ensemble":{"name":"British Isles height ensemble","members":[{"name":"Malin Head","id":{"authority":"EPSG","code":5130}},{"name":"Belfast Lough","id":{"authority":"EPSG","code":5131}},{"name":"Ordnance Datum Newlyn","id":{"authority":"EPSG","code":5101}},{"name":"Ordnance Datum Newlyn (Offshore)","id":{"authority":"EPSG","code":1164}},{"name":"Ordnance Datum Newlyn (Orkney Isles)","id":{"authority":"EPSG","code":5138}},{"name":"Lerwick","id":{"authority":"EPSG","code":5140}},{"name":"Stornoway","id":{"authority":"EPSG","code":5144}},{"name":"Douglas","id":{"authority":"EPSG","code":5148}},{"name":"St. Marys","id":{"authority":"EPSG","code":5147}}],"accuracy":"0.4","id":{"authority":"EPSG","code":1288}},"coordinate_system":{"subtype":"vertical","axis":[{"name":"Gravity-related height","abbreviation":"H","direction":"up","unit":"metre"}]},"scope":"Spatial referencing.","area":"United Kingdom (UK) - offshore to boundary of UKCS within 49°45'N to 61°N and 9°W to 2°E; onshore Great Britain (England, Wales and Scotland) and Northern Ireland. Ireland onshore. Isle of Man onshore.","bbox":{"south_latitude":49.75,"west_longitude":-9,"north_latitude":61.01,"east_longitude":2.01},"id":{"authority":"EPSG","code":9451}}

    wkt = to_wkt(j)
    assert wkt == """VERTCRS["BI height",
    ENSEMBLE["British Isles height ensemble",
        MEMBER["Malin Head",
            ID["EPSG",5130]],
        MEMBER["Belfast Lough",
            ID["EPSG",5131]],
        MEMBER["Ordnance Datum Newlyn",
            ID["EPSG",5101]],
        MEMBER["Ordnance Datum Newlyn (Offshore)",
            ID["EPSG",1164]],
        MEMBER["Ordnance Datum Newlyn (Orkney Isles)",
            ID["EPSG",5138]],
        MEMBER["Lerwick",
            ID["EPSG",5140]],
        MEMBER["Stornoway",
            ID["EPSG",5144]],
        MEMBER["Douglas",
            ID["EPSG",5148]],
        MEMBER["St. Marys",
            ID["EPSG",5147]],
        ENSEMBLEACCURACY[0.4],
        ID["EPSG",1288]],
    CS[vertical,1],
        AXIS["gravity-related height (H)",up,
            LENGTHUNIT["metre",1]],
    USAGE[
        SCOPE["Spatial referencing."],
        AREA["United Kingdom (UK) - offshore to boundary of UKCS within 49°45'N to 61°N and 9°W to 2°E; onshore Great Britain (England, Wales and Scotland) and Northern Ireland. Ireland onshore. Isle of Man onshore."],
        BBOX[49.75,-9,61.01,2.01]],
    ID["EPSG",9451]]"""

    wkt = to_wkt(j, options=Options(format=WKT1))
    assert wkt == """VERT_CS["BI height",
    VERT_DATUM["British Isles height ensemble",2005,
        AUTHORITY["EPSG","1288"]],
    UNIT["metre",1],
    AXIS["Gravity-related height (H)",UP],
    AUTHORITY["EPSG","9451"]]"""


def test_dynamic_vertical_crs_epsg_5613():

    j = {"$schema":"https://proj.org/schemas/v0.4/projjson.schema.json","type":"VerticalCRS","name":"RH2000 height","datum":{"type":"DynamicVerticalReferenceFrame","name":"Rikets hojdsystem 2000","frame_reference_epoch":2000},"coordinate_system":{"subtype":"vertical","axis":[{"name":"Gravity-related height","abbreviation":"H","direction":"up","unit":"metre"}]},"scope":"Geodesy, engineering survey.","area":"Sweden - onshore.","bbox":{"south_latitude":55.28,"west_longitude":10.93,"north_latitude":69.07,"east_longitude":24.17},"id":{"authority":"EPSG","code":5613}}

    wkt = to_wkt(j)
    assert wkt == """VERTCRS["RH2000 height",
    DYNAMIC[
        FRAMEEPOCH[2000]],
    VDATUM["Rikets hojdsystem 2000"],
    CS[vertical,1],
        AXIS["gravity-related height (H)",up,
            LENGTHUNIT["metre",1]],
    USAGE[
        SCOPE["Geodesy, engineering survey."],
        AREA["Sweden - onshore."],
        BBOX[55.28,10.93,69.07,24.17]],
    ID["EPSG",5613]]"""

    wkt = to_wkt(j, options=Options(format=WKT1))
    assert wkt == """VERT_CS["RH2000 height",
    VERT_DATUM["Rikets hojdsystem 2000",2005],
    UNIT["metre",1],
    AXIS["Gravity-related height (H)",UP],
    AUTHORITY["EPSG","5613"]]"""
