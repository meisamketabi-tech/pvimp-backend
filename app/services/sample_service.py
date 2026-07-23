class SampleService:


    def register(
        self,
        data
    ):

        return {

            "registered":True,

            "sample":data

        }



    def result(
        self,
        sample_id
    ):

        return {

            "id":sample_id,

            "result":"pending"

        }



service=SampleService()
