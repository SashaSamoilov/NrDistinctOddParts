import math, timeit

# Без кэширования очень медленно
import sys
from functools import lru_cache
sys.setrecursionlimit(10000)
@lru_cache(maxsize=None)
def nr_rec_distinct_odd_by_k(n, k):
    if n < k or n < 1 or k < 1:
        return 0
    if n == 1 and k == 1:
        return 1
    return nr_rec_distinct_odd_by_k(n - 2*k, k) + nr_rec_distinct_odd_by_k(n - (2*k - 1), k - 1)

def distinct_odd_parts_by_k(n, k):
    p = [[0] * (k + 1) for _ in range(n + 1)]
    p[1][1] = 1
    for i in range(1, n + 1):
        limit = min(k, i)
        for j in range(1, limit + 1):
            if i > 2 * j:
                p[i][j] += p[i - 2 * j][j]
            if i > 2 * j - 1 and j > 1:
                p[i][j] += p[i - (2 * j - 1)][j - 1]
    return p[n][k]

def restrict_parts_by_k(n, k):
    p = [0] * (n + 2)
    p[1] = 1
    for m in range(1, k + 1):
        for i in range(m + 1, n + 2):
            p[i] += p[i - m]
    return p[n + 1]

def distinct_odd_parts_naive(n):
    # Количество разбиений n на различные нечетные части (простой алгоритм)
    result = 0
    kbound = math.isqrt(n)
    for k in range(1, kbound + 1):
        if (n - k) % 2 == 0:
            result += nr_rec_distinct_odd_by_k(n, k)
    return result

def distinct_odd_parts(n):
    # Количество разбиений n на различные нечетные части
    result = 0
    kbound = math.isqrt(n)
    for i in range(1, kbound + 1):
        if (n - i) % 2 == 0:
            result += distinct_odd_parts_by_k(n, i)
    return result

def restrict_parts(n):
    # Количество разбиений n на различные нечетные части (через биекцию)
    result = 0
    kbound = math.isqrt(n)
    for i in range(1, kbound + 1):
        if (n - i) % 2 == 0:
            result += restrict_parts_by_k((n - i * i) // 2, i)
    return result

def test_correctness(minn, maxn):
    # Сравнение результатов алгоритмов для нескольких n
    print("Проверка корректности...")
    for n in range(minn, maxn):
        a1 = distinct_odd_parts_naive(n)
        a2 = distinct_odd_parts(n)
        a3 = restrict_parts(n)
        if a1 != a2 or a1 != a3 or a2 != a3:
            print(f"ОШИБКА: значения не совпадают для n={n}, a1 = {a1}, a2 = {a2}, a3 = {a3}!")
            return False
        else:
            print(f"f({n}) = {a1}")
    print("Все результаты совпадают.")
    return True

def measure_time():
    ns = [100, 200, 500, 1000, 3333, 5000, 7777, 9999, 15000, 25000, 49999]
    print("Замеры времени (10 повторений):")
    print("n\t\tАлг. 1 (с)\t\tАлг. 2 (с)\t\tАлг. 3 (с)\t\tr(n)")
    for n in ns:
        try:
            t1 = timeit.timeit(lambda: distinct_odd_parts_naive(n), number=10) / 10
            t1_str = f"{t1:.3f}"
        except RecursionError:
            t1_str = "-"

        t2 = timeit.timeit(lambda: distinct_odd_parts(n), number=10) / 10
        t3 = timeit.timeit(lambda: restrict_parts(n), number=10) / 10
        
        res = restrict_parts(n)
        print(f"{n}\t\t{t1_str}\t\t\t{t2:.3f}\t\t\t{t3:.3f}\t\t\t{res}")

test_correctness(250, 500)
measure_time()
