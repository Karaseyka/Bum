import queue

a = [[1, 1, 1],
     [1, 0, 0],
     [1, 1, 1],
     [1, 1, 1]]
sm = []
for i in range(len(a)):
    for j in range(len(a[i])):
        d = []
        if a[i][j] != 0:
            if i + 1 < len(a) and a[i + 1][j] == 1:
                d.append(len(a[i]) * (i + 1) + j + 1)
            if i - 1 >= 0 and a[i - 1][j] == 1:
                d.append(len(a[i]) * (i - 1) + j + 1)
            if j + 1 < len(a[i]) and a[i][j + 1] == 1:
                d.append(len(a[i]) * i + j + 2)
            if j - 1 >= 0 and a[i][j - 1] == 1:
                d.append(len(a[i]) * i + j)
            sm.append(d)
        else:
            sm.append([])
di = [1000000] * (len(a) * len(a[0]) + 1)
p = [1000000] * (len(a) * len(a[0]) + 1)
print(sm)


def bfs(start):
    q = queue.Queue()
    di[start] = 0
    q.put(start)
    while not q.empty():
        v = q.get()
        try:
            for u in sm[v - 1]:
                if di[u] == 1000000:
                    di[u] = di[v] + 1
                    q.put(u)
                    p[u] = v
        except Exception:
            print("dfhsfd", v)


bfs(1)


def return_way(t):
    f = [12]
    while t != 1:
        print(t)
        f.append(p[t])
        t = p[t]
    f.reverse()
    print(f)


return_way(12)
