def string_compare(*srings):
    res = list(srings)
    res.sort(reverse=True)
    return res

def float_compare(*srings):
    res = list(srings)
    res.sort(reverse=True)
    return res




if __name__ == '__main__':
    a = ''
    b = ''
    c = ''
    d = ''
    print(string_compare(a,b,c,d))
