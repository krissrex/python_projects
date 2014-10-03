def euler(a,b):
    """Iterative Euler algorithm."""
    x = a
    y = b
    r = 0
    if x<y:
        x,y = y,x
        
    while y != 0:
        r = x % y
        print ("{0} = {1}*{2} + {3}".format(x,y,x//y,r))
        x = y
        y = r

    print ("Gcd({0}, {1}) is {2}".format(a,b,x))

def gcdr(a, b):
    """Recursive Greatest Common Divisor algorithm."""
    if b == 0:
        return a
    if a<b:
        a,b = b,a
    print(a,b)
    return gcdr(b, a%b)

if __name__ == "__main__":
    # Sample data
    print(gcdr(1001, 1331))
    print()
    euler(1001, 1331)
    print()
    euler(1234,54321)
