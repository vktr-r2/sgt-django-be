from datetime import datetime
from .rapid_api_wrapper import RapidApiWrapperService

class ScheduleCallService:

    def __init__(self):
        self.api_wrapper = RapidApiWrapperService()

    def get_schedule_for_org(self, org_id):
        current_year = str(datetime.now().year)
        params = f"orgID={org_id}&year={current_year}"
        return self.api_wrapper.make_request("schedule", params=params)