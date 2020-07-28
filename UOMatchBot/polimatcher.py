import numpy as np

def product(factors):
	o=factors[0]
	for i in factors[1:]:
		o=o*i
	return o

def pm(M,V,min=3,N=1000,t=0,L=[],e=0):
	if sum([M[i,j] for i in V for j in V])==len(V)**2 and sum(M[V,V])==len(M[V,V]):
		if t==0:
			if V==[]:
				L=[[n,m] for n in range(len(M)) for m in range(1,len(M)) if m>n and M[n,n]==1 and M[m,m]==1 and M[n,m]==1]
			else:
				L=[V+[n] for n,kk in enumerate(product([M[f,:] for f in V])) if kk==1 and M[n,n]==1 and not n in V]
			return pm(M,V,min,N,1,L,0)
		else:
			LL=[]
			while e<len(L):
				LL+=[L[e]+[n] for n,kk in enumerate(product([M[f,:] for f in L[e]])) if kk==1 and M[n,n]==1 and not n in L[e] and n>L[e][-1] and len(L[e]+[n])<N+1]
				e+=1
			if len(LL)>0:
				return pm(M,V,min,N,1,L+LL,e)
			else:
				return [i for i in L if len(i)>=min]
	else:
		return L

#np.random.seed(1)
m=np.random.randint(2,size=(10,10))
M=m*m.T
print(M)
for i in pm(M,[],3):
	print(i)

