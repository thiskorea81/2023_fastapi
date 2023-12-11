from fastapi import FastAPI, Request, Form
from openai import Client
from openai import OpenAI
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

client = OpenAI() 

@app.post("/run_code")
async def run_code(request: Request, code: str = Form(...)):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": code}
        ]
    )
    result = completion.choices[0].message.content
    return templates.TemplateResponse("result.html", {"request": request, "result": result})

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
