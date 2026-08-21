class FormEngine:


    def generate(self,form):

        return {
            "form":form,
            "fields":[]
        }



    def validate(self,data):

        return {
            "valid":True,
            "errors":[]
        }



engine=FormEngine()
