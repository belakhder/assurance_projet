class Contract :
 
    def __init__(self,id,price,contract_type,creation_date=None,start_date=None,end_date=None,status="pending"):
        self.id=id
        self.creation_date=creation_date
        self.start_date=start_date
        self.end_date=end_date
        self.price=price
        self.contract_type=contract_type
        self.status=status
        