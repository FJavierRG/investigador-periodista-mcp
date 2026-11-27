from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from rich import print
import logging

load_dotenv()
GROQ_API_KEY= os.getenv("GROQ_API_KEY")
logger = logging.getLogger(__name__)

class QueryGenerator(BaseModel):
    querys: list[str]


def generate_mc_query(user_input: str)-> list[str]:
    model=ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.5,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
    )
    model=model.with_structured_output(QueryGenerator, include_raw=True)

    logger.info(f"Query generator: Mensaje del usuario {user_input}")

    messages = [
        ('system', ' Eres un agente especializado en crear querys a partir de una petición humana de lenguaje natural, para Media Cloud.'
        'Media Cloud utiliza búsquedas léxicas con operadores booleanos, no búsquedas semánticas en lenguaje natural'
        'La sintaxis que admite Media Cloud es la siguiente:'
        'AND	:Exige ambos términos.'
        'OR	:Exige al menos uno.'
        'NOT	:Excluye un término.'
        '"texto"	:Busca una frase literal. Concatenar varias palabras bajo comillas literales disminuye exponencialmente la'
        'probabilidad de encontrar un resultado que encaje.'
        'text*	:Busca distintas terminaciones.'
        '(A OR B)	:Agrupa condiciones.'
        '"texto"~5	:Busca términos próximos entre sí.'
        'article_title:Texto	:Busca únicamente en titulares.'
        'Debes generar una única query.'
        'Debes generar una query para buscar información sobre el hecho subyacente a la afirmación del usuario, no la petición de este'
        'de manera literal.'
        'Un sistema automático posterior utilizará la consulta como fuente de una investigación periodística con el objetivo de saber'
        'si el usuario afirma o no un bulo.'
        'Por ello las búsquedas no deben reflejar la hipótesis del usuario, a fin de evitar información sesgada, sino buscar'
        'información relativa al hecho, acontecimiento o afirmación.'),
        ('user', user_input)
    ]

    response = model.invoke(messages)
    logger.info(response['raw'].usage_metadata)
    return response

if __name__ == "__main__":
    query = generate_mc_query("El accidente de Urda fue culpa de un error humano")
    print(query['raw'].usage_metadata)
    print(query['parsed'].querys)
