from app.security.permission_engine import engine


def has_access(
    role,
    permission
):

    return engine.check(
        role,
        permission
    )
