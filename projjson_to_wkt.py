#!/usr/bin/env python
# SPDX-License-Identifier: MIT
# Copyright 2022, Even Rouault

WKT1 = "WKT1"
WKT2_2019 = "WKT2:2019"

DEG_TO_RAD = 0.0174532925199433


class Options:
    def __init__(self, format=WKT2_2019, single_line=False):
        if format not in (WKT1, WKT2_2019,):
            raise Exception("Unsupported WKT format")
        self.format = format
        self.single_line = single_line
        self.indentation_by_level = "" if single_line else " " * 4


class PROJJSONToWKT:
    def __init__(self, options=Options()):
        self.options = options
        self.wkt = ""
        self.stack_has_values = []
        self.indentation = ""

    def quote_str(self, x):
        return "\"" + x.replace("\"", "\"\"") + "\""

    def float_to_str(self, v):
        return "%.15g" % v

    def get_value_unit(self, v, default_unit):

        if isinstance(v, dict):
            val = v["value"]
            unit = v["unit"]
            if unit == "metre":
                return val, unit, 1.0
            elif unit == "degree":
                return val, unit, DEG_TO_RAD
            conv_factor = unit["conversion_factor"]
            return val, unit["name"], conv_factor
        return v, default_unit, (DEG_TO_RAD if default_unit == "degree" else 1.0)

    def start_node(self, name):
        if self.stack_has_values:
            if self.stack_has_values[-1]:
                self.wkt += ","
            else:
                self.stack_has_values[-1] = True
            if not self.options.single_line:
                self.wkt += "\n"
        self.wkt += self.indentation
        self.wkt += name
        self.wkt += "["
        self.stack_has_values.append(False)
        self.indentation += self.options.indentation_by_level

    def end_node(self):
        self.wkt += "]"
        self.end_pseudo_node()

    def start_pseudo_node(self):
        self.stack_has_values.append(True)
        self.indentation += self.options.indentation_by_level

    def end_pseudo_node(self):
        self.stack_has_values.pop()
        self.indentation = self.indentation[0:-
                                            len(self.options.indentation_by_level)]

    def add_quoted_string(self, s):
        if self.stack_has_values[-1]:
            self.wkt += ","
        self.wkt += self.quote_str(s)
        self.stack_has_values[-1] = True

    def add(self, s):
        if self.stack_has_values[-1]:
            self.wkt += ","
        self.wkt += s
        self.stack_has_values[-1] = True

    def id_to_wkt(self, id):
        if self.options.format == WKT1:
            self.start_node("AUTHORITY")
            self.add_quoted_string(id["authority"])
            code = id["code"]
            self.add_quoted_string(str(code))
            self.end_node()
        else:
            self.start_node("ID")
            self.add_quoted_string(id["authority"])
            code = id["code"]
            if isinstance(code, int):
                self.add(str(code))
            else:
                self.add_quoted_string(code)
            self.end_node()

    def object_usage_to_wkt(self, obj):
        if self.options.format != WKT1:
            scope = obj.get("scope", None)
            area = obj.get("area", None)
            bbox = obj.get("bbox", None)
            if scope or area or bbox:
                self.start_node("USAGE")
                if scope:
                    self.start_node("SCOPE")
                    self.add_quoted_string(scope)
                    self.end_node()
                if area:
                    self.start_node("AREA")
                    self.add_quoted_string(area)
                    self.end_node()
                if bbox:
                    self.start_node("BBOX")
                    self.add(self.float_to_str(bbox["south_latitude"]))
                    self.add(self.float_to_str(bbox["west_longitude"]))
                    self.add(self.float_to_str(bbox["north_latitude"]))
                    self.add(self.float_to_str(bbox["east_longitude"]))
                    self.end_node()
                self.end_node()
            else:
                usages = obj.get("usages", None)
                if usages:
                    for usage in usages:
                        self.object_usage_to_wkt(usage)

        id = obj.get("id", None)
        if id:
            self.id_to_wkt(id)
        elif self.options.format != WKT1:
            ids = obj.get("ids", None)
            if ids:
                for id in ids:
                    self.id_to_wkt(id)

        if self.options.format != WKT1:
            remarks = obj.get("remarks", None)
            if remarks:
                self.start_node("REMARK")
                self.add_quoted_string(remarks)
                self.end_node()

    def ellipsoid_to_wkt(self, ellipsoid):

        self.start_node("SPHEROID" if self.options.format ==
                        WKT1 else "ELLIPSOID")
        self.add_quoted_string(ellipsoid["name"])
        semi_major_axis = ellipsoid["semi_major_axis"]
        a, unit, conv_factor = self.get_value_unit(semi_major_axis, "metre")
        self.add(self.float_to_str(a))

        semi_minor_axis = ellipsoid.get("semi_minor_axis", None)
        inverse_flattening = ellipsoid.get("inverse_flattening", None)
        if inverse_flattening:
            rf, unit2, conv_factor2 = self.get_value_unit(
                inverse_flattening, None)
            self.add(self.float_to_str(rf))
        elif semi_minor_axis:
            b, unit2, conv_factor2 = self.get_value_unit(
                semi_minor_axis, "metre")
            assert unit == unit2, (unit, unit2)
            assert conv_factor == conv_factor2
            rf = a / (a - b)
            self.add(self.float_to_str(rf))
        else:
            raise Exception(
                "semi_minor_axis or inverse_flattening missing in ellipsoid")

        if conv_factor != 1 and self.options.format == WKT1:
            raise Exception('conv_factor != 1 unsupported for WKT1')
        if self.options.format != WKT1:
            self.start_node("LENGTHUNIT")
            self.add_quoted_string(unit)
            self.add(self.float_to_str(conv_factor))
            self.end_node()
        self.object_usage_to_wkt(ellipsoid)
        self.end_node()

    def prime_meridian_to_wkt(self, pm):

        self.start_node("PRIMEM")
        self.add_quoted_string(pm["name"])
        longitude = pm["longitude"]
        longitude, unit, conv_factor = self.get_value_unit(longitude, "degree")
        self.add(self.float_to_str(longitude))
        if self.options.format != WKT1:
            self.unit_to_wkt(
                {"type": "AngularUnit", "name": unit, "conversion_factor": conv_factor})
        self.object_usage_to_wkt(pm)
        self.end_node()

    def datum_to_wkt(self, datum):

        if self.options.format != WKT1:
            type = datum.get("type", None)
            if type and type == "DynamicGeodeticReferenceFrame":
                self.start_node("DYNAMIC")
                self.start_node("FRAMEEPOCH")
                self.add(str(datum["frame_reference_epoch"]))
                self.end_node()
                self.end_node()
        self.start_node("DATUM")
        self.add_quoted_string(datum["name"])
        self.ellipsoid_to_wkt(datum["ellipsoid"])
        self.object_usage_to_wkt(datum)
        self.end_node()

    def ensemble_member_to_wkt(self, member):

        self.start_node("MEMBER")
        self.add_quoted_string(member["name"])
        self.object_usage_to_wkt(member)
        self.end_node()

    def datum_ensemble_to_wkt(self, ensemble):

        if self.options.format == WKT1:
            self.start_node("DATUM")
            self.add_quoted_string(ensemble["name"].replace(" ensemble", ""))
            self.ellipsoid_to_wkt(ensemble["ellipsoid"])
            self.object_usage_to_wkt(ensemble)
            self.end_node()
        else:
            self.start_node("ENSEMBLE")
            self.add_quoted_string(ensemble["name"])
            members = ensemble["members"]
            for member in members:
                self.ensemble_member_to_wkt(member)
            self.ellipsoid_to_wkt(ensemble["ellipsoid"])
            accuracy = ensemble.get("accuracy", None)
            if accuracy:
                self.start_node("ENSEMBLEACCURACY")
                self.add(accuracy)
                self.end_node()
            self.object_usage_to_wkt(ensemble)
            self.end_node()

    def unit_to_wkt(self, unit):

        if unit == "degree":
            unit = {"name": unit, "conversion_factor": DEG_TO_RAD,
                    "type": "AngularUnit"}
        elif unit == "metre":
            unit = {"name": unit, "conversion_factor": 1.0, "type": "LinearUnit"}
        elif unit == "unity":
            unit = {"name": unit, "conversion_factor": 1.0, "type": "ScaleUnit"}

        type = unit["type"]
        name = unit["name"]
        conv_factor = unit["conversion_factor"]
        if self.options.format == WKT1:
            keyword = "UNIT"
        elif type == "AngularUnit":
            keyword = "ANGLEUNIT"
        elif type == "LinearUnit":
            keyword = "LENGTHUNIT"
        elif type == "ScaleUnit":
            keyword = "SCALEUNIT"
        elif type == "TimeUnit":
            keyword = "TIMEUNIT"
        elif type == "ParametricUnit":
            keyword = "PARAMETRICUNIT"
        elif type == "Unit":
            keyword = "UNIT"
        else:
            raise Exception("unexpected unit type")
        self.start_node(keyword)
        self.add_quoted_string(name)
        self.add(self.float_to_str(conv_factor))
        self.object_usage_to_wkt(unit)
        self.end_node()

    def meridian_to_wkt(self, pm):

        self.start_node("MERIDIAN")
        longitude = pm["longitude"]
        longitude, unit, conv_factor = self.get_value_unit(longitude, "degree")
        self.add(self.float_to_str(longitude))
        if self.options.format != WKT1:
            self.unit_to_wkt(
                {"type": "AngularUnit", "name": unit, "conversion_factor": conv_factor})
        self.object_usage_to_wkt(pm)
        self.end_node()

    def axis_to_wkt(self, axis):

        self.start_node("AXIS")
        name = axis["name"]
        if self.options.format != WKT1:
            name = name[0].lower() + name[1:]
        self.add_quoted_string(
            name + " (" + axis["abbreviation"] + ")")
        direction = axis["direction"]
        if self.options.format != WKT1:
            self.add(direction)
        else:
            direction = direction.upper()
            if direction not in ('EAST', 'NORTH', 'WEST', 'SOUTH', "UP", "DOWN"):
                direction = 'OTHER'
            self.add(direction)
        meridian = axis.get("meridian", None)
        if meridian and self.options.format != WKT1:
            self.meridian_to_wkt(meridian)
        if self.options.format != WKT1:
            self.unit_to_wkt(axis["unit"])
        self.end_node()

    def coordinate_system_to_wkt(self, cs):

        if self.options.format != WKT1:
            self.start_node("CS")
            self.add(cs["subtype"])  # unquoted!
        axis_list = cs["axis"]
        if self.options.format != WKT1:
            self.add(str(len(axis_list)))
            self.end_node()
            self.start_pseudo_node()
        else:
            self.unit_to_wkt(axis_list[0]["unit"])
        for axis in axis_list:
            self.axis_to_wkt(axis)
        if self.options.format != WKT1:
            self.end_pseudo_node()

    def geodetic_crs_to_wkt(self, crs, keyword=None, emit_cs=True):

        if keyword is None:
            type = crs["type"]
            if self.options.format == WKT1:
                keyword = "GEOGCS" if type == "GeographicCRS" else "GEOCCS"
            else:
                keyword = "GEOGCRS" if type == "GeographicCRS" else "GEODCRS"
        self.start_node(keyword)
        self.add_quoted_string(crs["name"])
        datum = crs.get("datum", None)
        if datum:
            self.datum_to_wkt(datum)
            pm = datum.get("prime_meridian", None)
            if pm:
                self.prime_meridian_to_wkt(pm)
            elif self.options.format == WKT1:
                self.prime_meridian_to_wkt(
                    {"name": "Greenwich", "longitude": 0})
        else:
            datum_ensemble = crs["datum_ensemble"]
            self.datum_ensemble_to_wkt(datum_ensemble)
            if self.options.format == WKT1:
                self.prime_meridian_to_wkt(
                    {"name": "Greenwich", "longitude": 0})
        if emit_cs:
            self.coordinate_system_to_wkt(crs["coordinate_system"])
        self.object_usage_to_wkt(crs)
        self.end_node()

    def derived_geodetic_crs_to_wkt(self, crs):

        if self.options.format == WKT1:
            raise Exception("%s unsupported in WKT1" % crs["type"])

        self.start_node("GEODCRS")
        self.add_quoted_string(crs["name"])
        base_crs = crs["base_crs"]
        base_keyword = "BASEGEOGCRS" if base_crs["type"] == "GeographicCRS" else "BASEGEODCRS"
        self.geodetic_crs_to_wkt(base_crs, keyword=base_keyword, emit_cs=False)
        self.conversion_to_wkt(crs["conversion"], keyword="DERIVINGCONVERSION")
        self.coordinate_system_to_wkt(crs["coordinate_system"])
        self.object_usage_to_wkt(crs)
        self.end_node()

    def method_to_wkt(self, method):

        self.start_node("METHOD")
        self.add_quoted_string(method["name"])
        self.object_usage_to_wkt(method)
        self.end_node()

    def parameter_to_wkt(self, parameter):

        value = parameter["value"]
        if isinstance(value, str):
            self.start_node("PARAMETERFILE")
            self.add_quoted_string(parameter["name"])
            self.add_quoted_string(value)
            self.object_usage_to_wkt(parameter)
            self.end_node()
        else:
            self.start_node("PARAMETER")
            self.add_quoted_string(parameter["name"])
            self.add(self.float_to_str(value))
            if self.options.format != WKT1:
                self.unit_to_wkt(parameter["unit"])
                self.object_usage_to_wkt(parameter)
            self.end_node()

    def conversion_to_wkt(self, conversion, keyword="CONVERSION"):

        if self.options.format != WKT1:
            self.start_node(keyword)
            self.add_quoted_string(conversion["name"])
            self.method_to_wkt(conversion["method"])
            parameters = conversion.get("parameters", None)
            if parameters:
                for parameter in parameters:
                    self.parameter_to_wkt(parameter)
            self.object_usage_to_wkt(conversion)
            self.end_node()
        else:
            self.start_node("PROJECTION")
            self.add_quoted_string(conversion["method"]["name"])
            self.end_node()
            parameters = conversion.get("parameters", None)
            if parameters:
                for parameter in parameters:
                    self.parameter_to_wkt(parameter)

    def projected_crs_to_wkt(self, crs):

        self.start_node("PROJCRS" if self.options.format != WKT1 else "PROJCS")
        self.add_quoted_string(crs["name"])
        base_crs = crs["base_crs"]
        if base_crs["coordinate_system"]["subtype"] == "ellipsoidal":
            base_keyword = "BASEGEOGCRS" if self.options.format != WKT1 else "GEOGCS"
        else:
            base_keyword = "BASEGEODCRS" if self.options.format != WKT1 else "GEOCCS"
        self.geodetic_crs_to_wkt(
            base_crs, keyword=base_keyword, emit_cs=(self.options.format == WKT1))
        self.conversion_to_wkt(crs["conversion"])
        self.coordinate_system_to_wkt(crs["coordinate_system"])
        self.object_usage_to_wkt(crs)
        self.end_node()

    def vertical_datum_to_wkt(self, datum):

        if self.options.format != WKT1:
            type = datum.get("type", None)
            if type and type == "DynamicVerticalReferenceFrame":
                self.start_node("DYNAMIC")
                self.start_node("FRAMEEPOCH")
                self.add(str(datum["frame_reference_epoch"]))
                self.end_node()
                self.end_node()

        self.start_node("VDATUM" if self.options.format !=
                        WKT1 else "VERT_DATUM")
        self.add_quoted_string(datum["name"])
        if self.options.format == WKT1:
            self.add("2005")
        self.object_usage_to_wkt(datum)
        self.end_node()

    def vertical_datum_ensemble_to_wkt(self, ensemble):

        if self.options.format == WKT1:
            self.start_node("VERT_DATUM")
            self.add_quoted_string(ensemble["name"])
            self.add("2005")
            self.object_usage_to_wkt(ensemble)
            self.end_node()
        else:
            self.start_node("ENSEMBLE")
            self.add_quoted_string(ensemble["name"])
            members = ensemble["members"]
            for member in members:
                self.ensemble_member_to_wkt(member)
            accuracy = ensemble.get("accuracy", None)
            if accuracy:
                self.start_node("ENSEMBLEACCURACY")
                self.add(accuracy)
                self.end_node()
            self.object_usage_to_wkt(ensemble)
            self.end_node()

    def vertical_crs_to_wkt(self, crs):

        self.start_node("VERTCRS" if self.options.format !=
                        WKT1 else "VERT_CS")
        self.add_quoted_string(crs["name"])
        datum = crs.get("datum", None)
        if datum:
            self.vertical_datum_to_wkt(datum)
        else:
            datum_ensemble = crs["datum_ensemble"]
            self.vertical_datum_ensemble_to_wkt(datum_ensemble)
        self.coordinate_system_to_wkt(crs["coordinate_system"])
        self.object_usage_to_wkt(crs)
        self.end_node()

    def compound_crs_to_wkt(self, crs):

        self.start_node("COMPOUNDCRS" if self.options.format !=
                        WKT1 else "COMPD_CS")
        self.add_quoted_string(crs["name"])
        components = crs["components"]
        for component in components:
            self.to_wkt(component)
        self.object_usage_to_wkt(crs)
        self.end_node()

    def abridged_transformation_to_wkt(self, transf):

        self.start_node("ABRIDGEDTRANSFORMATION")
        self.add_quoted_string(transf["name"])
        self.method_to_wkt(transf["method"])
        parameters = transf["parameters"]
        for parameter in parameters:
            self.parameter_to_wkt(parameter)
        self.object_usage_to_wkt(transf)
        self.end_node()

    def bound_crs_to_wkt(self, crs):

        if self.options.format == WKT1:
            raise Exception("BoundCRS unsupported in WKT1")

        self.start_node("BOUNDCRS")
        self.start_node("SOURCECRS")
        self.to_wkt(crs["source_crs"])
        self.end_node()
        self.start_node("TARGETCRS")
        self.to_wkt(crs["target_crs"])
        self.end_node()
        self.abridged_transformation_to_wkt(crs["transformation"])
        self.end_node()

    def to_wkt(self, projjson):

        type = projjson["type"]
        if type in ("GeodeticCRS", "GeographicCRS"):
            self.geodetic_crs_to_wkt(projjson)
        elif type in ("DerivedGeodeticCRS", "DerivedGeographicCRS"):
            self.derived_geodetic_crs_to_wkt(projjson)
        elif type == "ProjectedCRS":
            self.projected_crs_to_wkt(projjson)
        elif type == "VerticalCRS":
            self.vertical_crs_to_wkt(projjson)
        elif type == "CompoundCRS":
            self.compound_crs_to_wkt(projjson)
        elif type == "BoundCRS":
            self.bound_crs_to_wkt(projjson)
        else:
            raise Exception("Unsupported object type: %s" % type)

        return self.wkt


def to_wkt(projjson, options=Options()):
    """ Convert a PROJJSON dictionary into a WKT string """
    return PROJJSONToWKT(options).to_wkt(projjson)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description='Convert a PROJJSON string into a WKT string.')
    parser.add_argument('projjson',
                        help='PROJJSON string')
    parser.add_argument('--format', default=WKT2_2019,
                        help='WKT format', choices=(WKT2_2019, WKT1))
    parser.add_argument('--single-line', action='store_true',
                        help='Whether to output without indentation')
    args = parser.parse_args()

    projjson = json.loads(args.projjson)
    options = Options(format=args.format, single_line=args.single_line)
    print(to_wkt(projjson, options=options))
