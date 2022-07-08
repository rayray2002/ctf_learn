import random
import json
import functools as fn
import numpy as np
import string
import hashlib

charset = string.ascii_lowercase+string.digits+',. '
charset_idmap = {e: i for i, e in enumerate(charset)}

ksz = 80

def decrypt(ctx, key):
    N, ksz = len(charset), len(key)
    return ''.join(charset[(c-key[i % ksz]) % N] for i, c in enumerate(ctx))

def toPrintable(data):
    ul = ord('_')
    data = bytes(c if 32 <= c < 127 else ul for c in data)
    return data.decode('ascii')

with open('./output.txt') as f:
    ctx = f.readline().strip()[4:]
    enc = bytes.fromhex(f.readline().strip()[6:])
ctx = [charset_idmap[c] for c in ctx]

with open('./ngrams.json') as f:
    ngrams = json.load(f)

@fn.lru_cache(10000)
def get_trigram(x):
    x = ''.join(x)
    y = ngrams.get(x)
    if y is not None:
        return y
    ys = []
    a, b = ngrams.get(x[:2]), ngrams.get(x[2:])
    if a is not None and b is not None:
        ys.append(a+b)
    a, b = ngrams.get(x[:1]), ngrams.get(x[1:])
    if a is not None and b is not None:
        ys.append(a+b)
    if len(ys):
        return max(ys)
    if any(c not in ngrams for c in x):
        return -25
    return sum(map(ngrams.get, x))

@fn.lru_cache(10000)
def fitness(a):
    plain = decrypt(ctx, a)
    tgs = zip(plain, plain[1:], plain[2:])
    score = sum(get_trigram(tg) for tg in tgs)
    return score

def initialize(size):
    population = []
    for i in range(size):
        key = tuple(random.randrange(len(charset)) for _ in range(ksz))
        population.append(key)
    return population

def crossover(a, b, prob):
    r = list(a)
    for i in range(len(r)):
        if random.random() < prob:
            r[i] = b[i]
    return tuple(r)

def mutate(a):
    r = list(a)
    i = random.randrange(len(a))
    r[i] = random.randrange(len(charset))
    return tuple(r)

# keys = np.array(initialize(10000))
# scores = np.array([fitness(tuple(k)) for k in keys])
# keys = keys[scores.argsort()[::-1][:500]]

# for i in range(1000):
#     child = np.array([crossover(k, keys[random.randrange(len(keys))], 0.5) for k in keys])
#     mutated = np.array([mutate(k) for k in keys])
#     keys = np.concatenate((child, mutated))

#     scores = np.array([fitness(tuple(k)) for k in keys])
#     keys = keys[np.argsort(scores)[::-1][:500]]
#     print(i, max(scores))
#     print(decrypt(ctx, keys[0]))

# print(list(keys[0]))
key = [24, 23, 23, 21, 12, 11, 12, 33, 9, 15, 37, 25, 20, 17, 36, 1, 26, 31, 35, 17, 23, 11, 2, 22, 15, 28, 25, 8, 4, 26, 35, 21, 25, 24, 19, 14, 32, 19, 16, 34, 27, 0, 28, 8, 21, 24, 21, 10, 21, 28, 4, 2, 6, 32, 20, 33, 11, 10, 36, 34, 31, 30, 28, 12, 10, 2, 19, 27, 38, 7, 0, 20, 29, 38, 27, 2, 21, 17, 1, 28]
plain = "gitli is a 384 bits marmutatith designed to achieve high security with high perfortance across a bro,  range t  platforms. it is currently in round 2 of the nist sightweight cryptodnaphic pwiject, the submission consisting of an authenticatedgencryption and a  nyptograubic hash function. in this paper, we focus on the gitli cipher, which marforms fothenticated encryption with associated data."

# 82: t -> m
idx = plain.find("perfortance")
print(idx)
print(plain[82])
key[2] += charset_idmap['t'] - charset_idmap['m']
print(decrypt(ctx, key))
# gimli is a 384 bits marmutatith designed to achieve high security with high performance across a bro,  range t  platforms. it is currently in round 2 of the nist lightweight cryptodnaphic pwiject, the submission consisting of an authenticated encryption and a  nyptograubic hash function. in this paper, we focus on the gimli cipher, which marforms fothenticated encryption with associated data.

# 189: w -> r
# 190: i -> o
idx = plain.find("pwiject")
print(idx)
print(plain[189])
key[189%80] += charset_idmap['w'] - charset_idmap['r']
key[190%80] += charset_idmap['i'] - charset_idmap['o']
print(decrypt(ctx, key))
# gimli is a 384 bits marmutation designed to achieve high security with high performance across a bro,  range of platforms. it is currently in round 2 of the nist lightweight cryptodnaphic project, the submission consisting of an authenticated encryption and a  nyptographic hash function. in this paper, we focus on the gimli cipher, which marforms authenticated encryption with associated data.

# 340: m -> p
# 341: a -> e
idx = plain.find("marforms")
print(idx)
print(plain[340])
key[340%80] += charset_idmap['m'] - charset_idmap['p']
key[341%80] += charset_idmap['a'] - charset_idmap['e']
print(decrypt(ctx, key))
# gimli is a 384 bits permutation designed to achieve high security with high performance across a broad range of platforms. it is currently in round 2 of the nist lightweight cryptographic project, the submission consisting of an authenticated encryption and a cryptographic hash function. in this paper, we focus on the gimli cipher, which performs authenticated encryption with associated data.

print(key)
k = hashlib.sha512(''.join(charset[k] for k in key).encode('ascii')).digest()
flag = bytes(ci ^ ki for ci, ki in zip(enc, k)).decode('ascii')
print(flag)
