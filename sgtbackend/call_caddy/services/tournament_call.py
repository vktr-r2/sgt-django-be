from datetime import datetime
from .rapid_api_wrapper import RapidApiWrapperService

class TournamentCallService:

    def __init__(self):
        self.api_wrapper = RapidApiWrapperService()

    # Calls the tour schedule endpoint to GET tourney data for the season
    def get_tournament(self, org_id, tourn_id):
        current_year = str(datetime.now().year)
        params = {"orgID": org_id, "tourn_id": tourn_id, "year": current_year}
        return self.api_wrapper.make_request("tournament", params=params)