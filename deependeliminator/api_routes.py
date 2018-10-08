from application import rebar
from deependeliminator.schemas import FantasyTeamListSchema


registry = rebar.create_handler_registry(prefix='/api/v1')

@registry.handles(
    rule='/standings',
    method='GET',
    marshal_schema=FantasyTeamListSchema()
)
def get_standings_json():
    from deependeliminator.standings import get_standings_list
    return get_standings_list()
