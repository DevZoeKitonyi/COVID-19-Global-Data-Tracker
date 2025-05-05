import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

class CovidDataTracker:
    def __init__(self):
        self.base_url = "https://disease.sh/v3/covid-19"
        self.data = None
        
    def fetch_global_data(self):
        """Fetch global COVID-19 data"""
        try:
            response = requests.get(f"{self.base_url}/all")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching global data: {e}")
            return None

    def fetch_country_data(self):
        """Fetch COVID-19 data for all countries"""
        try:
            response = requests.get(f"{self.base_url}/countries")
            response.raise_for_status()
            self.data = pd.DataFrame(response.json())
            return self.data
        except requests.RequestException as e:
            print(f"Error fetching country data: {e}")
            return None

    def fetch_historical_data(self, days=30):
        """Fetch historical COVID-19 data"""
        try:
            response = requests.get(f"{self.base_url}/historical/all?lastdays={days}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching historical data: {e}")
            return None

    def create_cases_map(self):
        """Create a choropleth map of COVID-19 cases"""
        if self.data is None:
            self.fetch_country_data()
            
        fig = px.choropleth(
            self.data,
            locations="countryInfo.iso3",
            color=np.log10(self.data["cases"]),
            hover_name="country",
            hover_data=["cases", "deaths", "recovered"],
            color_continuous_scale="Viridis",
            title="Global COVID-19 Cases (Log Scale)"
        )
        fig.show()

    def create_trend_analysis(self, days=30):
        """Create trend analysis plots"""
        historical_data = self.fetch_historical_data(days)
        if historical_data:
            df = pd.DataFrame(historical_data)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df['cases'], name='Cases'))
            fig.add_trace(go.Scatter(x=df.index, y=df['deaths'], name='Deaths'))
            fig.add_trace(go.Scatter(x=df.index, y=df['recovered'], name='Recovered'))
            
            fig.update_layout(
                title=f"COVID-19 Trends (Last {days} Days)",
                xaxis_title="Date",
                yaxis_title="Count",
                hovermode='x unified'
            )
            fig.show()

    def get_top_countries(self, metric='cases', n=10):
        """Get top N countries by specified metric"""
        if self.data is None:
            self.fetch_country_data()
            
        return self.data.nlargest(n, metric)[['country', metric]]

    def generate_summary_report(self):
        """Generate a summary report of global COVID-19 statistics"""
        global_data = self.fetch_global_data()
        if global_data:
            print("\nGLOBAL COVID-19 SUMMARY")
            print("=" * 30)
            print(f"Total Cases: {global_data['cases']:,}")
            print(f"Total Deaths: {global_data['deaths']:,}")
            print(f"Total Recovered: {global_data['recovered']:,}")
            print(f"Active Cases: {global_data['active']:,}")
            print(f"Critical Cases: {global_data['critical']:,}")
            print(f"Cases Per Million: {global_data['casesPerOneMillion']:,}")
            print(f"Deaths Per Million: {global_data['deathsPerOneMillion']:,}")
            print(f"Tests: {global_data['tests']:,}")
            print(f"Tests Per Million: {global_data['testsPerOneMillion']:,}")
            print(f"Population: {global_data['population']:,}")
            print(f"Affected Countries: {global_data['affectedCountries']:,}")

def main():
    # Initialize the tracker
    tracker = CovidDataTracker()
    
    # Generate summary report
    tracker.generate_summary_report()
    
    # Create visualizations
    tracker.create_cases_map()
    tracker.create_trend_analysis()
    
    # Display top countries
    print("\nTop 10 Countries by Total Cases:")
    print(tracker.get_top_countries())

if __name__ == "__main__":
    main()
