class TemplateService:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "template":data

        }



    def render(
        self,
        template,
        values
    ):

        return {

            "template":template,

            "values":values

        }



service=TemplateService()
