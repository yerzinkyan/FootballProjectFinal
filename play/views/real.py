from ..models import Player
from django.http import HttpResponse

def real_squad(request):
    starting_players = Player.objects.filter(
        team='Real Madrid',
        is_starting=True
    ).order_by('id')

    bench_players = Player.objects.filter(
        team='Real Madrid',
        is_starting=False
    ).order_by('id')

    lines = []
    lines.append("</br>//// Real Madrid Starting lineup ////</br>4-3-3  Head Coach - Xabi Alonso")
    print("\n//// Real Madrid Starting lineup ////\n4-3-3  Head Coach - Xabi Alonso")

    for p in starting_players:  # p is now a real Player object
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    lines.append("</br>//// Real Madrid Bench ////")
    print("\n//// Real Madrid Bench ////")

    for p in bench_players:
        line = f"{p.number}. {p.name} ({p.position})"
        lines.append(line)
        print(line)

    body = "<br>".join(lines)
    return HttpResponse(body)