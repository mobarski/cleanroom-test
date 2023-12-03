import faker
from tqdm import tqdm

import pickle
import random
import hashlib
import sys
import os

def generate_ids(N, kind='ipv4', p=1.1):
    # number of IDs to generate = N*p
    # p>1 to ensure that we get N unique IDs
    out = set()
    fake = faker.Faker()
    generate_id = getattr(fake, kind)
    for _ in tqdm(range(int(N*p)), desc=f'generating {N} unique {kind} IDs'):
        out.add(generate_id())
    print('unique IDs:',len(out))
    out = list(out)[:N]
    print('output len:',len(out))
    os.makedirs('work', exist_ok=True)
    pickle.dump(out, open(f'work/{kind}.pkl','wb'))
    return out

def load_ids(kind):
    ids = pickle.load(open(f'work/{kind}.pkl','rb'))
    print(f'loaded {kind} IDs:',len(ids))
    return ids

def split(a,b,c, shuffle=True, kind='ipv4', N=2_000_000):
    try:
        ips = load_ids(kind)
    except:
        ips = generate_ids(N, kind=kind)
    assert c <= min(a,b)
    assert len(ips) >= a+b-c
    A = ips[:a]
    B = ips[a-c:a-c+b]
    if shuffle:
        print("shuffling A and B")
        random.shuffle(A)
        random.shuffle(B)
    return A,B

def write_file(filename, items):
    print(f"saving {filename}")
    with open(filename,'w') as f:
        for item in items:
            f.write(item+'\n')

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def generate_files(prefix, a,b,c, shuffle=True, kind='ipv4', N=2_000_000):
    A,B = split(a,b,c, shuffle=shuffle, kind=kind, N=N)
    write_file(prefix+'A.txt', A)
    write_file(prefix+'B.txt', B)
    AH = [md5(ip) for ip in A]
    BH = [md5(ip) for ip in B]
    write_file(prefix+'AH.txt', AH)
    write_file(prefix+'BH.txt', BH)
    print('DONE')
    

def cli():
    a = dict(enumerate(sys.argv))
    try:
        if int(a[3]) <= min(int(a[1]),int(a[2])):
            kind = a.get(4,'ipv4')
            N = int(a.get(5,2_000_000))
            generate_files('work/', a=int(a[1]), b=int(a[2]), c=int(a[3]), kind=kind, N=N)
        else:
            help()
    except:
        help()

def help():
    print("""\
USAGE:
    python3 gen.py <A> <B> <C> <kind=ipv4> <N=2_000_000>

WHERE:
    A = number of items in the A set
    B = number of items in the B set
    C = number of common items in A and B
    N = number of unique IDs to generate if the IDs are not already generated
    kind = faker method to use for generating IDs:
        ipv4, ipv6, email, mac_address, vin, iban, slug, etc.
    """)

if __name__ == '__main__':
    cli()
