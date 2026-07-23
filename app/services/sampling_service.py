class SamplingService:


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

            "sample_id":sample_id,

            "status":"pending"

        }



service=SamplingService()
