import json
import pandas as pd
import requests
from bs4 import BeautifulSoup

# The two websites im referring to are given below
world_url = "https://www.worldometers.info/coronavirus/"
india_state_url = "https://api.covid19india.org/data.json"
r = requests.get(world_url)
r1 = requests.get(india_state_url)


class TemplateReader:
    def __init__(self):
        pass

    def read_course_template(self, topic_selected):
        try:
            if topic_selected == 'India' or topic_selected == '1':
                data = json.loads(r1.content)
                df = (pd.DataFrame(data['statewise'])[['state', 'active', 'confirmed', 'deaths',
                                                       'recovered', 'lastupdatedtime']].set_index('state'))
                self.list_of_columns = ['active', 'confirmed', 'deaths', 'recovered',
                                        'lastupdatedtime', 'recovery_rate (in percentage)']
                df['recovery_rate (in percentage)'] = df['recovered'].apply(int) / (
                            df['deaths'].apply(int) + df['recovered'].apply(int))
                df['recovery_rate (in percentage)'] = (df['recovery_rate (in percentage)']*100).round(2)

            elif topic_selected == 'Worldwide' or topic_selected == '2':
                # World DataFrame
                soup = BeautifulSoup(r.content, 'lxml')
                table = soup.find(name="table")
                df = pd.read_html(str(table))[0]
                self.list_of_columns = ['Country,Other', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
                                        'TotalRecovered', 'ActiveCases', 'Serious,Critical', 'Recovery_Rate (in percentage)']
                df['Recovery_Rate (in percentage)'] = (
                            (df['TotalRecovered'] / (df['TotalDeaths'] + df['TotalRecovered'])) * 100).round(2)

            return df[self.list_of_columns].fillna(0)

        except Exception as e:
            print('The exception is '+str(e))
