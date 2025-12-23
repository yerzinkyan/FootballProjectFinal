
import random
import time

from ..models import Player
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response


def any_half_function(flag, output, team, inital_barca_player_f, inital_target_barca_player_f, inital_real_player_f, inital_target_real_player_f,
                      score, ids_b, ids_r, ids_b_bench, ids_r_bench, Ratings):
    if flag == "first_half":
        y = 1
        z = 46
    else:
        y = 45
        z = 91
        
    for i in range(y, z): # 45 անգամ կրկնություն այսինքն 45 րոպե
        if i == 60:
            print('\n//////////////////////// Changes //////////////////////')
            output.append('</br>//////////////////////// Changes //////////////////////')
            subs(ids_b, ids_b_bench, Ratings, output)
            subs(ids_b, ids_b_bench, Ratings, output)
            subs(ids_b, ids_b_bench, Ratings, output)
            subs(ids_r, ids_r_bench, Ratings, output)
            subs(ids_r, ids_r_bench, Ratings, output)
            subs(ids_r, ids_r_bench, Ratings, output)            
            print('///////////////////////////////////////////////////////\n')
            output.append('///////////////////////////////////////////////////////</br>')
            time.sleep(2)
        elif i == 75:
            print('\n//////////////////////// Changes //////////////////////')
            output.append('</br>//////////////////////// Changes //////////////////////')
            subs(ids_b, ids_b_bench, Ratings, output)
            subs(ids_b, ids_b_bench, Ratings, output)
            subs(ids_r, ids_r_bench, Ratings, output)
            subs(ids_r, ids_r_bench, Ratings, output)
            print('///////////////////////////////////////////////////////\n')
            output.append('///////////////////////////////////////////////////////</br>')
            time.sleep(2)
        else:
            version = random.choices(["Pass", "Shoot"], weights=[90, 10], k=1)[0] # Կատարվելիք գործողության որոշում
            res = random.choices(['ok', 'fail'], weights=[85, 15], k=1)[0] # Փոխանցումի հաջող լինելու հավանականությունն է որոշում
            res1 = random.choices(['ok', 'fail'], weights=[20, 80], k=1)[0]

            if team == 'Barcelona': # Թիմը Բարսելոնան է, փոխանցման հաջողության դեպքում կրկին փոխանցում է ձեռնարկվում, հակառակ դեպքում գնդակը անցնում է մրցակցին 
                P1_barca = inital_barca_player_f
                P2_barca = inital_target_barca_player_f
                if version == "Pass":
                    if res == 'ok':
                        inital_barca_player_f, inital_target_barca_player_f, Ratings = correct_pass(P1_barca, P2_barca, i, output, ids_b, Ratings)
                    else:
                        team = 'Real Madrid' 
                        inital_real_player_f, inital_target_real_player_f, Ratings = wrong_pass(inital_barca_player_f, inital_real_player_f, inital_target_real_player_f, i, output, ids_r, team, Ratings)
                elif version == "Shoot":
                    if res1 == 'ok':
                        score, inital_real_player_f, team, Ratings = goal_kicking(P1_barca, team, output, score, i, Ratings) 
                    else:
                        team, inital_real_player_f, Ratings = miss_kicking(output, P1_barca, team, i, Ratings)
                    version = "Pass"


            elif team == 'Real Madrid':  # Թիմը Յուվենտուսն է, փոխանցման հաջողության դեպքում կրկին փոխանցում է ձեռնարկվում, հակառակ դեպքում գնդակը անցնում է մրցակցին 
                P1_real = inital_real_player_f
                P2_real = inital_target_real_player_f
                if version == "Pass":
                    if res == 'ok':
                        inital_real_player_f, inital_target_real_player_f, Ratings = correct_pass(P1_real, P2_real, i, output, ids_r, Ratings)
                    else:
                        team = 'Barcelona'
                        inital_barca_player_f, inital_target_barca_player_f, Ratings = wrong_pass(inital_real_player_f, inital_barca_player_f, inital_target_barca_player_f, i, output, ids_b, team, Ratings)
                elif version == "Shoot":
                    if res1 == 'ok':
                        score, inital_barca_player_f, team, Ratings = goal_kicking(P1_real, team, output, score, i, Ratings)
                    else:
                        team, inital_barca_player_f, Ratings = miss_kicking(output, P1_real, team, i, Ratings)
                    version = "Pass"

            time.sleep(0.5)

    adding_time(i, output)
    return(score)


def correct_pass(P1, P2, minute, output, ids, rate):
    output.append(f'[minute {minute}] {P1.number}.{P1.name} plays a pass to {P2.number}.{P2.name}')
    print(f'[minute {minute}] {P1.number}.{P1.name} plays a pass to {P2.number}.{P2.name}')
    
    ensure_rating(P1, rate)
    ensure_rating(P2, rate)
    if rate[P1.name] < 10:
        rate[P1.name] += 0.3

    new_player = P2
    new_target = Player.objects.get(id=random.choice([n for n in ids if n not in (P1.id, P2.id)]))

    return new_player, new_target, rate


def wrong_pass(P1, opponent_P1, opponent_P2, minute, output, ids, team, rate):
    opponent_P1 = Player.objects.get(id=random.choice(ids))
    opponent_P2 = Player.objects.get(id=random.choice([n for n in ids if n != opponent_P1.id]))

    ensure_rating(P1, rate)
    if rate[P1.name] > 4:
        rate[P1.name] -= 0.3

    output.append(f'[minute {minute}] {P1.number}.{P1.name} lost the ball </br> </br> {team} with ball - {opponent_P1.number}.{opponent_P1.name}')
    print(f'[minute {minute}] {P1.number}.{P1.name} lost the ball \n\n> {team} with ball - {opponent_P1.number}.{opponent_P1.name}')

    return(opponent_P1, opponent_P2, rate)


