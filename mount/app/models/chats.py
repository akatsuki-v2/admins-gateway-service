from app.models import BaseModel


class Chat(BaseModel):
    chat_id: int
    name: str
    topic: str
    read_privileges: int
    write_privileges: int
    auto_join: bool
