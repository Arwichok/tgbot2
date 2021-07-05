from sqlalchemy.orm import declared_attr, as_declarative


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower() + 's'
