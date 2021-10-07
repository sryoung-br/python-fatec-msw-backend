from os import defpath
import pandas as pd

class CovidBusiness():

  def __init__(self, dataset_file):
    df = pd.read_csv(dataset_file)
    df = df.rename(columns = {'Country/Region':'Country', 
                          'New cases': 'NewCases', 
                          'New deaths': 'NewDeaths', 
                          'New recovered': 'NewRecovered', 
                          'WHO Region':'Region'})
    self.dataset = df

  '''
  Method - Filter by Confirmed Cases
  '''
  def get_countries(self):
    countries = self.dataset['Country']
    countries = countries.drop_duplicates()
    collection = {'countries' : [key for key in countries]}
    return collection

  def filter_by_confirmed(self, country=None, start=None, end=None):

    if country == None or country == "":
      filter = self.dataset.query(f'Date >= "{start}" & Date  <=  "{end}" ')
    else:
      filter = self.dataset.query(f'Country == "{country}" & \
                                   Date >= "{start}" & Date  <=  "{end}"')
      

    #agregation
    group_by = dict(filter.groupby(['Country']).sum()["Confirmed"])
    
    #transform
    collection = [{"country" : key, "value" : int(group_by[key]) } for key in group_by.keys()]
    collection = sorted(collection, key = lambda i: i['value'],reverse=True)

    return collection


  '''
  Method - Filter by Death Cases
  '''
  def filter_by_death(self, country=None, start=None, end=None):

    if country == None or country == "":
      filter = self.dataset.query(f'Date >= "{start}" & Date  <=  "{end}" ')
    else:
      filter = self.dataset.query(f'Country == "{country}" & \
                                   Date >= "{start}" & Date  <=  "{end}"')
      

    #agregation
    group_by = dict(filter.groupby(['Country']).sum()["Deaths"])
    
    #transform
    collection = [{"country" : key, "value" : int(group_by[key]) } for key in group_by.keys()]
    collection = sorted(collection, key = lambda i: i['value'],reverse=True)

    return collection

  '''
  Method - Filter by Recovered Cases
  '''
  def filter_by_recovered(self, country=None, start=None, end=None):

    if country == None or country == "":
      filter = self.dataset.query(f'Date >= "{start}" & Date  <=  "{end}" ')
    else:
      filter = self.dataset.query(f'Country == "{country}" & \
                                   Date >= "{start}" & Date  <=  "{end}"')
      

    #agregation
    group_by = dict(filter.groupby(['Country']).sum()["Recovered"])
    
    #transform
    collection = [{"country" : key, "value" : int(group_by[key]) } for key in group_by.keys()]
    collection = sorted(collection, key = lambda i: i['value'],reverse=True)

    return collection


  '''
  Method - Filter by Active Cases
  '''
  def filter_by_active(self, country=None, start=None, end=None):

    if country == None or country == "":
      filter = self.dataset.query(f'Date >= "{start}" & Date  <=  "{end}" ')
    else:
      filter = self.dataset.query(f'Country == "{country}" & \
                                   Date >= "{start}" & Date  <=  "{end}"')
      

    #agregation
    group_by = dict(filter.groupby(['Country']).sum()["Active"])

    #transform
    collection = [{"country" : key, "value" : int(group_by[key]) } for key in group_by.keys()]
    collection = sorted(collection, key = lambda i: i['value'],reverse=True)

    return collection

  '''
  Method - Moving Average
  '''
  def moving_average(self, country=None, start=None, end=None, window=int):

    if country == None or country == "":
      return { "error" : "Parâmetro country necessário."}
    else:
      filter = self.dataset.query(f'Country == "{country}" & \
                                   Date >= "{start}" & Date  <=  "{end}"')

    filter = filter.set_index('Date')

    confirmed = filter["Confirmed"].rolling(window = window).mean().fillna(0)
    deaths = filter["Deaths"].rolling(window = window).mean().fillna(0)
    active = filter["Active"].rolling(window = window).mean().fillna(0)
    recovered = filter["Recovered"].rolling(window = window).mean().fillna(0)

    return { 
      "confirmed" : [ {"index" : key, "ma" : confirmed[key] } for key in confirmed.keys() ], 
      "deaths" : [ {"index" : key, "ma" : deaths[key] } for key in deaths.keys() ],
      "active" : [ {"index" : key, "ma" : active[key] } for key in active.keys() ],
      "recovered" : [ {"index" : key, "ma" : recovered[key] } for key in recovered.keys() ], }     
