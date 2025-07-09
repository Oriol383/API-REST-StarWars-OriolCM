from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean, ForeignKey, Table, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

user_planet_fav = Table(
    "user_planet_fav",
    db.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("planet_id", Integer, ForeignKey("planet.id"), primary_key=True)
)

user_character_fav = Table(
    "user_character_fav",
    db.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("character_id", Integer, ForeignKey("character.id"), primary_key=True)
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    sub_date: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))

    favorite_planets = relationship("Planet", secondary=user_planet_fav, back_populates="users_who_favorited")
    favorite_characters = relationship("Character", secondary=user_character_fav, back_populates="users_who_favorited")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "is_active": self.is_active,
            "sub_date": self.sub_date,
            "name": self.name,
            "last_name": self.last_name
        }

class Planet (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    solar_system: Mapped[str] = mapped_column(String(60))

    users_who_favorited = relationship("User", secondary=user_planet_fav, back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "solar_system": self.solar_system
        }

class Character (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(120))
    race: Mapped[str] = mapped_column(String(120))
    native_planet: Mapped[str] = mapped_column(String(60))
    is_jedi: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    users_who_favorited = relationship("User", secondary=user_character_fav, back_populates="favorite_characters")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "race": self.race,
            "native_planet": self.native_planet,
            "is_jedi": self.is_jedi
        }

class Fav (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_owner: Mapped[str] = mapped_column(String(60))
    caption: Mapped[str] = mapped_column(String(240))
    timestamp: Mapped[int] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "post_owner": self.post_owner,
            "caption": self.caption,
            "timestamp": self.timestamp
        }

class Weapon (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(120))
    name: Mapped[str] = mapped_column(String(120))
    is_lethal: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    weapon_owner_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)

    owner = relationship("Character", backref="weapons")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name, 
            "is_lethal": self.is_lethal,
            "weapon_owner_id": self.weapon_owner_id
        }