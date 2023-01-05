# pyspecter

[![Python version](https://img.shields.io/pypi/pyversions/pyspecter)](https://img.shields.io/pypi/pyversions/pyspecter)
[![PyPI version](https://badge.fury.io/py/pyspecter.svg)](https://badge.fury.io/py/pyspecter)
[![PyPI download](https://img.shields.io/pypi/dm/pyspecter)](https://img.shields.io/pypi/dm/pyspecter)

A Python library to query nested structure, inspired by [specter](https://github.com/redplanetlabs/specter)

If you are dealing with nested python structure and it require complex rule to search the data underneath like:

* Key start with a pattern
* Value to be filter
* Conditional path to walk into
* ...

this is the right library fit the use case as it extract the `Navigation` rule to a list, saving your a lot of trouble writting your own logic to navigate the nested data.

## Get started
![image](https://user-images.githubusercontent.com/1008321/210162209-a7cce888-99ad-48af-ac63-693d63f825ff.png)

## Examples

    m = {"A":{"B1":[10,20],"B2":2,"B3":3}
         ,"C":{"B1":[1,2],"B2":[3,4]}
         ,"D":[1,2,3,4]
         ,"E":[None,2,3,4]
         ,"F":{"G":1}
         ,"H":["A1","A2","A3"]}
    
### Navigate to specific item 
#### FIRST/LAST     

    assert query(m, ["D", S.FIRST]) == 1
    assert query(m, ["A", S.FIRST]) == ("B1", [10, 20]) # first element from dict.items()

    assert query(m, ["D", S.LAST]) == 4
    assert query(m, ["A", S.LAST]) == ("B3", 3) # last element from dict.items()
    
#### Nth    
Navigate to the Nth element

    assert query(m, ["D", (S.NTH, 1)]) == 2
    assert query(m, ["D",(S.NTH, 1, 2)]) == [ 2, 3 ]
        
#### Operation on dict    
    
Navigate to `values` or `keys` of current position
        
    assert query(m, ["C", S.MVALS]) == [[1, 2], [3, 4]]
    assert query(m, ["C", S.MKEYS]) == ['B1', 'B2']

Navigate to a sub map of current position

    assert query(m, ["A", (S.SUB_MAP, "B1")]) == {"B1":[10,20]}

Annotate with index with current position
    
    assert query(m, ["A", S.INDEXED_VALS]) == [(0, ("B1", [10,20])), (1, ("B2", 2)), (2, ("B3", 3))]
    assert query(m, ["C", "B1", S.INDEXED_VALS]) == [(0, 1), (1, 2)]
    
#### Filtering    
    
filter elements by supplying a function

    assert query(m, ["A", "B1", (S.FILTER, lambda x: x > 10)]) == [20]
    assert query(m, ["C", (S.FILTER, lambda k, v: k.endswith("2"))]) == [[3, 4]]

Navigate to map which its key or value satisify a custom function 

    assert query(m, ["A", (S.MKEY_IF, lambda x:x.endswith("1"))]) == [[10, 20]]
    assert query(m, ["A", (S.MVAL_IF, lambda x:x==[10,20])]) == [[10, 20]]
    
#### Conditional Navigation

Navigate to a specifie path

    assert query(m, ["D", (S.NTH_PATH, 2)]) == [3]

Navigate to a position if and only if the path exists

    assert query(m, [(S.MUST,"F","G")]) == 1
    assert query(m, [(S.MUST,"F","G","NOT_EXISTS")]) == None 

Navigate to a range

    assert query(m, ["D",(S.SRANGE,2,3)]) == [3]

Navigate to a `2nd path`  if `1st path` exists, else return `None`

    assert query(m,[(S.IF_PATH,["C","B1"],["E"])]) == [None,2,3,4]
    assert query(m,[(S.IF_PATH,["C","B1"],["NOT_EXISTS"])]) == None

Navigate to a `2nd path`  if `1st path` exists, else navigate to `3rd path`

    assert query(m,[(S.IF_PATH,["C","B3"],["E"],["F"])]) == {'G': 1}

Navigate to values of dict if key satisfy a regex expression:

    assert query(m, ["A",(S.REGEX,r"B[23]")]) == [ 2,3 ]

Navigate to values of list if elements satisfy a regex expression:

    assert query(m, ["H",(S.REGEX,r"\S1")]) == [ "A1" ]

Navigate with optional path node 

    assert query(m, [(S.MAYBE,"F","G")]) == 1

#### Handling None value

Return default value if current position is `None`

    assert query(None,[(S.NONE_VAL,10)]) == 10

If current position is not a None,then return the value of current position

    assert query(5,[(S.NONE_VAL,10)]) == 5
    
    

    
