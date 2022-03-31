from turtle import back
from backpack import Backpack
import random
from typing import Tuple

LENGTH_FINAL = 100
def selection(List, int):
    print("hola")

def elite(l, backpack):
    aux = list(l)
    aux.sort(key = backpack.getFitness, reverse = True)
    return set(aux[0:LENGTH_FINAL])

def get_q(p_i_list, divisor):
    q = []
    aux = 0
    for i in range(0, len(p_i_list)):
        aux = aux + (p_i_list[i] / divisor)
        q.append(aux)
    return q
        
def selection_method(individuals, p_i_list, divisor, length, isRulet = False):
    p_i_list = [0] + p_i_list if isRulet else p_i_list
    q_list = get_q(p_i_list, divisor)
    len_p_i_list = len(p_i_list)
    i = 1
    res = []
    while (len(res) < length):
        if (i == len_p_i_list):
            i = 1
        r = random.uniform(0,1)
        if (q_list[i-1] < r and r <= q_list[i]):
            index = i - 1 if isRulet else i
            res.append(individuals[index])
        i += 1

    return res

def ruleta(individuals, backpack):
    f_list = []
    sumFit = 0
    length = len(individuals)
    for i in range (length):
        f_list.append(backpack.getFitness(individuals[i]))
        sumFit += f_list[i]
    res = selection_method(individuals, f_list, sumFit, length / 2, isRulet=True)
    return res

def rank(individuals):
    aux = list(individuals)
    sumfit = 0
    aux.sort(reverse = True)
    length = len(individuals)
    f_i_list = []
    for i in range(0,len(aux)):
        fit_inv = (length - (aux.index(individuals[i]) + 1)) / length 
        f_i_list.append(fit_inv)
        sumfit += fit_inv
    
    res = selection_method(individuals, f_i_list, sumfit, length / 2)
    return res

def tournament(list, backpack):
    u = random.uniform(0.5,1)
    competitors = random.sample(list, 4)
    pair_one = competitors[:2]
    pair_two = competitors[2:]
    r = random.uniform(0,1)
    winners = []
    pairs = [pair_one, pair_two, winners]
    for p in pairs:
        first_fit = backpack.getFitnes(p[0])
        second_fit = backpack.getFitness(p[1])
        best_fit = p[1] if second_fit > first_fit else p[0]
        worst_fit = p[1] if second_fit <= first_fit else p[0]

        if r < u:
            winners.append(best_fit)
        else:
            winners.append(worst_fit)

    return winners[-1]

def boltzman(l, backpack):
    pass

def truncated(list, k, backpack):
    fitness = []
    for i in range (len(list)):
        fitness.append(backpack.getFitness(list[i]), list[i])
    fitness.sort()
    list_truncated = fitness[k: len(list)]

    #TO DO: HAY QUE LLAMAR A ALGUNO DE LOS OTROS METODOS. DESPUES DEFINIMOS CUAL
