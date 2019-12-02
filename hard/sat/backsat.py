from randsat import formula
from bfsat import bfsolve
from copy import deepcopy
# literals  x_1 ...  x_n represented by  1  2 ...  n
# literals -x_1 ... -x_n represented by -1 -2 ... -n

# assignment vector is a string, one character per variable
# unsatisfiable if and only if empty string
UNKNOWN, FALSE, TRUE = '?', '0', '1'

def showf(f): 
  print('formula now has length', len(f))
  for j in f: 
    print(j)

def showfa(f, a):
  if f:
    print('unsatisfiable')
  else:
    print('solution', a)

def fixliteral(t, f, a): # in f, set literal t True, return updated a
  index = abs(t)-1
  assert(a[index]== UNKNOWN)
  new_a = a[:index] + (TRUE if (t>0) else FALSE) + a[index+1:]
  for clause in f[:]:
    clauseSat = False
    for literal in clause[:]:
      if literal == -t:
        clause.remove(literal)
        if len(clause)==0: # f unsat
          return ''
      elif literal == t: 
        clauseSat = True
    if clauseSat: f.remove(clause)
  return new_a

def mycopy(f,a):
  newa = a
  newf = []
  for clause in f: 
    newf.append(list(clause))
  return newf, newa

def sat(f): 
  return not f #  True iff  f is empty list

def unsat(a): 
  return not a # True iff a is empty string

def backsat(f,a):
  if unsat(a) or sat(f): 
    return f,a
  minj = f.index(min(f,key=len))  # clause with fewest literals
  if len(f[minj])==0:
    return f, ''
  if len(f[minj])==1: 
    a = fixliteral(f[minj][0], f, a)
    return backsat(f,a)
  #split: 2 possible bool. vals for literal f[minj][0]
  fcopy, acopy = mycopy(f,a)
  a = fixliteral(f[minj][0], f, a)  # f[minj][0] True
  f,a = backsat(f,a)
  if sat(f): 
    return f, a
  f,a = fcopy, acopy
  a = fixliteral(-f[minj][0], f, a) # f[minj][0] False
  return backsat(f, a)

def backsolve(n,myf):
  asn = UNKNOWN * n
  f,a = backsat(myf,asn)
  return f,a

#n,myf=6,[[-5,-6],[-3,5],[-2,5],[1,-6],[1,-4],[1,-3],[2,3],[2,6],[3,-5],[3,4],[4,-5],[5,-6]]
#n,myf=6,[[-4,-5,6],[-4,5,-6],[-2,4,-5],[-2,5,-6],[-1,-3,-4],[-1,-3,4],[-1,4,-6],[1,-4,5],[1,-3,-5],[1,-3,4],[1,5,-6],[2,5,6],[3,-5,-6],[4,-5,6],[4,5,-6],[4,5,6]]

#max m: (n choose k)(2^k)
#n, k, m = 20, 5, 400  # good example
#n, k, m = 30, 5, 100 # backtrack yes, bf too slow
n, k, m = 10, 3, 48  # good example

myf = formula(n,k,m)
#n,myf = 5, [[1,-5],[-2,-3],[3,4],[-4,-5],[2,5],[-1,-5]]
#n,myf = 5, [[1,-2],[1,3],[-2,-3],[2,4],[-3,-4],[3,-5],[3,5]]
myf2 = deepcopy(myf)
print('formula with', n, 'vars', m, 'clauses')
showf(myf)
print('')
f, a = backsolve(n, myf)
showfa(f, a)

print('\nverify with bfsolve')
bfsolve(n, myf2, True)
