import faker
from tqdm import tqdm
import pickle
import random
import hashlib
import sys
import os

def generate_ips(N, p=1.1):
    out = set()
    fake = faker.Faker()
    for _ in tqdm(range(int(N*p))):
        out.add(fake.ipv4())
    print('unique ips:',len(out))
    out = list(out)[:N]
    print('output len:',len(out))
    os.makedirs('work', exist_ok=True)
    pickle.dump(out, open('work/ips.pkl','wb'))

def load_ips():
    ips = pickle.load(open('work/ips.pkl','rb'))
    print('loaded ips:',len(ips))
    return ips

def split(a,b,c, shuffle=True):
    ips = load_ips()
    assert c <= min(a,b)
    assert len(ips) >= a+b-c
    A = ips[:a]
    B = ips[a-c:a-c+b]
    if shuffle:
        random.shuffle(A)
        random.shuffle(B)
    return A,B

def write_file(filename, items):
    with open(filename,'w') as f:
        for item in items:
            f.write(item+'\n')

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def generate_files(prefix, a,b,c, shuffle=True):
    A,B = split(a,b,c, shuffle=shuffle)
    write_file(prefix+'A.txt', A)
    write_file(prefix+'B.txt', B)
    AH = [md5(ip) for ip in A]
    BH = [md5(ip) for ip in B]
    write_file(prefix+'AH.txt', AH)
    write_file(prefix+'BH.txt', BH)
    

def cli():
    a = dict(enumerate(sys.argv))
    try:
        if a[1] == 'init':
            n = int(a[2], 2_000_000)
            generate_ips(n)
        elif int(a[3]) <= min(int(a[1]),int(a[2])):   
            generate_files('work/', a=int(a[1]), b=int(a[2]), c=int(a[3]))
        else:
            help()
    except:
        help()

def help():
    print("""\
USAGE:
    python3 gen.py <A> <B> <C>
        OR
    python3 gen.py init <N>
    """)

if __name__ == '__main__':
    cli()
