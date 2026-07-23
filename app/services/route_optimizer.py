class RouteOptimizer:


    def optimize(
        self,
        units
    ):

        result=[]


        for index,unit in enumerate(units):

            result.append({

                "order":index+1,

                "unit":unit

            })


        return result



engine=RouteOptimizer()
