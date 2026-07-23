class TaskService:


    tasks=[]


    def create(
        self,
        data
    ):

        self.tasks.append(data)

        return {

            "created":True,

            "task":data

        }



    def list(self):

        return self.tasks



    def update(
        self,
        task_id,
        data
    ):

        return {

            "updated":True,

            "id":task_id,

            "data":data

        }



service=TaskService()
