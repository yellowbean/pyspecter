from pyspecter import query, S
import pytest

m = {"A":{"B1":[10,20],"B2":2,"B3":3}
     ,"C":{"B1":[1,2],"B2":[3,4]}
     ,"D":[1,2,3,4]
     ,"E":[None,2,3,4]
     ,"F":{"G":1}
     ,"H":["A1","A2","A3"]}


def test_first():
    assert query(m, ["D", S.FIRST]) == 1
    assert query(m, ["A", S.FIRST]) == ("B1", [10, 20])

    assert query(m, ["D", S.LAST]) == 4
    assert query(m, ["A", S.LAST]) == ("B3", 3)


def test_nth():
    assert query(m, ["D", (S.NTH, 1)]) == 2
    # assert query(m, ["D",(S.NTH, 1)]) == 2


def test_map():
    assert query(m, ["C", S.MVALS]) == [[1, 2], [3, 4]]
    assert query(m, ["C", S.MKEYS]) == ['B1', 'B2']


def test_index_vals():
    assert query(m, ["A", S.INDEXED_VALS]) == [(0, ("B1", [10,20])), (1, ("B2", 2)), (2, ("B3", 3))]
    assert query(m, ["C", "B1", S.INDEXED_VALS]) == [(0, 1), (1, 2)]


def test_filter():
    assert query(m, ["A", "B1", (S.FILTER, lambda x: x > 10)]) == [20]
    assert query(m, ["C", (S.FILTER, lambda k, v: k.endswith("2"))]) == [[3, 4]]


def test_map_if():
    assert query(m, ["A", (S.MKEY_IF, lambda x:x.endswith("1"))]) == [[10, 20]]
    assert query(m, ["A", (S.MVAL_IF, lambda x:x==[10,20])]) == [[10, 20]]


def test_sub_map():
    assert query(m, ["A", (S.SUB_MAP, "B1")]) == {"B1":[10,20]}


def test_nthpath():
    assert query(m, ["D", (S.NTH_PATH, 2)]) == [3]

def test_none_to_val():
    assert query(None,[(S.NONE_VAL,10)]) == 10
    assert query(5,[(S.NONE_VAL,10)]) == 5

def test_srange():
    assert query(m, ["D",(S.SRANGE,2,3)]) == [3]

def test_must():
    assert query(m, [(S.MUST,"F","G")]) == 1
    assert query(m, [(S.MUST,"F","G","NOT_EXISTS")]) == None 

def test_if_path():
    assert query(m,[(S.IF_PATH,["C","B1"],["E"])]) == [None,2,3,4]
    assert query(m,[(S.IF_PATH,["C","B1"],["NOT_EXISTS"])]) == None
    assert query(m,[(S.IF_PATH,["C","B3"],["E"],["F"])]) == {'G': 1}

def test_regrex():
    assert query(m, ["A",(S.REGEX,r"B[23]")]) == [ 2,3 ]
    assert query(m, ["H",(S.REGEX,r"\S1")]) == [ "A1" ]

def test_maybe():
    m1 = {"A":{"B":{"C":1}}}
    assert query(m1, ["A",(S.MAYBE,"B"),"C"]) == 1
    assert query(m1, ["A",(S.MAYBE,"D"),"B"]) == {"C":1}


