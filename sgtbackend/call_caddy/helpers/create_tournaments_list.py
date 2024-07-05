from datetime import datetime
from models import Tournament

def create_tournament_ids_list(self):
        current_year = datetime.now().year
        tournament_list = Tournament.objects.filter(year=str(current_year)).values_list('source_id', flat=True)
        return list(tournament_list)