n_iter = 10_000_000
pi = 0
for i in range(n_iter):
    d = i*2+1

    if i % 2 == 0:
        pi += 4/d

    else:
        pi -= 4/d

print(pi)