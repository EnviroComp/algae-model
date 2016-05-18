import math

def calc_fn(nh, no, kmn, po, kmp):
    a = (nh+no)/(nh+no+kmn)
    b = (po)/(po+kmp)
    return min(a, b)
assert abs(calc_fn(0.0278,0.2763,0.025,0.0342,0.001) - 0.9240352476) < 0.01

def calc_ft(temp, tm, ktg1, ktg2):
    if temp <= tm:
        p = ((temp-tm) * (temp-tm) * -1 * ktg1)
    else:
        p = ((temp-tm) * (temp-tm) * -1 * ktg2)
    return math.exp(p)
assert abs(calc_ft(11.2067,30,0.008,0.008) - 0.0592787136) < 0.01

def calc_kess(last, sediment):
    a = 1.1 + (8.8 * last)
    b = 0.054 * math.pow((1000 * last), 0.667)
    c = 0.0458 * sediment
    return a + b + c
assert abs(calc_kess(0.014, 105.6667) - 6.376685346) < 0.01

def calc_death(kpr, kpd, kd1, kd2, temp):
    a = kpr*math.exp(kd1*(temp-20))
    b = kpd*math.exp(kd2*(temp-20))
    return a+b
assert abs(calc_death(0.125, 0.02, 0.069, 0.069, 11.2067)-0.0790433189) < 0.01

def calc_alpha(solar, im, kess, depth):
    a = math.exp(((-1*solar)/im) * math.exp((-1*kess*depth)))
    b = math.exp(((-1*solar)/im))
    return a-b
assert abs(calc_alpha(308.6, 300, 6.376685346, 2.22)-0.642516) < 0.01

def calc_fi(alpha, fday, depth, kess):
    a = math.e * fday * alpha
    b = depth * kess
    return a/b
assert abs(calc_fi(0.642516, 0.52, 2.22, 6.376685346) - 0.0641554858) < 0.01

def calc_growth(fn, fi, ft, pmx):
    return fn * fi * ft * pmx
assert abs(calc_growth(0.9240352476, 0.0641554858, 0.125, 2) - 0.0070283131) < 0.01

def calc_concentration(cj, cii, growth, death):
    return max(cj, cii + (cii * (growth-death)))
assert abs(calc_concentration(0.014, 0.014, 0.0070283131, 0.0790433189)-0.014) < 0.01
