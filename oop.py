class Program:
    def __init__(self,*args,**kwargs):
        print(**kwargs)
        
p1 = Program(12,13)        