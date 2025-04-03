from random import random as rand
from random import randint
from math import sqrt
from matplotlib import pyplot as plt
from scipy.stats.qmc import Sobol
##### INPUT #####
N_points=200

N_dim=3
n_neighbors=N_dim+2

lims=[[-5,5],[-5,5],[-5,5]]
fname='links.csv'
##### ENDINPUT #####
def is_prime(n):
	for i in range(2,n):
		if n % i == 0:
			return False
		if i**2>n:
			return True
	return True

def gen_primes(N):
	primes=[]
	i=1
	while len(primes)<N:
		if is_prime(i):
			primes.append(i)
		i+=1
	
	
	return primes
primes=gen_primes(N_points)


X=[[] for _ in range(N_dim)]
if False:
	points=[[rand() for _ in range(2)] for _ in range(N_points)]
elif False:
	points = []
	for i in range(N_points):
		point=[]
		for k in range(N_dim):
			x=randint(0,N_points)
			while x in X[k]:
				x=randint(0,N_points)
			X[k].append(x/N_points)
			point.append(x/N_points)
		points.append(point)
elif True:
	S=Sobol(N_dim)
	points=S.random(N_points)

for point in points:
	for i in range(N_dim):
		point[i]=point[i]*(lims[i][1]-lims[i][0])+lims[i][0]

ids=[i for i in range(N_points)]
fig = plt.figure
if N_dim==3: ax=plt.axes(projection='3d')

letters='xyzuvwabcdefghijklmnopqrst'
if N_dim<len(letters):
	data=open(fname,'w')
	for i in range(2):
		for k in range(N_dim):
			data.write(letters[k]+str(i)+'\t')
	data.write('\n')

links=[]
for i in range(N_points):
	r=[]
	for j in range(N_points):
		if i==j: r.append(1e308)
		else:
			R=0
			for k in range(N_dim):
				R+=(points[i][k]-points[j][k])**2
				
			r.append(sqrt(R))
	id_sort=[id for _,id in sorted(zip(r,ids))]
	for k in range(n_neighbors):
		pointi=points[i]
		pointk=points[id_sort[k]]
		
		if primes[i]*primes[k] in links: continue
		
		links.append(primes[i]*primes[k])
		
		if N_dim==2:
			plt.plot([pointi[0],pointk[0]],[pointi[1],pointk[1]],'b-')
		elif N_dim==3:
			plt.plot([pointi[0],pointk[0]],[pointi[1],pointk[1]],[pointi[2],pointk[2]],'b-',lw=0.5)
		if N_dim<len(letters):
			for m in range(N_dim):
				data.write(str(pointi[m]))
				data.write('\t')
			for m in range(N_dim):
				data.write(str(pointk[m]))
				data.write('\t')
			data.write('\n')
		
if N_dim==2:		
	plt.plot([point[0] for point in points],[point[1] for point in points],'k.')
if N_dim==3:		
	plt.plot([point[0] for point in points],[point[1] for point in points],[point[2] for point in points],'k.',ms=1)
plt.show()

data.close()