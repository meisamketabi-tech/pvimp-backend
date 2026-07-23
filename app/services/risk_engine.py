class RiskEngine:


    def calculate(
        self,
        data
    ):

        score=0


        if data.get("violation_count",0)>0:

            score+=50


        if data.get("history_bad"):

            score+=30


        if data.get("complaint"):

            score+=20



        level="LOW"


        if score>=70:

            level="HIGH"

        elif score>=40:

            level="MEDIUM"



        return {

            "score":score,

            "level":level

        }



engine=RiskEngine()
