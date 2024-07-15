from django.core.management.base import BaseCommand
from call_caddy.services.schedule_call import ScheduleCallService
from call_caddy.services.schedule_data_processor import ScheduleDataProcessor
from call_caddy.serializers.schedule import ScheduleSerializer

class Command(BaseCommand):
    help = "(Args: org_id) Command calls /schedule endpoint, validates response, and inserts data into DB"

    def handle(self, *args, **kwargs):
        
        # Call /schedule endpoint
        service = ScheduleCallService()
        response = service.get_schedule("1")

        if not response:
            self.stdout.write(self.style.ERROR("No data received from ScheduleCallService."))
            return

        self.stdout.write("Validating the schedule response data...")
        
        # Instantiate serializer
        serializer = ScheduleSerializer(data=response)

        # Validate data
        if serializer.is_valid():
            # Instantiate data processor
            processed_data = ScheduleDataProcessor(serializer.validated_data)
            # Map and save data
            processed_data.process_schedule_data()
            self.stdout.write("Schedule imported")
        else:
            self.stdout.write(self.style.ERROR(f"Error in /schedule response data: {serializer.errors}"))