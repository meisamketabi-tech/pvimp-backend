class SearchService:


    def index(
        self,
        data
    ):

        return {

            "indexed":True,

            "data":data

        }



    def search(
        self,
        keyword
    ):

        return []



service=SearchService()
