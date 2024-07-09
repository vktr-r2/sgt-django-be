from django.core.management.base import BaseCommand
from call_caddy.services.schedule_call import ScheduleCallService
from call_caddy.serializers.schedule import ScheduleSerializer

class Command(BaseCommand):
    help = "Calls /schedule endpoint, serializer response, and inserts data into DB"

    def handle(self, *args, **kwargs):
        
        # Assuming ScheduleCallService returns a response that needs to be serialized
        service = ScheduleCallService()
        response = service.get_schedule("1")

        if not response:
            self.stdout.write(self.style.ERROR("No data received from ScheduleCallService."))
            return

        # Process the response with ScheduleSerializerr
        self.stdout.write("Serializing the response data...")
        
        serializer = ScheduleSerializer()
        serializer.map_schedule_data(response)
        
        """if serializer.is_valid():
            self.stdout.write(self.style.SUCCESS("Data is valid."))
            # You can now work with the validated data or save it to the database
            serializer.save()
        else:
            self.stdout.write(self.style.ERROR(f"Invalid data: {serializer.errors}"))"""