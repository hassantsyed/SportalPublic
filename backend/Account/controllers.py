from .models import Account

def createAccount(GID):
    try:
        a = Account(GID=GID)
        a.save()
        return a
    except Exception:
        return 404

def getAccount(GID):
    a = Account.objects.filter(GID=GID).first()
    if a is None:
        a = createAccount(GID)
    return a.pk