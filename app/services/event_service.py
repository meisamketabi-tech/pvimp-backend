class EventService:


    events=[]


    def publish(
        self,
        data
    ):

        self.events.append(data)

        return {

            "published":True,

            "event":data

        }



    def stream(self):

        return self.events



service=EventService()
