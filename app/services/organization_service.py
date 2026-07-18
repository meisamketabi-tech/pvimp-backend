from sqlalchemy.orm import Session

from app.db.models.organization import OrganizationUnit


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

        nodes[unit.id] = {
            "id": unit.id,
            "name": unit.name,
            "code": unit.code,
            "type_id": unit.type_id,
            "level_id": unit.level_id,
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