def goal_kicking(P1_attack, team, output, s, minute, rate):
    output.append(f'[minute {minute}] {P1_attack.number}.{P1_attack.name} IS SHOOTING AND GOOOOAAAAL')
    print(f'[minute {minute}] {P1_attack.number}.{P1_attack.name} IS SHOOTING AND GOOOOAAAAL')

    ensure_rating(P1_attack, rate)
    if rate[P1_attack.name] < 10:
        rate[P1_attack.name] += 1.5


    if team == "Barcelona":
        s[0] += 1
        P1_defense = Player.objects.filter(team='Real Madrid', position='STR', is_starting=True).first()
        team == 'Real Madrid'
    else:
        s[1] += 1
        P1_defense = Player.objects.filter(team='Barcelona', position='STR', is_starting=True).first()
        team == 'Barcelona'

    print(f'\n{P1_defense} will restart from centre')
    output.append(f"</br>{P1_defense} will restart from centre")
    team = "Real Madrid"
    output.append(f'///// BARCELONA {s[0]} - {s[1]} Real Madrid /////</br>')
    print(f'///// BARCELONA {s[0]} - {s[1]} Real Madrid /////\n')

    return(s, P1_defense, team, rate)


def miss_kicking(output, P1_attack, team, minute, rate):
    output.append(f'[minute {minute}] {P1_attack.number}.{P1_attack.name} takes a shot but misses')
    print(f'[minute {minute}] {P1_attack.number}.{P1_attack.name} takes a shot but misses')
    ensure_rating(P1_attack, rate)
    if rate[P1_attack.name] > 5:
        rate[P1_attack.name] -= 0.5
    if team == "Barcelona":
        P1_defense = Player.objects.filter(team='Real Madrid', position='GK', is_starting=True).first()
        team = 'Real Madrid'
    else:
        P1_defense = Player.objects.filter(team='Barcelona', position='GK', is_starting=True).first()
        team = 'Barcelona'
    print(f'\nFree kick from a goal defended by {P1_defense}')
    output.append(f"</br>Free kick from a goal defended by {P1_defense}")
    return(team, P1_defense,rate)


def adding_time(x, output):
    add = random.randint(0,3) # Ավելացրած ժամաանակ
    if add > 0:
        output.append(f"The referee adds {add} minutes of added time")
        print(f"The referee adds {add} minutes of added time")
        for j in range(1, add + 1):
            output.append(f'[minute {x} + {j}]')
            print(f'[minute {x} + {j}]')


def penality_shootout(output):
    print("\n////////////SCORE IS EQUAL SO WE WILL HAVE PENALITY SHOOTOUT////////////")
    output.append("</br>////////////SCORE IS EQUAL SO WE WILL HAVE PENALITY SHOOTOUT////////////")
    score = {
        'Barcelona': 0,
        'Real Madrid': 0
    }

    teams = ['Barcelona', 'Real Madrid']

    for i in range(5):
        for team in teams:
            result = random.choice(['ok', 'fail'])
            if result == 'ok':
                score[team] += 1
            print(f"Penalty {i+1}: {team} --> {result} SCORE IS {score}")
            output.append(f"Penalty {i+1}: {team} --> {result} SCORE IS {score}")

    while score['Barcelona'] == score['Real Madrid']:
        for team in teams:
            result = random.choice(['ok', 'fail'])
            if result == 'ok':
                score[team] += 1
            print(f"Penalty {i+1}: {team} --> Goal!! SCORE IS {score}")
            output.append(f"Penalty {i+1}: {team} --> Goal!! SCORE IS {score}")

        if score['Barcelona'] != score['Real Madrid']:
            break

    winner = max(score, key=score.get)

    print(f"\nResult: {score}")
    print(f"******************************************")
    print(f"******************************************")
    print(f"*******{winner} IS CHAMPIIIIIOOOOON*******")
    print(f"******************************************")
    print(f"******************************************")

    output.append(f"\nResult: {score}")
    output.append(f"******************************************")
    output.append(f"******************************************")
    output.append(f"*******{winner} IS CHAMPIIIIIOOOOON*******")
    output.append(f"******************************************")
    output.append(f"******************************************")
    return winner, score


def subs(start_ids, bench_ids, rate, output):
    k = 0
    for i in range(k,len(start_ids)):
        player_out = Player.objects.get(id=start_ids[i])
        player_out_name = player_out.name
        pos_out = player_out.position
        if rate.get(player_out_name, 5) <= 6:
            player_out.in_starting = False
            for j in range(len(bench_ids)):
                player_in = Player.objects.get(id=bench_ids[j])
                player_in_name = player_in.name
                if player_in.position == pos_out:
                    player_in.is_starting = True
                    start_ids.pop(i)
                    start_ids.append(bench_ids[j])
                    bench_ids.pop(j)
                    player_out.save()
                    player_in.save()
                    print(f"({player_in_name}) comes on to replace ({player_out_name})")
                    output.append(f"({player_in_name}) comes on to replace ({player_out_name})")
                    return
            k = i + 1
            time.sleep(0.2)


def save_initial_state():
    return list(
        Player.objects.values('id', 'is_starting')
    )


def restore_initial_state(initial_state):
    for p in initial_state:
        Player.objects.filter(id=p['id']).update(
            is_starting=p['is_starting']
        )


def ensure_rating(player, rate, default=5):
    rate.setdefault(player.name, default)
