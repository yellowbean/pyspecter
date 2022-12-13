# pyspecter
A library query on nested structure, inspired by [specter](https://github.com/redplanetlabs/specter)

## Samples

    m = {"A":{"B1":1,"B2":2},
         "C":{"B1":[1,2],"B2":[3,4]}
         ,"D":[1,2,3,4]}
 

    query(m,["A", "B1"])
    # 1 
    
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
