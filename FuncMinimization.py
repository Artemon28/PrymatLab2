import array
import math

def ConstantValue(func, a, b, epsilon):
    return 1/20

temp = 1/5
def StepSplittingMethod(func, a, b, epsilon):
    return temp / 2

def goldenRatio(func, a, b, epsilon):
    countIter = 1
    countFunc = 0
    phi = (math.sqrt(5) + 1) / 2
    resphi = 2 - phi
    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    f1 = func(x1)
    f2 = func(x2)
    countFunc += 2
    while (b - a) > epsilon:
        countIter += 1
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + resphi * (b - a)
            f1 = func(x1)
            countFunc += 1
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - resphi * (b - a)
            f2 = func(x2)
            countFunc += 1
    return ((x1 + x2) / 2)


def Fibonacci(func, a, b, epsilon):
    countIter = 0
    countFunc = 0
    fib1 = 2
    fib2 = 1
    fib3 = 1
    prev = b - a
    while ((b - a) / epsilon) >= fib1:
        fib3 = fib2
        temp_fib = fib1
        fib1 = fib2 + fib1
        fib2 = temp_fib
    tmp1 = a + fib3 / fib1 * (b - a)
    tmp2 = a + fib2 / fib1 * (b - a)
    count_operation = 0
    ytmp1 = func(tmp1)
    ytmp2 = func(tmp2)
    countFunc += 2
    while (b - a > epsilon):
        countIter += 1
        count_operation = count_operation + 1
        if (ytmp1 > ytmp2):
            a = tmp1
            tmp1 = tmp2
            ytmp1 = ytmp2
            tmp2 = a + fib2 / fib1 * (b - a)
            ytmp2 = func(tmp2)
            countFunc += 1
        else:
            b = tmp2
            tmp2 = tmp1
            ytmp2 = ytmp1
            tmp1 = a + fib3 / fib1 * (b - a)
            ytmp1 = func(tmp1)
            countFunc += 1
        prev = b - a
        temp_fib = fib3
        fib3 = fib2 - fib3
        fib1 = fib2
        fib2 = temp_fib
    tmp2 = tmp1 + epsilon
    ytmp2 = func(tmp2)
    countFunc += 1
    if (ytmp1 >= ytmp2):
        a = tmp1
    else:
        b = tmp2
    return((a + b) / 2)