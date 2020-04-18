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
            if topic_selected == 'India':
                data = json.loads(r1.content)
                df = (pd.DataFrame(data['statewise'])[['state', 'active', 'confirmed', 'deaths', 'recovered', 'lastupdatedtime']]
                      .set_index('state'))
                df['recovery_rate'] = df['recovered'].apply(int) / (
                            df['deaths'].apply(int) + df['recovered'].apply(int))

            elif topic_selected == 'Worldwide':
                # World DataFrame
                soup = BeautifulSoup(r.content, 'lxml')
                table = soup.find(name="table")
                df = pd.read_html(str(table))[0]

            return df

        except Exception as e:
            print('The exception is '+str(e))
