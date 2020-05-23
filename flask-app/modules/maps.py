from googlesearch import search
import google

def getWeb(name):
    url = search(name, tld="co.in", num=1)
    return next(url) #generator object get next value