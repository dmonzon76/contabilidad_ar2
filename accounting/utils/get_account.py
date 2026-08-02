from accounting.models.account import Account

def get_account(code):
    return Account.objects.get(code=code)
