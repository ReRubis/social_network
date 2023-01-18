from pydantic import BaseModel


class text_post(BaseModel):
    text: str


class which_reaction(BaseModel):
    '''Either like, either dlike'''
    reaction: str
