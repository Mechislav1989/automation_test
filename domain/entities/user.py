from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str

    def __post_init__(self):
        if not self.username:
            raise ValueError("Name cannot be empty")
        if not self.password:
            raise ValueError("Password cannot be empty")