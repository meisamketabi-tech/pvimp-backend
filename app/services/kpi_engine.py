class KPIEngine:


    def calculate(self,data):

        inspections=data.get(
            "inspections",
            0
        )

        violations=data.get(
            "violations",
            0
        )


        compliance=100


        if inspections:
            compliance=(
                (inspections-violations)
                /
                inspections
            )*100


        return {
            "inspection_count":inspections,
            "violation_count":violations,
            "compliance_rate":round(compliance,2)
        }


engine=KPIEngine()
