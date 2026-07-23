class AuditService:


    logs=[]


    def record(
        self,
        data
    ):

        self.logs.append(data)

        return {

            "recorded":True

        }



    def history(self):

        return self.logs



service=AuditService()
