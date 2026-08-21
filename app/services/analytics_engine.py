class AnalyticsEngine:


    def summarize(
        self,
        data
    ):

        total=len(data)

        value=sum(
            item.get("value",0)
            for item in data
        )


        return {

            "count":total,

            "total":value,

            "average":
            round(
                value/total,
                2
            ) if total else 0

        }



engine=AnalyticsEngine()
