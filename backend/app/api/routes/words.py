import uuid
from typing import Any
from fastapi import APIRouter, HTTPException

from ..models import Word, WordCreate, WordPublic, WordUpdate, WordsPublic

words_db: dict[str, dict] = {}

router = APIRouter(prefix="/words", tags=["words"])


@router.get("/", response_model=WordsPublic)
def read_words(skip: int = 0, limit: int = 100) -> Any:
    words = list(words_db.values())[skip : skip + limit]
    return WordsPublic(data=words, count=len(words_db))


@router.get("/{id}", response_model=WordPublic)
def read_word(id: str) -> Any:
    word = words_db.get(id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found!")
    
    return word


@router.post("/", response_model=WordPublic)
def create_word(word_in: WordCreate) -> Any:
    word_id = str(uuid.uuid4())
    new_word = Word.model_validate(word_in, update={"id": word_id})
    words_db[word_id] = new_word.model_dump()
    return new_word


@router.put("/{id}", response_model=WordPublic)
def update_word(id: str, word_in: WordUpdate) -> Any:
    word = words_db.get(id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found!")

    updated_data = {**word, **word_in.model_dump(exclude_unset=True)}
    words_db[id] = updated_data
    return updated_data


@router.delete("/{id}")
def delete_word(id: str) -> dict[str, str]:
    if id not in words_db:
        raise HTTPException(status_code=404, detail="Word not found")
    
    del words_db[id]
    return {"message": "Word deleted successfully"}