import os
import sys
import django

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User
from company.models import CompanyUser

username = "daniel"
user = User.objects.filter(username=username).first()
if not user:
    print("NOUSER")
else:
    print("USER:", user.username, "id", user.id)
    qs = CompanyUser.objects.filter(user=user, is_active=True).select_related("company")
    print("COUNT:", qs.count())
    for cu in qs:
        print(
            "COMPANY_ID:",
            cu.company_id,
            "COMPANY:",
            getattr(cu.company, "name", None),
            "ROLE:",
            cu.role,
        )
