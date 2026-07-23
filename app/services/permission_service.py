class PermissionService:


    def check(
        self,
        role,
        resource,
        action
    ):

        return {

            "allowed":True,

            "role":role,

            "resource":resource,

            "action":action

        }



    def role_permissions(
        self,
        role
    ):

        return []



service=PermissionService()
