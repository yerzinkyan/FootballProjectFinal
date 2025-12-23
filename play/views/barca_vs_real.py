import time
import random
from django.http import HttpResponse

from ..models import Player
from . import barca_squad, real_squad
from .utils import any_half_function, save_initial_state, restore_initial_state, penality_shootout


# նախնական ստատիկ տվյալների ներմուծում //////////////////////////////////////////////////
Barca_ID = list(Player.objects.filter(team='Barcelona', is_starting=True).values_list('id', flat=True))
Real_ID = list(Player.objects.filter(team='Real Madrid', is_starting=True).values_list('id', flat=True))
Barca_Bench_ID = list(Player.objects.filter(team='Barcelona', is_starting=False).values_list('id', flat=True))
Real_Bench_ID = list(Player.objects.filter(team='Real Madrid', is_starting=False).values_list('id', flat=True))


Teams = ["Barcelona", "Real Madrid"]
first_half_team = random.choice(Teams)
if first_half_team == 'Barcelona':
    second_half_team = 'Real Madrid'
else:
    second_half_team = 'Barcelona'


# ////////////////////////////////////////////////////////////////////////////////////////
# Գլխավոր ֆունկցիա //////////////////////////////////////////////////////////////////////
def barca_vs_real(request):
    initial_state = save_initial_state()
    team = first_half_team # Առաջին խաղակեսը սկսում է Բարսելոնան
    output = [] # output on browser screen
    score =[0, 0]
    Ratings = {}
    for i in  list(Player.objects.filter(is_starting=True).values_list('id', flat=True)):
        Ratings[f"{Player.objects.get(id=i).name}"] = 5

    inital_barca_player = Player.objects.get(team='Barcelona', is_starting=True, position = 'STR') # Դաշտի կենտրոնից խաղը միշտ սկսում ա կենտրոնական հարձակվողը
    inital_target_barca_player = Player.objects.get(id=random.choice([n for n in Barca_ID if n != inital_barca_player.id])) # Փոխանցում ստացող ֆուտբոլիստ

    inital_real_player = Player.objects.get(team='Real Madrid', is_starting=True, position = 'STR') # Դաշտի կենտրոնից խաղը միշտ սկսում ա կենտրոնական հարձակվողը
    inital_target_real_player = Player.objects.get(id=random.choice([n for n in Real_ID if n != inital_real_player.id])) # Փոխանցում ստացող ֆուտբոլիստ
    
    output += barca_squad(request)
    output += real_squad(request)
    time.sleep(3)

    print("\n")
    output.append("</br>")
    time.sleep(3)

#/////////////////////////////////////////////////////////////////////////////////////////////
# Առաջին խաղակես//////////////////////////////////////////////////////////////////////////////
    flag = "first_half"
    print(f"////////We are starting the 1st half////////\n////////{first_half_team} starts from centre////////\n")
    output.append(f"////////We are starting the 1st half////////</br>////////{first_half_team} starts from centre////////</br>")
    
    score = any_half_function(flag, output, team, inital_barca_player, inital_target_barca_player, inital_real_player, inital_target_real_player, 
                  score, Barca_ID, Real_ID, Barca_Bench_ID, Real_Bench_ID, Ratings)
    
    print(f'\n/////FIRST HALF IS ENDED/////')
    print(f'/////BARCELONA {score[0]} - {score[1]} Real Madrid/////')
    output.append(f'</br>/////FIRST HALF IS ENDED/////')
    output.append(f'/////BARCELONA {score[0]} - {score[1]} Real Madrid /////')
#/////////////////////////////////////////////////////////////////////////////////////////////
# Առաջին խաղակեսի ավարտ//////////////////////////////////////////////////////////////////////

    time.sleep(5)

#///////////////////////////////////////////////////////////////////////////////////////////
# Երկրորդ խաղակես///////////////////////////////////////////////////////////////////////////
    flag = "second_half"
    print(f"\n////////We came back and starting the 2st half\n{second_half_team} starts from centre////////\n")
    output.append(f"</br>////////We came back and starting the 2st half</br>{second_half_team} starts from centre////////</br>")
    score = any_half_function(flag, output, team, inital_barca_player, inital_target_barca_player, inital_real_player, inital_target_real_player,
                      score, Barca_ID, Real_ID, Barca_Bench_ID, Real_Bench_ID, Ratings)

    print(f'\n///// THE MATCH IS ENDED/////')
    print(f'/////BARCELONA {score[0]} - {score[1]} Real Madrid/////')
    output.append(f'</br>/////THE MATCH IS ENDED/////')
    output.append(f'/////BARCELONA {score[0]} - {score[1]} Real Madrid /////')
#/////////////////////////////////////////////////////////////////////////////////////////////
# Երկրորդ խաղակեսի ավարտ//////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////////////////////////////
# 11մետրանոց հարվածաշար///////////////////////////////////////////////////////////////////////
    if score[0] == score[1]:
        penality_shootout(output)
    
    print("\n************* Ratings of footballers *************")
    for player, rating in Ratings.items():
        output.append(f"{player} --> {round(rating, 1)}")
        print(f"{player} --> {round(rating, 1)}", end=' || ')

    best_player, best_rating = max(Ratings.items(), key=lambda x: x[1])
    print(f"\n************* MAN OF THE MACTH IS {best_player} - {round(best_rating, 1)} *************")
    output.append(f"</br>************* MAN OF THE MACTH IS {best_player} - {round(best_rating, 1)} *************")
    print("miban")

    restore_initial_state(initial_state)
    return HttpResponse("<br>".join([x.decode() if isinstance(x, bytes) else x for x in output]))
#/////////////////////////////////////////////////////////////////////////////////////////////
# Ամբողջական խաղի ավարտ///////////////////////////////////////////////////////////////////////