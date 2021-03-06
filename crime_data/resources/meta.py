from flask import jsonify
from flask.ext.cachecontrol import cache_for
from webargs.flaskparser import use_args
from marshmallow import fields, Schema
from crime_data.common import cdemodels, marshmallow_schemas
from crime_data.common.marshmallow_schemas import ma
from crime_data.common.base import CdeResource


class FilterColumnSchema(Schema):
    """The schema for a specific filter that can be used"""

    name = fields.String()
    type = fields.String()
    format = fields.String()
    maxLength = fields.Integer()


class MetaDetailResponseSchema(Schema):
    """The format for responses from the meta API endpoint"""

    endpoint = fields.String()
    filters = ma.Nested(FilterColumnSchema, many=True)


FAMILIES = {
    'incidents': cdemodels.IncidentTableFamily(),
    'incidents/count': cdemodels.IncidentCountTableFamily(),
    'arson': cdemodels.ArsonTableFamily(),
    'arrests/race': cdemodels.ArrestsByRaceTableFamily(),
    'arrests/ethnicity': cdemodels.ArrestsByEthnicityTableFamily(),
    'arrests/age_sex': cdemodels.ArrestsByAgeSexTableFamily()
}


class MetaDetail(CdeResource):
    """
    The meta API endpoint returns information about the API endpoint
    that follows it. Currently this is just the allowed filters for
    the endpoint.
    """

    @cache_for(hours=1)
    def get(self, endpoint):
        endpoint = endpoint.rstrip('/')
        out = {
            'endpoint': endpoint,
            'filters': FAMILIES[endpoint].filter_columns
        }
        return jsonify(out)
