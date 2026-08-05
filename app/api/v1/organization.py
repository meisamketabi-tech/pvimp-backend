@router.get("/{unit_id}")
def organization_detail(
    unit_id: int,
    db: Session = Depends(get_db),
    # user=Depends(
#     require_permission("VIEW_ORGANIZATION")
# ),
):

    from app.db.models.organization_responsibility import OrganizationResponsibility


    unit = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.id == unit_id
        )
        .first()
    )


    if not unit:

        raise HTTPException(
            status_code=404,
            detail="Organization unit not found",
        )


    positions = (
        db.query(OrganizationUnitPosition)
        .filter(
            OrganizationUnitPosition.organization_unit_id == unit.id,
            OrganizationUnitPosition.is_active == True,
        )
        .all()
    )


    users = (
        db.query(UserAssignment)
        .filter(
            UserAssignment.organization_unit_id == unit.id,
            UserAssignment.is_active == True,
        )
        .all()
    )


    responsibilities = (
        db.query(OrganizationResponsibility)
        .filter(
            OrganizationResponsibility.organization_unit_id == unit.id
        )
        .all()
    )


    children = (
        db.query(OrganizationUnit)
        .filter(
            OrganizationUnit.parent_id == unit.id,
            OrganizationUnit.is_active == True
        )
        .all()
    )


    return {

        "id": unit.id,

        "name": unit.name,

        "code": unit.code,

        "unit_type": unit.unit_type,

        "parent_id": unit.parent_id,


        "positions": [

            {
                "id": p.id,
                "position_id": p.organization_position.id,
                "position_code": p.organization_position.code,
                "position_title": p.organization_position.title,
                "assigned_users": 0,
            }

            for p in positions

        ],


        "users": [

            {
                "assignment_id": u.id,
                "user_id": u.user.id,
                "full_name": u.user.full_name,
                "role": u.role.name,
            }

            for u in users

        ],


        "responsibilities": [

            {
                "id": r.id,
                "title": r.title,
                "description": r.description,
                "priority": r.priority,
                "inspection_type_id": r.inspection_type_id,
                "inspection_type": r.inspection_type.title
                if r.inspection_type else None,
            }

            for r in responsibilities

        ],


        "children": [

            {
                "id": c.id,
                "name": c.name,
                "unit_type": c.unit_type,
            }

            for c in children

        ],

    }