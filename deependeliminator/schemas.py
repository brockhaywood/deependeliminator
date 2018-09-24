from flask_rebar.validation import ResponseSchema
from marshmallow import fields, pre_dump


class FantasyTeamSchema(ResponseSchema):
    name = fields.String(required=True)
    points = fields.Number(required=True)


class FantasyTeamListSchema(ResponseSchema):
    data = fields.Nested(FantasyTeamSchema, many=True)

    @pre_dump
    def envelope_in_data(self, data):
        return {'data': data}