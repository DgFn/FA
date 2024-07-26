from database.engine import Session, engine
from database.models import User, Base
from repositories.users import get_users

def main():
    new_user = User(login='puska')

    with Session() as session:
        session.add(new_user)
        session.commit()

        users = get_users(session)

        print(users)


if __name__ == '__main__':
    main()