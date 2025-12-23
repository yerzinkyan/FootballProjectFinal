from ..models import Player
from django.http import HttpResponse

def barca_squad(request):
    starting_players = Player.objects.filter(
        team='Barcelona',
        is_starting=True
    ).order_by('id')

    bench_players = Player.objects.filter(
        team='Barcelona',
        is_starting=False
    ).order_by('id')

    lines = []
    lines.append("</br>//// Barcelona Starting lineup ////</br>4-3-3  Head Coach - Hansi Flick")
    print("\n//// Barcelona Starting lineup ////\n4-3-3  Head Coach - Hansi Flick")

    for p in starting_players:  # p is now a real Player object
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    lines.append("</br>//// Barcelona Bench ////")
    print("\n//// Barcelona Bench ////")

    for p in bench_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    body = "<br>".join(lines)
    return HttpResponse(body)