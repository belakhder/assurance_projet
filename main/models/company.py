
from main.models.address import Address


class Company:
    def __init__(self,id,company_name,company_email,company_tel,address,company_registration_nb,company_type='Client Potentiel'):
        
        self.id=id
        self.company_name=company_name
        self.company_email=company_email
        self.company_tel=company_tel
        self.company_registration_nb=company_registration_nb
        self.company_type=company_type
        self.address=address

        # check adddress validity
 
        if isinstance (address,Address):
            self.address=address
        else:
            raise TypeError('invalide type')



        # add address or modify address
    def add_address(self,address):
        if isinstance (address,Address):
            self.address=address
        else:
            raise TypeError('invalide type')








