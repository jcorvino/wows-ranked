import random
import matplotlib.pyplot as plt


#configuration

bestplc=33
cutoff=3000
reqstars=55
winrate=50

#run to rank 1 (from12)

def onerun():
    battles=0
    stars=0
    while stars < reqstars:
        battles=battles+1
        if  random.randint(1,100)<= winrate:
            stars=stars+1
            if stars%2==0 and stars <=4:
                stars=stars+1
            elif stars%4==0 and stars <=24 and stars>4:
                 stars=stars+1
            elif stars%5==0 and stars>24:
                 stars=stars+1

        else:
            if random.randint(1,100) > bestplc and stars!=0:   #best player doesnt lose star + stats cant go below unrewocable
                stars=stars-1

        if battles > cutoff:
           break;

    return battles

#create dataset

s=[]
for i in range(0,100000):
    n=onerun()
    if n<cutoff-1:     #remove cutoff artifcat
        s.append(n)


#Draw

s.sort()
optbins=s[len(s)-1]-s[0]    #determines binnumber for 1:1 bins

f=plt.figure()
f.suptitle("Battles needed for going from Rank 12 to Rank 1:")
plt.title("Assuming 50% WR and 33% for keeping star when losing")
plt.hist(s,bins=optbins)
plt.xlabel('required Battles')
plt.ylabel('divide by 1000 to get %')

plt.savefig('filename.png', dpi=300)