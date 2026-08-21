class PermissionEngine:


    def check(
        self,
        user_role,
        permission
    ):

        matrix={

            "admin":[
                "all"
            ],

            "manager":[
                "dashboard",
                "reports",
                "inspection"
            ],

            "inspector":[
                "inspection",
                "sampling"
            ],

            "responsible_health":[
                "forms",
                "inspection"
            ]

        }


        allowed=matrix.get(
            user_role,
            []
        )


        return (
            "all" in allowed
            or
            permission in allowed
        )


engine=PermissionEngine()
