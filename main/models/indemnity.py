from datetime import date
class Indemnity :
     def __init__(
         self,
         sinister_id,
         client_id,
         amount=0,creation_date=None,refund_status='not made'):
        self.sinister_id=sinister_id
        self.amount=amount
        self.creation_date=creation_date
        self.refund_status=refund_status

        
        #check amount validity
        if isinstance(amount,float) or isinstance(amount,int) :
            self.amount=amount 
        else:
            raise Exception('invalid type')
    

