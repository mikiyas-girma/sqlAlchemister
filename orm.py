from sqlalchemy import (create_engine, String, Integer,
                        Column, func, ForeignKey, or_,
                        Sequence, join)
from sqlalchemy.orm import (declarative_base, sessionmaker, relationship,
                            Mapped, mapped_column, joinedload)

engine = create_engine(
    'postgresql://postgres:Mm1122@localhost:5432/school', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column()

    addresses = relationship("Address", backref="user",
                             cascade="all, delete-orphan")

    def __repr__(self):
        return "<User(name='%s', fullname='%s')>" % (
            self.name, self.fullname
        )


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


# user1 = User(name="Alice", fullname="Alice Boe")
# address1 = Address(email="alice@example.com", user=user1)
# address2 = Address(email="ali2@gmail.com", user=user1)

# # You can create more users and addresses here
# user2 = User(name="Bob", fullname="Bob maron")
# address2 = Address(email="bob@example.com", user=user2)

# session.add_all([user1, user2])
# session.commit()


user = session.query(User).join(Address, User.id == Address.user_id).first()

# if user:
#     print(f"User: {user.name}")
#     for address in user.addresses:
#         print(f"\tEmail: {address.email}")
# else:
#     print("User not found")

user1 = session.query(User).filter(User.id == 3).first()
print(user1)
session.delete(user1)
session.commit()

# users = session.query(User).options(joinedload(User.addresses)).all()

# for user in users:
#     print(f"User: {user.name}")
#     for address in user.addresses:
#         print(f"\tEmail: {address.email}")
