import numpy as np
import difflib  

urls = ["www.hackprinceton.com", "www.reddit.com","www.google.com", "www.okcupid.com"]

def auto_correct(url):
    res = difflib.get_close_matches(url,urls,n=1)
    if len(res) > 0:
        return res[0]
    else:
        if len(url) > 4:
            url = url.replace(" ","")
            if not(url[:4] == "."):
                url = url[:3] + "."+ url[3:]
            if url[-4] == ".":
                url = url[:-4] + "."+url[-4:]
    return url 
            




