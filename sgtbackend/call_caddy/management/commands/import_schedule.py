from django.core.management.base import BaseCommand
from call_caddy.services.schedule_call import ScheduleCallService
from call_caddy.services.schedule_data_processor import ScheduleDataProcessor
from call_caddy.serializers.schedule import ScheduleSerializer

class Command(BaseCommand):
    help = "Calls /schedule endpoint, serializer response, and inserts data into DB"

    def handle(self, *args, **kwargs):
        
        # Call /schedule endpoint
        service = ScheduleCallService()
        response = service.get_schedule("1")

        if not response:
            self.stdout.write(self.style.ERROR("No data received from ScheduleCallService."))
            return

        # Process the response with ScheduleSerializerr
        self.stdout.write("Serializing the response data...")
        
        # Instantiate serializer
        serializer = ScheduleSerializer(data=response)

        # Validate data
        if serializer.is_valid():
            # Instantiate data processor
            processed_data = ScheduleDataProcessor(serializer.validated_data)
            # Map and save data
            processed_data.process_schedule_data()
        else:
            self.stdout.write(self.style.ERROR(f"Error in response data: {serializer.errors}"))