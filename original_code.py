import math

def calculate_area(r):
    pi = 3.14
    radius = r
    if r < 0:
       print("radius can't be negative")
       return
    area = pi*r*r  
    return area

def main():
   x = 10
   y = 0 # unused variable
   print("area is:",calculate_area(x))
   print("area of -5:", calculate_area(-5))
   print("done")

main()
