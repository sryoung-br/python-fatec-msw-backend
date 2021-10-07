import uvicorn
from fastapi import FastAPI
from covid_business import CovidBusiness

#Autorizar clientes enviarem requisições para API
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, 
                allow_origins=['*'],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
dataset_file = 'full_grouped.csv'

covid = CovidBusiness(dataset_file)


@app.get("/")
async def read_root():
    return {"server": "Servidor iniciado com Sucesso"}

'''
Resource - Covid Status
'''
@app.get("/api/v1/fatec/covid/countries")
async def covid_countries():
  return covid.get_countries()

@app.get("/api/v1/fatec/covid/status")
async def covid_status(country: str = "", start: str = "", end: str = ""):
  
  #Confirmados
  confirmed = covid.filter_by_confirmed(country=country, start=start, end=end)

  #Mortes
  deaths = covid.filter_by_death(country=country, start=start, end=end)

  #Ativos
  active = covid.filter_by_active(country=country, start=start, end=end)

  #Recuperados
  recovered = covid.filter_by_recovered(country=country, start=start, end=end)

  obj = {"confirmed" : confirmed, 
          "deaths" : deaths, 
          "active": active, 
          "recovered": recovered}

  return obj

@app.get("/api/v1/fatec/moving/average")
async def covid_moving_average(country: str = "", start: str = "", end: str = "", window: int = 7): #default = 7
    
    #Média móvel
    moving_average = covid.moving_average(country=country, start=start, end=end, window=window)

    return moving_average

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0")