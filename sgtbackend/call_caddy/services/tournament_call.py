from datetime import datetime
import logging
from call_caddy.services.rapid_api_wrapper import RapidApiWrapperService

logger = logging.getLogger("call_caddy")

class TournamentCallService:

    def __init__(self):
        self.api_wrapper = RapidApiWrapperService()

    # Calls the tournament endpoint to GET data for a specific tourney
    def get_tournament(self, org_id, tourn_id):
        current_year = str(datetime.now().year)
        params = {"orgId": org_id, "tournId": tourn_id, "year": current_year}
        return self.api_wrapper.make_request("tournament", params=params)
