
class Instalment :
     def __init__(
         self,amount,due_date,Payment_mode='',payment_date='',status="en attente"):
        self.amount=amount
        self.due_date=due_date
        self.Payment_mode=Payment_mode
        self.payment_date=payment_date
        self.status=status
   
   