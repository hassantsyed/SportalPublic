from .models import Participant

def create(name):
    try:
        p = Participant(name=name)
        p.save()
        return 200
    except Exception:
        return 400