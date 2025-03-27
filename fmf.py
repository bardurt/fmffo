import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

default_year = '2025'
default_type = 'Hysa 1 MSC'
selected_type = default_type
selected_years = default_year
volume_profile_active = True

def fetch_data():
 selected_type = input(f"Enter the type to plot (default: '{default_type}'): ").strip() or default_type
 selected_years = input(f"Enter the years to plot (comma-separated, default: '{default_year}'): ").strip() or default_year
 selected_years = [year.strip() for year in selected_years.split(',')]
 volume_profile_input = input("Show Volume Profile Y / N (Default: Y): ").strip() or "Y"
 volume_profile_active = volume_profile_input.lower() == "y"

 print(f"Fetching data for: {selected_type}, years {', '.join(selected_years)}")

 data_frames = []
 for year in selected_years:
    csv_file = f'data/fmf{year}.csv'
    try:
        df = pd.read_csv(csv_file, on_bad_lines='warn')
        df['year'] = year 
        data_frames.append(df)
    except pd.errors.ParserError as e:
        print(f"ParserError for {year}: {e}")
        continue
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")
        continue

 if not data_frames:
    raise Exception("No valid data files loaded.")

 data = pd.concat(data_frames, ignore_index=True)

 return data


if '--listall' in sys.argv:
    listall_index = sys.argv.index('--listall')
    if len(sys.argv) > listall_index + 1:
        suffix = sys.argv[listall_index + 1]
        csv_file = f'data/fmf{suffix}.csv'
    else:
        csv_file = f'data/fmf{default_year}.csv'
    
    try:
        data = pd.read_csv(csv_file, on_bad_lines='warn')
        unique_types = sorted(data['type'].dropna().unique(), key=str.lower)
        print(f"Available types from {csv_file}:")
        for t in unique_types:
            print(t)
    except Exception as e:
        print(f"Error loading file {csv_file}: {e}")
    sys.exit(0)

raw = fetch_data()
raw['type'] = raw['type'].str.strip()
selected_data = raw[raw['type'].str.lower() == selected_type.lower()].copy()

if selected_data.empty:
    print(f"\nNo data found for '{selected_type}'. Available 'type' values:")
    print(sorted(data['type'].dropna().unique(), key=str.lower))
else:
    selected_data['date'] = pd.to_datetime(selected_data['date'], format='%Y%m%d')
    selected_data = selected_data.sort_values('date')
    
    selected_data['index'] = range(len(selected_data))
    indices = selected_data['index']
    avg_prices = selected_data['avg price']
    max_prices = selected_data['max price']
    min_prices = selected_data['min price']
    kg_values = selected_data['kg']
    date_labels = selected_data['date'].dt.strftime('%Y-%m-%d')
    
    y_min = min(min_prices.min(), avg_prices.min())
    y_max = max(max_prices.max(), avg_prices.max())
    
    if volume_profile_active:
        fig, (ax_vp, ax1) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [1, 5]})
        price_bins = np.linspace(y_min, y_max, num=20)
        volume_profile = np.histogram(avg_prices, bins=price_bins, weights=kg_values)[0]
        ax_vp.barh(price_bins[:-1], volume_profile, height=np.diff(price_bins), color='#00b2eb', alpha=0.7)
        ax_vp.invert_yaxis()
        ax_vp.set_ylim(y_min, y_max)
        ax_vp.set_xticks([])  
        ax_vp.set_title("Volume Profile", fontsize=12)
        ax_vp.set_ylabel('Price (kr)', fontsize=12)
    else:
        fig, ax1 = plt.subplots(figsize=(12, 7))
    
    ax1.vlines(indices, min_prices, max_prices, color='#dfa69e', linewidth=1.5, label='Min-Max Range')
    ax1.plot(indices, avg_prices, color='black', linewidth=2, marker='o', markersize=4, label='Avg Price')
    ax1.set_ylim(y_min, y_max) 
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Price (kr)', fontsize=12, color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    ax2 = ax1.twinx()
    ax2.bar(indices, kg_values, alpha=0.3, color='#00b2eb', label='Kg', width=0.8)
    ax2.set_ylabel('Kilograms (kg)', fontsize=12, color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    
    step = max(1, len(indices) // 10)
    ax1.set_xticks(indices[::step])
    ax1.set_xticklabels(date_labels[::step], rotation=45)
    
    plt.title(f'Price Trends for {selected_type}', fontsize=14)
    plt.tight_layout()
    plt.show()



