### Lambda (anonymous) functions ###
#purpose --> create a small anonymous function without a name, throwaway functions
#that are just needed where they have been created, mainly used in combo with
#filter(), map(), reduce() and sort(). create and use a function in a single line,
#only need to use once.


def f(x):
    return 3*x + 1

print f(2)



#'lambda' then 'inputs' then ':' then 'what the function does, expression of return value'
#cannot use lambda expressions for multi-line functions
g = lambda x: 3*x + 1

print g(2)



#Combine first and last name into single full name

fullName = lambda fn, ln: fn.strip().title() + " " + ln.strip().title()

print fullName("    leo", "MESSI     ")




#lambda expression with no name

scifi_authors = ["Isaac Asimov", "ay Bradbury", "Robert Heinlein", "Arthus C. Clarke",
                 "Frank Herbert", "Orson Scott Card", "Douglas Adams", "H. G. Wells",
                 "Leigh Brackett"]

scifi_authors.sort(key = lambda name: name.split(" ")[-1].lower())
print scifi_authors




#lambda function within a function

def build_quadratic_function(a, b, c):
    #returns the function f(x) = ax^2 + bx + c
    return lambda x: a*x**2 + b*x + c

f = build_quadratic_function(2, 3, -5)
print f(0)
print f(1)
print f(2)

print build_quadratic_function(3, 0, 1)(2) #3x^2+1 evaluated for x=2



 
