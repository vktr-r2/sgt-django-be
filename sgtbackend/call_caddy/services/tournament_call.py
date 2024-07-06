from datetime import datetime
from call_caddy.services.rapid_api_wrapper import RapidApiWrapperService


class TournamentCallService:

    def __init__(self):
        self.api_wrapper = RapidApiWrapperService()

    # Calls the tournament endpoint to GET data for a specific tourney
    def get_tournament(self, org_id, tourn_id):
        current_year = str(datetime.now().year)
        params = {"orgID": org_id, "tourn_id": tourn_id, "year": current_year}
        return self.api_wrapper.make_request("tournament", params=params)
