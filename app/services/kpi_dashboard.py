class KPIDashboard:


    def calculate(
        self,
        data
    ):

        result={}


        for item in data:

            target=item.get(
                "target",
                1
            )

            value=item.get(
                "value",
                0
            )


            result[item.get("code")] = {

                "value":value,

                "achievement":
                round(
                    value/target*100,
                    2
                )

            }


        return result



engine=KPIDashboard()
