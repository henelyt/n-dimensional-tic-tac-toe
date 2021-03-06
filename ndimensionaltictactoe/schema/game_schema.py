from marshmallow import Schema, fields


class MoveSchema(Schema):
    x = fields.Integer()
    y = fields.Integer()


class MarkSchema(Schema):
    x = fields.Integer()
    y = fields.Integer()
    value = fields.Integer()


class PlayerSchema(Schema):
    key = fields.UUID()
    name = fields.String()
    winner = fields.Boolean()


class LobbySchema(Schema):
    lobby = fields.Nested(PlayerSchema, many=True)


class PlayerSummarySchema(Schema):
    name = fields.String()


class GameSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Integer()
    size_y = fields.Integer()
    player_x = fields.Nested(PlayerSchema)
    player_o = fields.Nested(PlayerSchema)
    cells = fields.Nested(MarkSchema, many=True)
    winning_length = fields.Integer()
    state = fields.Integer()
    winner = fields.Boolean()


class GameSummarySchema(Schema):
    name = fields.String()
    key = fields.UUID()
    size_x = fields.Integer()
    size_y = fields.Integer()
    winning_length = fields.Integer()
    player_x = fields.Nested(PlayerSummarySchema)
    player_o = fields.Nested(PlayerSummarySchema)


class RoundSchema(Schema):
    winner_points = fields.Integer()
    x_size = fields.Integer()
    y_size = fields.Integer()
    winning_length = fields.Integer()
    winners = fields.Nested(fields.UUID, many=True)
    games = fields.Nested(GameSchema, many=True)


class TournamentSchema(Schema):
    name = fields.String()
    key = fields.UUID()
    rounds = fields.Nested(RoundSchema, many=True)
    tournament_open = fields.Boolean()
