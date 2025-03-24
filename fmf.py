import sys
import pandas as pd
import matplotlib.pyplot as plt

default_year = '2025'
default_type = 'Hysa 1 MSC'

if '--listall' in sys.argv:
    csv_file = f'data/fmf{default_year}.csv'
    try:
        data = pd.read_csv(csv_file, on_bad_lines='warn')
        unique_types = sorted(data['type'].dropna().unique(), key=str.lower)
        print("Available types:")
        for t in unique_types:
            print(t)
    except Exception as e:
        print(f"Error loading file: {e}")
    sys.exit(0)

selected_type = input(f"Enter the type to plot (default: '{default_type}'): ").strip() or default_type
selected_years = input(f"Enter the years to plot (comma-separated, default: '{default_year}'): ").strip() or default_year
selected_years = [year.strip() for year in selected_years.split(',')]

print(f"Plotting data for: {selected_type}, years {', '.join(selected_years)}")

data_frames = []
for year in selected_years:
    csv_file = f'data/fmf{year}.csv'
    try:
        df = pd.read_csv(csv_file, on_bad_lines='warn')
        df['year'] = year  # Track year in data
        data_frames.append(df)
    except pd.errors.ParserError as e:
        print(f"ParserError for {year}: {e}")
        continue
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")
        continue

if not data_frames:
    print("No valid data files loaded.")
    sys.exit(1)

data = pd.concat(data_frames, ignore_index=True)
data['type'] = data['type'].str.strip()
selected_data = data[data['type'].str.lower() == selected_type.lower()].copy()

if selected_data.empty:
    print(f"\nNo data found for '{selected_type}'. Available 'type' values:")
    print(sorted(data['type'].dropna().unique(), key=str.lower))
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