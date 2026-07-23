class WorkOrderService:


    def create(
        self,
        data
    ):

        return {

            "created":True,

            "order":data

        }



    def assign(
        self,
        order_id,
        user_id
    ):

        return {

            "assigned":True,

            "order_id":order_id,

            "user_id":user_id

        }



service=WorkOrderService()
