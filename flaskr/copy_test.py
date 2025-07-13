# importing copy module 
import copy 
  
# initializing list 1  
li1 = [1, 2, [3,5], 4] 
  
# using deepcopy for deepcopy   
li3 = copy.deepcopy(li1)
li3[2][0] = 7
print ("The original elements after deep copying") 
for i in range(0,len(li1)): 
    print (li1[i],end=" ") 

print ("")  
# using copy for shallow copy   
li2 = copy.copy(li1)  
li2[2][0] = 7
print ("The original elements after shallow copying") 
for i in range(0,len(li1)): 
    print (li1[i],end=" ") 

