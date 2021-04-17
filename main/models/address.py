from config import default_country_name
class Address :
    """stores user address information"""
    def __init__(self,id,line1,state,postal_code,city,line2=None,country=default_country_name):
        self.id=id
        self.line1=line1
        self.line2=line2
        self.city=city
        self.postal_code=postal_code
        self.state=state
        self.country=country
        

