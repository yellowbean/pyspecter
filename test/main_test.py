from pyspecter import *
import pytest

m = {"A":{"B1":[10,20],"B2":2,"B3":3}
     ,"C":{"B1":[1,2],"B2":[3,4]}
     ,"D":[1,2,3,4]
     ,"E":[None,2,3,4]}


def test_simple():
    assert 1 == 1

def test_first():
    assert query(m,["D", S.FIRST]) == 1
    assert query(m,["A", S.FIRST]) == ("B1",[10,20])
    
    assert query(m,["D", S.LAST]) == 4
    assert query(m,["A", S.LAST]) == ("B3",3)


def test_nth():
    assert query(m,["D",(S.NTH,1)]) == 2
    #assert query(m,["D",(S.NTH,1)]) == 2

def test_map():
    assert query(m,["C",S.MVALS])==[[1,2],[3,4]]
    assert query(m,["C",S.MKEYS])==['B1','B2']

query(m,["D", (S.NTH, 2)])
# 3

query(m,["C", S.MVALS, S.LAST])
# [2,4]

query(m,["C",S.MVALS,S.FIRST])
# [1,3]

query(m,["C",S.MKEYS])
# ['B1', 'B2']

query(m, [(S.MULTI_PATH,["A", "B1"], ["D"])])
# [1, [1, 2, 3, 4]]

query(m,["D",(S.FILTER,lambda x:x>2)])
# [3,4]

query(m,["C",S.INDEXED_VALS])
# [(0, 'B1'), (1, 'B2')]

query(m,["C",(S.MKEY_IN,set(["B1","B2"]))])
# {'B1': [1, 2], 'B2': [3, 4]}
