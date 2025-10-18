import matplotlib.pyplot as plt

class Visualizer:
    @staticmethod
    def plot_population_trend(data, country):
        plt.figure(figsize=(10, 6))

        # Extract years and population columns
        year_columns = [col for col in data.columns if 'population' in col]
        years = [int(col.split()[0]) for col in year_columns]  # Extract year from 'YYYY population'
        population = [data[col].values[0] for col in year_columns]  # Assuming only one row per country

        plt.plot(years, population, marker='o', label=f"{country} Population Trend")
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.title(f"{country} Population Trend")
        plt.xticks(years, rotation=45)  # Rotate x-axis labels
        plt.tight_layout()  # Adjust layout to prevent label overlap
        plt.legend()
        plt.show()

    @staticmethod
    def plot_growth_rate(data, country):
        plt.figure(figsize=(10, 6))

        # Extract years and growth rate columns
        year_columns = [col for col in data.columns if 'population' in col]
        years = [int(col.split()[0]) for col in year_columns]  # Extract year from 'YYYY population'
        growth_rates = []

        # Calculate growth rates for each year (except the first one)
        for i in range(1, len(year_columns)):
            prev_year = year_columns[i-1]
            curr_year = year_columns[i]
            growth_rate = ((data[curr_year].values[0] - data[prev_year].values[0]) / data[prev_year].values[0]) * 100
            growth_rates.append(growth_rate)

        plt.bar(years[1:], growth_rates, color='orange', label=f"{country} Growth Rate")
        plt.xlabel("Year")
        plt.ylabel("Growth Rate (%)")
        plt.title(f"{country} Yearly Growth Rate")
        plt.xticks(years[1:], rotation=45)  # Rotate x-axis labels
        plt.tight_layout()  # Adjust layout to prevent label overlap
        plt.legend()
        plt.show()
