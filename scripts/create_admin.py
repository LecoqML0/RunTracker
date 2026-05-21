import sys

from app.db.session import get_session
from app.schemas.user import UserDB
from app.security import hash_password

def create_admin(email: str, password: str):
    for session in get_session():
        user = UserDB(
            email=email,
            hashed_password=hash_password(password),
            is_admin=True,
            username = "admin"
        )
        session.add(user)
        session.commit()

if __name__ == "__main__":
    create_admin(sys.argv[1], sys.argv[2])