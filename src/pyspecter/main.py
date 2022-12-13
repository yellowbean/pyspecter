from enum import Enum

class S(Enum):
    ALL=0
    FIRST=1
    LAST=2
    NTH=3
    MVALS=4
    MKEYS=5
    INDEXED_VALS=6
    FILTER=7
    MULTI_PATH=8
    MKEY_IN=9

def query(d,p,debug=False):
    if debug:
        print("matching",d,p)
    match p:
        case []:
            return d
        case [S.MKEYS,*_r] if isinstance(d,dict):
            return query(list(d.keys()),_r)
        case [(S.MKEY_IN,ks),*_r] if isinstance(d,dict):
            _d = {k:v for k,v in d.items() if k in ks}
            return query(_d,_r)
        case [S.MVALS,*_r] if isinstance(d,dict):
            return query(list(d.values()),_r)   
        case [S.FIRST,*_r]:
            return [ query(_[0],_r) for _ in d]
        case [S.LAST,*_r]:
            return [ query(_[-1],_r) for _ in d] 
        case [(S.NTH,n),*_r]:
            return query(d[n],_r)  
        case [S.INDEXED_VALS,*_r]:
            return [ query(_,_r) for _ in enumerate(d)]
        case [(S.MULTI_PATH,*_p),*_r]:
            return [ query(d, _+_r) for _ in _p ]    
        case [S.ALL,*_r] if isinstance(d,list):
            return [ query(_ ,_r) for _ in d ]
        case [(S.FILTER,f),*_r]:
            return [ query(_ ,_r) for _ in d if f(_)]
        case [_h,*_r] if isinstance(d,dict):
            try:
                return query(d[_h],_r)
            except KeyError as ke:
                print(f"{p[0]} is not in {d}")

