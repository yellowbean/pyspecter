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
    MKEY_IF=10
    MVAL_IF=11
    SUB_MAP=12
    NTH_PATH=13
    NONE_LIST=14
    NONE_SET=15
    NONE_TUPLE=16
    #STAY=17
    #STOP=18
    VAL=19

def query(d,p,debug=False):
    if debug:
        print("matching",d,p)
    match p:
        case []:
            return d
        case [S.MKEYS,*_r] if isinstance(d,dict):
            return query(list(d.keys()),_r)
        case [S.ALL,*_r] :
            if isinstance(d,list) or isinstance(d,range):
                return [ query(_,_r) for _ in d ]
            elif isinstance(d,dict):
                _d = [ [k,v] for k,v in d.items()]
                return query(_d,_r)
        case [(S.MKEY_IN,ks),*_r] if isinstance(d,dict):
            _d = {k:v for k,v in d.items() if k in ks}
            return query(_d,_r)
        case [S.MVALS,*_r] if isinstance(d,dict):
            return query(list(d.values()),_r)   
        case [S.FIRST,*_r]:
            return [ query(_[0],_r) for _ in d]
        case [S.LAST,*_r]:
            return [ query(_[-1],_r) for _ in d] 
        case [(S.NTH,n),*_r] if isinstance(n,int):
            return query(d[n],_r)
        case [(S.NTH,*n),*_r]:
            return [ query(d[_],_r) for _ in n ]
        case [S.INDEXED_VALS,*_r]:
            return [ query(_,_r) for _ in enumerate(d)]
        case [(S.MULTI_PATH,*_p),*_r]:
            return [ query(d, _+_r) for _ in _p ]    
        case [S.ALL,*_r] if isinstance(d,list):
            return [ query(_ ,_r) for _ in d ]
        case [(S.FILTER,f),*_r]:
            return [ query(_ ,_r) for _ in d if f(_)]
        case [(S.MKEY_IF,f),*_r]:
            return [ query(d[k],_r) for k in d.keys() if f(k) ]
        case [(S.MVAL_IF,f),*_r]:
            return [ query(d[k],_r) for k,v in d.items() if f(v) ]
        case [(S.SUB_MAP,ks),*_r]:
            return query({k:v for k,v in d.items() if k in ks} ,_r)
        case [(S.NTH_PATH, *paths),*_r]:
            return [query(d,_r)[npth] for npth in paths]
        case [S.NONE_LIST, *_r]:
            if d is None:
                return query([],_r)
            return query(d,_r)
        case [S.NONE_SET, *_r]:
            if d is None:
                return query(set(),_r)        
            return query(d,_r)
        case [S.NONE_TUPLE, *_r]:
            if d is None:
                return query((),_r)    
            return query(d,_r)
        case [S.VAL, *_r]:
            sub_result = query(d,_r)
            return [ [d, _] for _ in sub_result ]
        case [_h,*_r] if isinstance(d,dict):
            try:
                return query(d[_h],_r)
            except KeyError as ke:
                print(f"{_h} is not in {d}")
