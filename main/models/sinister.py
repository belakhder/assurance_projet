from datetime import date
class Sinister :
     def __init__(
         self,description,
         opposing_insurer,
         amount,id=None,status='in progress',closing_date=None,creation_date=None,sinister_date=None):
        self.id=id
        self.sinister_date=sinister_date
        self.description=description
        self.creation_date=creation_date
        self.status=status
        self.closing_date=closing_date
        self.opposing_insurer=opposing_insurer
        self.amount=amount    


        # check description validity
        if isinstance (description,str):
            self.description=description
        else:
            raise TypeError('invalid type')

        # check creation_date validity
        # if creation_date is not None:
        #     if isinstance (creation_date,date):
        #         self.creation_date=creation_date
        #     else:
        #         raise TypeError('invalid type')
        
        # if closing_date is not None:
            
        #     if isinstance (closing_date,date):
        #         self.closing_date=closing_date
        #     else:
        #         raise TypeError('invalid type')
        #check status validity
        if isinstance (status,str):
            self.status=status 
            print(self.status)  
        else:
            raise Exception('invalid type')

        # check opposing_insurer validity
        if isinstance (opposing_insurer,str):
            self.opposing_insurer=opposing_insurer
        else:
            raise TypeError('invalid type')
        
        #check amount validity
        if isinstance(amount,float) or isinstance(amount,int) :
            self.amount=amount 
        else:
            raise Exception('invalid type')
    

