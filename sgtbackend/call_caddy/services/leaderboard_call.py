from datetime import datetime
from .rapid_api_wrapper import RapidApiWrapperService

class LeaderboardCallService:

    def __init__(self):
        self.api_wrapper = RapidApiWrapperService()

    # Calls the tour schedule endpoint to GET leaderboard data for the tourney
    def get_leaderboard(self, org_id, tourn_id):
        current_year = str(datetime.now().year)
        params = {"orgID": org_id, "tourn_id": tourn_id, "year": current_year}
        return self.api_wrapper.make_request("leaderboard", params=params)