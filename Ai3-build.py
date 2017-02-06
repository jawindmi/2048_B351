import random
dic = open("Ai3.txt", 'w')
#opens the dictionary of moves
di = {}
#creates new dictionary

values = [0, 2]
moves = ['w', 's', 'a', 'd']


for a in values:
    for b in values:
        for c in values:
            for d in values:
                for e in values:
                    for f in values:
                        for g in values:
                            for h in values:
                                for i in values:
                                    for j in values:
                                        for k in values:
                                            for l in values: 
                                                for m in values:
                                                    for n in values:
                                                        for o in values:
                                                            for p in values:
                                                                matrix=str([[a,b,c,d],[e,f,g,h],[i,j,k,l],[m,n,o,p]])
                                                                print matrix
                                                                di[matrix]=random.choice(moves)
                                                                
                                                    




dic.write(str(di))
dic.close()
#writes out and closes the dictionary