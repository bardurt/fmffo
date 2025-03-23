import pandas as pd
import matplotlib.pyplot as plt


default_year = '2025'
default_type = 'Hysa 1 MSC'
selected_type = input(f"Enter the type to plot (default: '{default_type}'): ").strip() or default_type
selected_year = input(f"Enter the year to plot (default: '{default_year}'): ").strip() or default_year
print(f"Plotting data for: {selected_type}, year {selected_year}")

csv_file = csv_file = 'fmf' + selected_year + '.csv'
try:
    data = pd.read_csv(csv_file, on_bad_lines='warn')
except pd.errors.ParserError as e:
    print(f"ParserError: {e}")
    data = pd.read_csv(csv_file, on_bad_lines='skip')
    print("Loaded data by skipping problematic rows.")

data['type'] = data['type'].str.strip()  
selected_data = data[data['type'].str.lower() == selected_type.lower()].copy()

if selected_data.empty:
    print(f"\nNo data found for '{selected_type}'. Available 'type' values:")
    print(data['type'].unique())
else:
    selected_data['date'] = pd.to_datetime(selected_data['date'], format='%Y%m%d')

    selected_data = selected_data.sort_values('date')

    dates = selected_data['date']
    avg_prices = selected_data['avg price']
    max_prices = selected_data['max price']
    min_prices = selected_data['min price']

    plt.figure(figsize=(12, 7))  

    plt.plot(dates, max_prices, marker='^', linestyle='-', color='r', label='Max Price')
    plt.plot(dates, avg_prices, marker='o', linestyle='-', color='b', label='Avg Price')
    plt.plot(dates, min_prices, marker='v', linestyle='-', color='g', label='Min Price')

    plt.title(f'Price Trends of {selected_type} Over Time', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (kr)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()  

    plt.tight_layout()
    plt.show()