from fastapi import APIRouter, Depends
from lib.dictionary_req import dictionary_present
dictionary = APIRouter()

@dictionary.post("/dictionary")
def present(response):
    return dictionary_present(response)

