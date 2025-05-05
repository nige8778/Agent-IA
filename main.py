import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

# Charger les variables d'environnement
load_dotenv()

# Initialiser l'API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Créer l'application FastAPI
app = FastAPI(title="Mon Agent IA Simple")

# Modèle de données pour la requête
class MessageRequest(BaseModel):
    message: str

# Modèle de données pour la réponse
class MessageResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon Agent IA! Envoyez un message à /chat pour discuter."}

@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    try:
        # Appel à l'API OpenAI
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un assistant IA utile et amical."},
                {"role": "user", "content": request.message}
            ]
        )
        
        # Récupérer la réponse
        response_text = completion.choices[0].message.content
        
        return MessageResponse(response=response_text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'appel à l'API: {str(e)}")

# Pour lancer l'application localement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
