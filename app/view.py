from shortcuts import render

def index(requset):
    return render(requset,"./template/test.html",{'name': 'Johnny', 'numbers':[0, 1, 2]})
