from enum import Enum
from functools import reduce  # forward compatibility for Python 3
import operator
import re


def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)

def lookupMap(m,ks):
    if not isinstance(m, dict) and len(ks) > 0:
        return None
    match ks:
        case []:
            return m
        case _:
            if ks[0] in m:
                return lookupMap(m[ks[0]],ks[1:])
            else:
                return None


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
    NONE_VAL=17
    #STAY=17
    #STOP=18
    VAL=20
    SRANGE=21
    MUST=22 # stop navigation
    IF_PATH=23
    REGEX=24
    MAYBE=25

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
        case [S.MVALS, *_r] if isinstance(d, dict):
            return query(list(d.values()),_r)   
        case [S.FIRST, *_r] if isinstance(d,list):
            return query(d[0], _r)
        case [S.FIRST, *_r] if isinstance(d,dict):
            ps = list(d.items())
            return query(ps[0], _r)
        case [S.LAST, *_r] if isinstance(d,list):
            return query(d[-1],_r)
        case [S.LAST, *_r]  if isinstance(d,dict):
            ps = list(d.items())
            return query(ps[-1], _r)
        case [(S.NTH,n), *_r] if isinstance(n,int):
            return query(d[n], _r)
        case [(S.NTH,*n), *_r]:
            return [ query(d[_], _r) for _ in n ]
        case [S.INDEXED_VALS, *_r] if isinstance(d, dict):
            ps = list(d.items())
            return [ query(_, _r) for _ in enumerate(ps)]
        case [S.INDEXED_VALS,*_r] if isinstance(d, list):
            return [ query(_, _r) for _ in enumerate(d)]
        case [(S.MULTI_PATH,*_p), *_r]:
            return [ query(d, _ + _r) for _ in _p ]    
        case [S.ALL, *_r] if isinstance(d,list):
            return [ query(_, _r) for _ in d]
        case [(S.FILTER, f), *_r] if isinstance(d, dict):
            return [ query(d[k], _r) for k, v in d.items() if f(k, v)]
        case [(S.FILTER, f), *_r] if isinstance(d, list):
            return [ query(_, _r) for _ in d if f(_)]
        case [(S.MKEY_IF, f), *_r]:
            return [ query(d[k], _r) for k in d.keys() if f(k) ]
        case [(S.MVAL_IF, f), *_r]:
            return [ query(d[k], _r) for k, v in d.items() if f(v) ]
        case [(S.SUB_MAP, ks), *_r]:
            return query({k:v for k,v in d.items() if k in ks} ,_r)
        case [(S.NTH_PATH, *paths),*_r]:
            return [ query(d, _r)[npth] for npth in paths]
        case [S.NONE_LIST, *_r]:
            if d is None:
                return query([],_r)
            return query(d,_r)
        case [S.NONE_SET, *_r]:
            if d is None:
                return query(set(),_r)        
            return query(d, _r)
        case [S.NONE_TUPLE, *_r]:
            if d is None:
                return query((),_r)    
            return query(d,_r)
        case [S.VAL, *_r]:
            sub_result = query(d,_r)
            return [ [d, _] for _ in sub_result ]
        case [(S.NONE_VAL, v), *_r]:
            if d is None:
                return v
            return query(d, _r)
        case [(S.SRANGE, s,e), *_r]:
            return query(d[s:e], _r)
        case [(S.MUST,*k), *_r]:
            x = lookupMap(d, k)
            return query(x, _r)
        case [(S.IF_PATH, cond, t), *_r]:
            if lookupMap(d, cond):
                return query(d, t + _r)
            else:
                return None
        case [(S.IF_PATH, cond,t,f), *_r]:
            if lookupMap(d, cond):
                return query(d, t + _r)
            else:
                return query(d, f + _r)
        case [(S.REGEX, reg), *_r] if isinstance(d,dict):
            pass_keys = [ query(d[k], _r) for k in d.keys() if re.match(reg,k) ]
            return pass_keys
        case [(S.REGEX, reg), *_r] if isinstance(d,list):
            pass_keys = [ query(d[i], _r) for i,k in enumerate(d) if re.match(reg,k) ]
            return pass_keys
        case [(S.MAYBE, *m), *_r]:
            if len(m)>0 :
                new_m = m[1:]
                if m[0] in d:
                    return query(d[m[0]], [(S.MAYBE, *new_m)]+_r)
                else:
                    return query(d, [(S.MAYBE, *new_m)]+_r)
            else:
                return query(d, _r)
        case [_h, *_r] if isinstance(d,dict):
            try:
                return query(d[_h],_r)
            except KeyError as ke:
                print(f"{_h} is not in {d}")
            except TypeError as te:
                print(f"navigate to {_h} on {d}, rest path:{_r}")
