from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import Literal
from rich import print

load_dotenv()
GROQ_API_KEY= os.getenv("GROQ_API_KEY")

class InputSystemValidator(BaseModel):
    input_validation: Literal['Accepted', 'Rejected']


def model_call(user_input: str)-> str:
    model=ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
    )
    model=model.with_structured_output(InputSystemValidator, include_raw=True)
    
    messages = [
        ('system','Determina si la entrada del usuario contiene una afirmación objetiva, suficientemente delimitada'
        'y susceptible de investigación.Rechaza las preguntas, las valoraciones puramente subjetivas y las peticiones' 
        'que no constituyan afirmaciones.'
        'Limítate a evaluar la entrada. No investigues la afirmación ni evalúes su veracidad.'
        'El sistema, posteriormente, modelará todo un proceso de investigación periodística para dar al usuario un informe sobre'
        'la veracidad, trazabilidad y documentación de su solicitud.'),
        ('user', user_input)
    ]

    response = model.invoke(messages)
    return response

validacion = model_call("La tierra es plana")
print(validacion['parsed'].input_validation)
print("Analisis de la peticion\n")
print(f"Consumo de tokens:\n Tokens de entrada: {validacion['raw'].usage_metadata['input_tokens']}\n Tokens de salida: {validacion['raw'].usage_metadata['output_tokens']}\n"
      f"Total tokens consumidos: {validacion['raw'].usage_metadata['total_tokens']}")