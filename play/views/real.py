from ..models import Player
from django.http import HttpResponse

def real_squad(request):
    starting_players = list(Player.objects.filter(team='Real Madrid', is_starting=True).values_list('id', flat=True))
    bench_players = list(Player.objects.filter(team='Real Madrid', is_starting=False).values_list('id', flat=True))

    lines = []
    lines.append("</br>//// Real Madrid Starting lineup ////\n")
    print("\n//// Real Madrid Starting lineup ////")
    for p in starting_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    lines.append("</br>//// Real Madrid Bench ////\n")
    print("\n//// Real Madrid Bench ////")
    for p in bench_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    body = "<br>".join(lines)
    return HttpResponse(body)
