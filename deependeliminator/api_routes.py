from application import rebar
from deependeliminator.schemas import FantasyTeamListSchema
from deependeliminator.standings import get_standings_list


registry = rebar.create_handler_registry(prefix='/api/v1')

@registry.handles(
    rule='/standings',
    method='GET',
    marshal_schema=FantasyTeamListSchema()
)
def get_standings_json():
    return get_standings_list()
