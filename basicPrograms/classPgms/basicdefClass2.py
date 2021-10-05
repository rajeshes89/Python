import basic_pgm_with_class

#The following is the input for prime and fib series

input_value = raw_input("Enter :")
obj = basic_pgm_with_class.basic(input_value)
data = obj.prime()

if data : 
    print "Given number",input_value, "is not prime"
else :
    print "Given number ",input_value,"is prime"

data1 = obj.fib()

print "Fib series is ",data1

#Input for palindrome

string = raw_input("Enter :")
obj1 = basic_pgm_with_class.basic(str(string))
data2 = obj1.reverse()

print data2, "is the reverse"
if data2 == string :
    print "Given value is a palindrome"
else :
    print "Given value is not a palindrome"


#input for factorial

fact_var = raw_input("Enter fact value :")

obj2  = basic_pgm_with_class.basic(int(fact_var))
print obj2.factorial()



    
