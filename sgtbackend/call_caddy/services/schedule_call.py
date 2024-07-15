from datetime import datetime
import logging
from call_caddy.services.rapid_api_wrapper import RapidApiWrapperService

logger = logging.getLogger("call_caddy")

class ScheduleCallService:

    def __init__(self):
        self.api_wrapper = RapidApiWrapperService()

    # Calls the tour schedule endpoint to GET tourney data for the season
    def get_schedule(self, org_id):
        current_year = str(datetime.now().year)
        params = {"orgID": org_id, "year": current_year}
        return self.api_wrapper.make_request("schedule", params=params)
