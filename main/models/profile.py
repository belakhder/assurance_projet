
class Profile :
    
    def __init__(self,name,last_name,email,tel):
        self.name=name
        self.last_name=last_name
        self.email=email
        self.tel=tel
        


        # check name validity
        if isinstance (name,str):
            self.name=name
        else:
            raise TypeError('invalid type')

        # check last_name validity
        if isinstance (last_name,str):
            self.last_name=last_name
        else:
            raise TypeError('invalid type')
        
        #check email validity
        if isinstance (email,str):
            self.email=email 
        else:
            raise TypeError('invalid type')

        #check tel validity
        if isinstance(tel,str):
            self.tel=tel
        elif isinstance(tel,int):
            self.tel=str(tel)
        else:
            raise Exception('invalid number of telephone')
    


        


