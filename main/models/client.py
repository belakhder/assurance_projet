from main.models.profile import Profile
from main.models.address import Address


class Client(Profile):
    def __init__(self,id,name,last_name,email,tel,address,client_type='Client Potentiel'):
        super().__init__(name,last_name,email,tel)
        self.id=id
        self.client_type=client_type
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








