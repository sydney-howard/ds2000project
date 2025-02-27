import csv
import matplotlib.pyplot as plt

# Reads the CSV file into a list.
def read_csv_data(filename):
    data = list()
    with open(filename, "r") as file:
        csv_file = csv.reader(file)
        for line in csv_file:
            data.append(line)
    return data

# Creates a dictionary with the keys as the country and the values as a list of 2 lists. The first list is the emissions data, the second is the corresponding years.
def create_dict(data):
    data_dict = {}
    cleaned_data = data[2:]
    for country_data in cleaned_data:
        emissions_data = country_data[2:]
        years = list(range(1990, 2022))
        data_years = []
        country = country_data[0]
        float_data = []
        for i in range(len(emissions_data)):
            if emissions_data[i] == '':
                continue
            elif emissions_data[i] == "..":
                continue
            elif "B" in emissions_data[i]:
                continue
            else:
                data_years.append(years[i])
                emissions_data[i] = emissions_data[i].replace(",", "")  
                float_data.append(float(emissions_data[i]))                
        data_dict[country] = [float_data, data_years]
    return data_dict

# Finds the average amount of emissions per year.
def create_means(data_dict):
    mean_dict = {}
    for country, numbers in data_dict.items():
        mean_dict[country] = round(sum(numbers[0]) / len(numbers[0]), 2)
    return mean_dict

# Finds the country with the highest and lowest averages of emissions per year (using the means dictionary). Also outputs the OECD dictionary.
def find_extrema(mean_dict):
    country_dict = {}
    OECD_dict = {}
    for country, value in mean_dict.items():
        if "OECD" in country:
            OECD_dict[country] = value
        else: 
            country_dict[country] = value
    country_least = min(country_dict, key = country_dict.get)
    country_most = max(country_dict, key = country_dict.get)
    OECD_dict.pop("OECD")
    return country_least, country_most, OECD_dict


# Plots Iceland's Emissions 
def plot_CO2_emissions(data_dict):
    plt.figure(figsize=(10, 6))
    country = 'Iceland'  
    if country in data_dict:    
           x_values = data_dict[country][1] # Years
           y_values = data_dict[country][0] # Emissions
           color = 'skyblue'
           plt.scatter(x_values, y_values, label=country, color=color)
           plt.title("CO2 Emissions Over Time: Iceland")
           plt.xlabel("Year")
           plt.ylabel("CO2 Emissions in Tonnes Equivalent")
           plt.legend()
           plt.grid(True)
           plt.savefig("Iceland_CO2_emissions.png", bbox_inches="tight")
           plt.show()
    else:
        print("Data for Iceland not available")

# Plots Iceland and the US Emissions
def plot_CO2_comparison(data_dict):
    for country, values in data_dict.items():
        if country == 'United States':
            color = 'salmon' 
        elif country == 'Iceland':
            color = 'skyblue'   
        else:
            color = 'gray'          
        x_values = data_dict[country][1] # Years
        y_values = data_dict[country][0] # Emissions
        plt.scatter(x_values, y_values, label= country, color=color)
    plt.title("CO2 Emissions Over Time: U.S. Vs. Iceland")
    plt.xlabel("Year")
    plt.ylabel("CO2 Emissions in Tonnes Equivalent")
    plt.legend()
    plt.grid(True)
    plt.savefig("CO2_emissions.png", bbox_inches="tight")
    plt.show()
    
   
# Plots the mean tonnes of CO2 per year for the 3 OECD regions.
def plot_CO2_OECD(OECD_dict):
    x_values = OECD_dict.keys()
    heights = OECD_dict.values()
    plt.figure(figsize=(15, 7))
    colors = ['skyblue', 'salmon', 'lightgreen']
    plt.bar(x_values, heights, color=colors)
    # Labels
    plt.title("Annual Average of CO2 Emissions in OECD Regions")
    plt.xlabel("OECD Region")
    plt.ylabel("CO2 Emissions in Tonnes Equivalent")
    plt.savefig("OECDvsNonOECD.png", bbox_inches="tight")
    plt.show()


# Plots the average annual kilograms of co2 per 1000 us dollars per country
def plot_dollar_means(dollars_means):
    x_values = dollars_means.keys()
    heights = dollars_means.values()  
    colors = ['skyblue', 'salmon', 'lightgreen', 'gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'lightpink', 'lightcoral', 'lightblue']
    plt.bar(x_values, heights, color=colors)
    # Labels
    plt.title("Annual Average Kilo's of CO2 per 1,000 dollars Per Country")
    plt.xlabel("Country")
    plt.ylabel("Annual Mean Kilograms of CO2")
    plt.xticks(fontsize = 5, rotation = 90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("kilo_per_thousand_dollars.jpg", bbox_inches="tight")
    plt.show()

    
def main():
    # Using "tonnes.csv"
    tonnes_data = (read_csv_data("tonnes.csv"))
    tonnes_dict = create_dict(tonnes_data)
    tonnes_means = create_means(tonnes_dict)
    
    
    # Using "kilo_per_thousand_dollars.csv"
    dollars_data = (read_csv_data("kilo_per_thousand_dollars.csv"))
    dollars_dict = create_dict(dollars_data)
    dollars_means = create_means(dollars_dict)
    print(dollars_means)
  
    # Extrema and OECD Dictionary Init
    least_emission_average, most_emmision_average, OECD_dict = find_extrema(tonnes_means)
    print(OECD_dict)
    print("The country with the least emmisions:", least_emission_average)
    print("The country with the most emmisions:", most_emmision_average)
    
    # Plotting CO2 Emissions 
    plot_countries = ["United States", "Iceland"]
    selected_countries_emissions= {}
    for country in plot_countries:
        if country in tonnes_dict:
            selected_countries_emissions[country] = tonnes_dict[country]
            
    plot_CO2_emissions(selected_countries_emissions)
    
    # Comparing CO2 Emissions
    plot_CO2_comparison(selected_countries_emissions)
    
    # Plotting Kilo Per Thousand Dollars
    plot_dollar_means(dollars_means)
    
    # Plotting OECD Means
    plot_CO2_OECD(OECD_dict)
    
    
main()