
class Payment :
     def __init__(
         self,amount,payment_mode='cash',
         payment_date=None,nb_bank_check=None,
         transaction_number=None,card_number=None,
         payor_last_name=None,payor_name=None):
        self.amount=amount
        self.Payment_mode=payment_mode
        self.payment_date=payment_date
        self.nb_bank_check=nb_bank_check
        self.transaction_number=transaction_number
        self.card_number=card_number
        self.payor_last_name=payor_last_name
        self.payor_name=payor_name
   
   