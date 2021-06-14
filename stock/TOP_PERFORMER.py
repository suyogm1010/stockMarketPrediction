import matplotlib.pyplot as plt
y = [30,40,50,60,10,30,40,50,80,70,90,60]
Z = [505,540,450,660,710,530,440,650,580,570,690,660]
x=[1,2,3,4,5,6,7,8,9,10,11,12]
plt.plot(x,Z , label="Y-axis=>Units",color='green', linewidth=2,marker='o', markerfacecolor='green', markersize=12)
plt.xlabel('Months')
# naming the y axis
plt.ylabel('Unit Consumption')
plt.legend()
plt.show()


#Max the Ratio Top the Performer
P = sum(Z[:int(len(Z)/2)])
Q = sum(Z[int(len(Z)/2):])
Q/P
P/Q




F = sum(y[:int(len(y)/2)])

S = sum(y[int(len(y)/2):])


S/F
F/S




DICT = {"IT":{"A":1.2,"B":1.27,"C":1.90,"D":1.45,"E":1.21,"F":1.67},"FIN":{"G":1.72,"H":1.47,"I":1.40,"J":1.55,"K":1.43,"L":1.90}}


DICT["IT"]

v = {"A":1.2,"B":1.27,"C":1.90,"D":1.45,"E":1.21,"F":1.67}

sorted(v)

dat = []
for  keys in v:
    #print(keys)
    print(v[keys])
    dat.append(v[keys])
    
    
print(sorted(v.values()))

dat = sorted(v.values())
o = 1.2
for n in v:
    print(n)
    
    if v[n]==o:
        print(n)
    

for n in v:
    #print(n)
    for jk in dat:    
        if v[n]==jk:
            print(n)



        
got = [n for n in v]

got = [i for i in range(1,6)]


from collections import OrderedDict 

dict = {'ravi':10,'rajnish':9,'sanjeev':15,'yash':2,'suraj':32} 

dict1 = OrderedDict(sorted(dict.values())) 

print(dict1) 


# creating a new dictionary 
my_dict = {"A":1.2,"B":1.27,"C":1.90,"D":1.45,"E":1.21,"F":1.67}


# list out keys and values separately 
key_list = list(my_dict.keys()) 
val_list = list(my_dict.values()) 
  
print(key_list[val_list.index(o)]) 
my_dict.keys()[my_dict.values().index(o)]
print(key_list[val_list.index(112)]) 
  
list(v.keys())[list(v.values()).index(o)]

# one-liner 
print(list(my_dict.keys())[list(my_dict.values()).index(o)])