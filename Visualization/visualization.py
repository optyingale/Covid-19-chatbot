import geopandas as gpd
import matplotlib.pyplot as plt

img_loc = './Images/'


class GenerateGraph:
    def india_or_worldwide(self, df):
        # Pre determining font size
        plt.rcParams.update({'font.size': 23})
        try:
            if df.index.name == 'state':

                # Converting each important column to integer for continuous values
                df['active'] = df['active'].apply(int)
                df['confirmed'] = df['confirmed'].apply(int)
                df['deaths'] = df['deaths'].apply(int)
                df['recovered'] = df['recovered'].apply(int)

                # Read geometry file
                india = gpd.read_file('./Visualization/Indian_States.shp')

                # Replacing Values before joining with df
                india['st_nm'].replace('NCT of Delhi', 'Delhi', inplace=True)
                india['st_nm'].replace('Jammu & Kashmir', 'Jammu and Kashmir', inplace=True)
                india['st_nm'].replace('Andaman & Nicobar Island', 'Andaman and Nicobar Islands', inplace=True)
                india['st_nm'].replace('Arunanchal Pradesh', 'Arunachal Pradesh', inplace=True)
                india['st_nm'].replace('Dadara & Nagar Havelli', 'Dadra and Nagar Haveli', inplace=True)
                india['st_nm'].replace('Daman & Diu', 'Daman and Diu', inplace=True)

                # Joining df and india
                # Dropped Total as it skews the range of plot towards the higher side
                india_joined = india.join(df.drop(['Ladakh', 'Total']), how='right', on='st_nm')

                # Plotting Deaths, Active, Confirmed, Recovered
                india_joined.plot(edgecolor='0.8', linewidth=0.7, column='deaths', cmap='YlOrRd', legend=True,
                                  figsize=(15, 15), vmin=india_joined['deaths'].min(),
                                  vmax=india_joined['deaths'].max())
                plt.title('Covid-19 Statewise Data — Deaths', fontdict={'fontsize': '30', 'fontweight': '15'})
                plt.savefig(img_loc + 'Deceased.png')
                india_joined.plot(edgecolor='0.8', linewidth=0.7, column='active', cmap='Greys', legend=True,
                                  figsize=(15, 15), vmin=india_joined['active'].min(),
                                  vmax=india_joined['active'].max())
                plt.title('Covid-19 Statewise Data — Active Cases', fontdict={'fontsize': '30', 'fontweight': '15'})
                plt.savefig(img_loc + 'Active.png')
                india_joined.plot(edgecolor='0.8', linewidth=0.7, column='confirmed', cmap='Blues', legend=True,
                                  figsize=(15, 15), vmin=india_joined['confirmed'].min(),
                                  vmax=india_joined['confirmed'].max())
                plt.title('Covid-19 Statewise Data — Confirmed Cases', fontdict={'fontsize': '30', 'fontweight': '15'})
                plt.savefig(img_loc + 'Confirmed.png')
                india_joined.plot(edgecolor='0.8', linewidth=0.7, column='recovered', cmap='YlGn', legend=True,
                                  figsize=(15, 15), vmin=india_joined['recovered'].min(),
                                  vmax=india_joined['recovered'].max())
                plt.title('Covid-19 Statewise Data — Recovered Cases', fontdict={'fontsize': '30', 'fontweight': '15'})
                plt.savefig(img_loc + 'Recovered.png')

                # Generating pie chart
                active = df.loc['Total', :]['active']
                deaths = df.loc['Total', :]['deaths']
                recovered = df.loc['Total', :]['recovered']

                labels = ['Recovered\n' + str(recovered), 'Deceased\n' + str(deaths), 'Active\n' + str(active)]

                plt.figure(figsize=(15, 15))
                plt.pie([recovered, deaths, active], labels=labels, )
                central_circle = plt.Circle((0, 0), 0.5, color='white')
                fig = plt.gcf()
                # plt.rc('font', size=17)
                fig.gca().add_artist(central_circle)
                plt.title('Total Confirmed, Recovered and Deceased Cases', fontsize=35)
                plt.savefig(img_loc + 'Pie_chart.png')

                self.status = 'done'

            elif df.index.name == 'Country,Other':

                # Replacing names of all Countries to match with existing df
                world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
                world.name.replace('United States of America', 'USA', inplace=True)
                world.name.replace('South Korea', 'S. Korea', inplace=True)
                world.name.replace('United Kingdom', 'UK', inplace=True)
                world.name.replace('United Arab Emirates', 'UAE', inplace=True)
                world.name.replace('Dominican Rep.', 'Dominican Republic', inplace=True)
                world.name.replace('Bosnia and Herz.', 'Bosnia', inplace=True)
                world.name.replace('Macedonia', 'North Macedonia', inplace=True)
                world.name.replace('Dem. Rep. Congo', 'DRC', inplace=True)
                world.name.replace('Eq. Guinea', 'Equatorial Guinea', inplace=True)
                world.name.replace('Central African Rep.', 'CAR', inplace=True)
                world.name.replace('Falkland Is.', 'Falkland Islands', inplace=True)
                world.name.replace('W. Sahara', 'Western Sahara', inplace=True)

                # Drop World and Total as they skew the range of plot towards higher side
                joined = world.join(df.drop(['World', 'Total:']), how='right', on='name')

                # Plotting Deaths, Active, Confirmed, Recovered
                joined.plot(edgecolor='0.8', linewidth=0.7, column='TotalDeaths', legend=True, cmap='YlOrRd',
                            figsize=(25, 25), vmin=joined['TotalDeaths'].min(), vmax=joined['TotalDeaths'].max())
                plt.title('Covid-19 World — TotalDeaths', fontdict={'fontsize': '40', 'fontweight': '20'})
                plt.savefig(img_loc + 'Deceased.png')
                joined.plot(edgecolor='0.8', linewidth=0.7, column='ActiveCases', legend=True, cmap='Greys',
                            figsize=(25, 25), vmin=joined['ActiveCases'].min(), vmax=joined['ActiveCases'].max())
                plt.title('Covid-19 World — ActiveCases', fontdict={'fontsize': '40', 'fontweight': '20'})
                plt.savefig(img_loc + 'Active.png')
                joined.plot(edgecolor='0.8', linewidth=0.7, column='TotalCases', legend=True, cmap='Blues',
                            figsize=(25, 25), vmin=joined['TotalCases'].min(), vmax=joined['TotalCases'].max())
                plt.title('Covid-19 World — TotalCases', fontdict={'fontsize': '40', 'fontweight': '20'})
                plt.savefig(img_loc + 'Confirmed.png')
                joined.plot(edgecolor='0.8', linewidth=0.7, column='TotalRecovered', legend=True, cmap='YlGn',
                            figsize=(25, 25), vmin=joined['TotalRecovered'].min(), vmax=joined['TotalRecovered'].max())
                plt.title('Covid-19 World — TotalRecovered', fontdict={'fontsize': '40', 'fontweight': '20'})
                plt.savefig(img_loc + 'Recovered.png')

                # Pie Chart
                recovered = df.loc['World', :]['TotalRecovered'].astype(int)
                deaths = df.loc['World', :]['TotalDeaths'].astype(int)
                active = df.loc['World', :]['ActiveCases'].astype(int)

                labels = ['Recovered\n' + str(recovered), 'Deceased\n' + str(deaths), 'Active\n' + str(active)]

                plt.figure(figsize=(15, 15))
                plt.pie([recovered, deaths, active], labels=labels, )
                central_circle = plt.Circle((0, 0), 0.5, color='white')
                fig = plt.gcf()
                # plt.rc('font', size=30)
                fig.gca().add_artist(central_circle)
                plt.title('Total Confirmed, Recovered and Deceased Cases', fontsize=30)
                plt.savefig(img_loc + 'Pie_chart.png')

                self.status = 'done'

        except Exception as e:
            print('this is in visualization ', e)
            self.status = str(e)
        return self.status
