import json
from pathlib import Path
from django.http import JsonResponse
from django.shortcuts import render

LOOKUP = json.loads((Path(__file__).resolve().parent.parent / "lookup.json").read_text())
BANDS = ["first", "1-4", "5-49", "50+"]


def estimate(request):
    band = request.GET.get("band", "")
    repro = request.GET.get("repro", "")
    if band not in BANDS or repro not in ("0", "1"):
        return JsonResponse({"error": "band must be first, 1-4, 5-49 or 50+; repro must be 0 or 1"},
                            status=400)
    return JsonResponse(LOOKUP[f"{band}|{repro}"] | {"band": band, "repro": int(repro)})

def index(request):
    return render(request, "predictor/index.html")