from sqlalchemy.orm import Session

from app.db.models.organization import OrganizationUnit
from app.db.models.assignment import UserAssignment
from app.db.models.organization_unit_position import OrganizationUnitPosition



def build_tree(
    db: Session,
):

    units = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.is_active == True
        )
        .all()
    )


    nodes = {}

    roots = []


    for unit in units:


        assignments = (
            db.query(UserAssignment)
            .filter(
                UserAssignment.organization_unit_id == unit.id,
                UserAssignment.is_active == True,
            )
            .all()
        )


        positions = (
            db.query(OrganizationUnitPosition)
            .filter(
                OrganizationUnitPosition.organization_unit_id == unit.id,
                OrganizationUnitPosition.is_active == True,
            )
            .all()
        )


        primary_user = None

        for assignment in assignments:

            if assignment.is_primary:

                primary_user = {
                    "id": assignment.user.id,
                    "username": assignment.user.username,
                    "full_name": assignment.user.full_name,
                    "role": assignment.role.name,
                }

                break



        nodes[unit.id] = {

            "id": unit.id,

            "name": unit.name,

            "code": unit.code,

            "type_id": unit.type_id,

            "level_id": unit.level_id,


            "manager": primary_user,


            "statistics": {

                "users_count": len(assignments),

                "positions_count": len(positions),

            },


            "positions": [

                {
                    "id": p.organization_position.id,
                    "title": p.organization_position.title,
                }

                for p in positions

            ],


            "users": [

                {
                    "id": a.user.id,
                    "username": a.user.username,
                    "full_name": a.user.full_name,
                    "role": a.role.name,
                    "is_primary": a.is_primary,
                }

                for a in assignments

            ],


            "children": [],

        }



    for unit in units:


        node = nodes[unit.id]


        if unit.parent_id:


            parent = nodes.get(unit.parent_id)


            if parent:

                parent["children"].append(node)


        else:

            roots.append(node)



    return roots