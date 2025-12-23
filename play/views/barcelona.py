from ..models import Player
from django.http import HttpResponse

def barca_squad(request):
    starting_players = list(Player.objects.filter(team='Barcelona', is_starting=True).values_list('id', flat=True))
    bench_players = list(Player.objects.filter(team='Barcelona', is_starting=False).values_list('id', flat=True))

    lines = []
    lines.append("</br>//// Barcelona Starting lineup ////")
    print("\n//// Barcelona Starting lineup ////")
    for p in starting_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    lines.append("</br>//// Barcelona Bench ////\n")
    print("\n//// Barcelona Bench ////")
    for p in bench_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    body = "<br>".join(lines)
    return HttpResponse(body)
