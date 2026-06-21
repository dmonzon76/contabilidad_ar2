from django.http import JsonResponse
from django.db.models import Q
from fiscal.models import AFIPActivity

def afip_search(request):
    q = request.GET.get("q", "").strip()

    if not q:
        return JsonResponse([], safe=False)

    results = (
        AFIPActivity.objects
        .filter(
            Q(code__icontains=q) |
            Q(description__icontains=q) |
            Q(description_long__icontains=q)
        )
        .order_by("code")[:20]
    )

    data = [
        {
            "id": activity.code,
            "text": f"{activity.code} – {activity.description}",
        }
        for activity in results
    ]

    return JsonResponse(data, safe=False)
