import uuid
from sqlmodel import SQLModel, Field

class WordBase(SQLModel):
    hanzii: str = Field(unique=True, min_length=1, max_length=16, description="Chinese character(s)")
    meaning: str | None = Field(default=None, max_length=255, description="Meaning or gloss")
    pinyin: str | None = Field(default=None, max_length=64, description="Pinyin transcription")
    
    
class Word(WordBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    
class WordCreate(WordBase):
    pass


class WordUpdate(WordBase):
    hanzii: str = Field(default=None, min_length=1, max_length=16)
    meaning: str | None = Field(default=None, max_length=255)
    pinyin: str | None = Field(default=None, max_length=64)
    

class WordPublic(WordBase):
    id: uuid.UUID
    

class WordsPublic(SQLModel):
    data: list[WordPublic]
    count: int