class CaesarCreateTables:
    def __init__(self) -> None:
        self.caesaraiworldmodelsfields = ("filename","model")
        

    def create(self,caesarcrud):
        caesarcrud.create_table("modelid",self.caesaraiworldmodelsfields,
        ("varchar(255) NOT NULL","LONGBLOB"),
        "caesaraiworldmodels")

