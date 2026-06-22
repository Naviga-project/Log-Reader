light = "green"

if (light=="green"):
    print("go")

elif ( light=="yellow"):
 print("slow down")

elif (light=="red"): 
   print("stop")


num=int(input("enter no."))

rem= num%2
if (rem==0):
   print("even")

else:
   print("odd")



   a =int(input("enter the no."))
   b=int(input("enter the no."))  

   c =int(input("enter the no."))
if(a>=b and a>=c):
   print("larger",a)
elif(b>=a,b>=c):
   print("more large",b)
else:
   print("more more lRGER",c)



   
marks=[89.8,98.9,56.8,45.8]
print(marks)
print(len(marks))
print(marks[2])
print(marks[3])



marks=[23.3,43.5,65.6,76.9]
print((marks[:4]))

marks=[23.4,45.6,34.5,56.7]
print(marks[1:])


list =["hi","pli","asi"]
print(list.sort())
print(list)
# print(list.append(5))
print(list.sort(reverse=True))


list=[2,3,4]
list.pop(2)
print(list)
