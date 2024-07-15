from django.core.management.base import BaseCommand
from datetime import datetime
import logging
from call_caddy.services.tournament_call import TournamentCallService
from call_caddy.services.tournament_data_processor import TournamentDataProcessor
from call_caddy.serializers.tournament import TournamentSerializer

logger = logging.getLogger("call_caddy")

class Command(BaseCommand):
    help = "(Args: org_id, tournament_id) Command calls /tournament endpoint, validates response, and inserts data into DB"

    def add_arguments(self, parser):
        parser.add_argument("tournament_id", type=str, help="Tournament ID")

    def handle(self, *args, **kwargs):
        tournament_id = kwargs["tournament_id"]

        service = TournamentCallService()
        response = service.get_tournament("1", tournament_id)

        if not response:
            self.stdout.write(self.style.ERROR("No data received from TournamnentCallService."))
            return
        
        self.stdout.write("Validating the schedule response data...")

        # Instantiate serializer
        serializer = TournamentSerializer(data=response)


        # Validate data
        if serializer.is_valid():
            # Instantiate data processor
            processed_data = TournamentDataProcessor(response)
            processed_data.process_tournament_data()
            self.stdout.write("Tournament imported")
        else:
            self.stdout.write(self.style.ERROR(f"Error in /tournament response data"))