class ConfigService:


    cache={}



    def set(
        self,
        key,
        value
    ):

        self.cache[key]=value


        return {

            "saved":True,

            "key":key

        }



    def get(
        self,
        key
    ):

        return self.cache.get(key)



service=ConfigService()
