import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

LABEL_PRICE = 'Price (DKK)'
LABEL_WEIGHT = 'KG'
LABEL_DATE = 'Date'
LABEL_HISTOGRAM = 'Histogram'

HEADER_INDEX = 'index'
HEADER_TYPE = 'type'
HEADER_KG = 'kg'
HEADER_DATE = 'date'
HEADER_MIN_PRICE = 'min price'
HEADER_AVG_PRICE = 'avg price'
HEADER_MAX_PRICE = 'max price'

default_year = '2025'
default_type = 'Hysa 1 MSC'
selected_type = default_type
selected_years = default_year
print_max_min_price = False

def display_help():
        print("""
    Usage: script.py [options]

    Options:
        --listtype [years]     List all unique types (comma-separated years optional)
        --listdate [years]     List all unique dates (comma-separated years optional)
        --price                Execute price analysis
        --weight               Execute weight analysis
        --dryrun [years]       Validate data formatting (comma-separated years optional)
        -h, --help             Show this help message

    Examples:
        script.py --listtype 2022,2023
        script.py --price
        script.py --dryrun 2023
    """)


def fetch_data(selected_years):
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

def plot_price_trend(data_frame, type, plot_histogram, print_price_range, print_volume):
    data_frame[HEADER_DATE] = pd.to_datetime(data_frame[HEADER_DATE], format='%Y%m%d')
    data_frame = data_frame.sort_values(HEADER_DATE)
    
    data_frame[HEADER_INDEX] = range(len(data_frame))
    indices = data_frame[HEADER_INDEX]
    print(data_frame)
    avg_prices = data_frame[HEADER_AVG_PRICE]
    max_prices = data_frame[HEADER_MAX_PRICE]
    min_prices = data_frame[HEADER_MIN_PRICE]
    kg_values = data_frame[HEADER_KG]
    date_labels = data_frame[HEADER_DATE].dt.strftime('%Y-%m-%d')
    
    y_min = min(min_prices.min(), avg_prices.min()) -1
    y_max = max(max_prices.max(), avg_prices.max()) +1
    
    if plot_histogram:
        fig, (ax_vp, ax1) = plt.subplots(1, 2, figsize=(14, 7), gridspec_kw={'width_ratios': [1, 5]})
        price_bins = np.linspace(y_min, y_max, num=20)
        volume_profile = np.histogram(avg_prices, bins=price_bins, weights=kg_values)[0]
        ax_vp.barh(price_bins[:-1], volume_profile, height=np.diff(price_bins), color='#00b2eb', alpha=0.7)
        ax_vp.invert_yaxis()
        ax_vp.set_ylim(y_min, y_max)
        ax_vp.set_xticks([])  
        ax_vp.set_title(LABEL_HISTOGRAM, fontsize=12)
        ax_vp.set_ylabel(LABEL_PRICE, fontsize=12)
    else:
        fig, ax1 = plt.subplots(figsize=(12, 7))
    
    if(print_price_range):
        ax1.vlines(indices, min_prices, max_prices, color='#dfa69e', linewidth=1.5, label='Min-Max Range')
    
    ax1.plot(indices, avg_prices, color='black', linewidth=2, markersize=4, label='Avg Price')
    ax1.set_ylim(y_min, y_max) 
    ax1.set_xlabel(LABEL_DATE, fontsize=12)
    ax1.set_ylabel(LABEL_PRICE, fontsize=12, color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    if(print_volume):
        ax2 = ax1.twinx()
        ax2.bar(indices, kg_values, alpha=0.3, color='#00b2eb', label='Kg', width=0.8)
        ax2.set_ylabel(LABEL_WEIGHT, fontsize=12, color='black')
        ax2.tick_params(axis='y', labelcolor='black')
    
    step = max(1, len(indices) // 10)
    ax1.set_xticks(indices[::step])
    ax1.set_xticklabels(date_labels[::step], rotation=45)
    
    plt.title(f'Price Trends for {type}', fontsize=14)
    plt.tight_layout()
    plt.show()


def plot_weight_trend(data_frame, label):
    data_frame[HEADER_DATE] = pd.to_datetime(data_frame[HEADER_DATE], format='%Y%m%d')
    data_frame = data_frame.sort_values(HEADER_DATE)
    
    daily_weights = data_frame.groupby(HEADER_DATE)[HEADER_KG].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    
    plt.bar(
        daily_weights[HEADER_DATE].astype(str), 
        daily_weights[HEADER_KG],
        color='blue',
        label=f'Daily Weight for {label}'
    )
    
    plt.title(f'Daily Weight Trend for {label}', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Total Weight (Kg)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    
    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(nbins=10)) 

    ax.set_xticklabels(daily_weights[HEADER_DATE].dt.strftime('%Y-%m-%d'), rotation=45)
    
    plt.tight_layout()
    plt.show()

def execute_price_analysis(): 
    selected_type = input(f"Enter the type to plot (default: '{default_type}'): ").strip() or default_type
    selected_years = input(f"Enter the years to plot (comma-separated, default: '{default_year}'): ").strip() or default_year
    selected_years = [year.strip() for year in selected_years.split(',')]
    volume_profile_input = input("Show Price Histogram Y / N (Default: N): ").strip() or "N"
    show_volume_profile = volume_profile_input.lower() == 'y'
    show_all_prices_input = input("Show Min / Max prices Y / N (Default: N): ").strip() or "N"
    show_all_prices = show_all_prices_input.lower() == 'y'
    show_volume_input = input("Plot volume bars Y / N (Default: N): ").strip() or "N"
    show_volume = show_volume_input.lower() == 'y'

    print(f"Fetching data for: {selected_type}, years {', '.join(selected_years)}, Histogram : {show_volume_profile}")

    raw = fetch_data(selected_years)
    raw[HEADER_TYPE] = raw[HEADER_TYPE].str.strip()
    selected_data = raw[raw[HEADER_TYPE].str.lower() == selected_type.lower()].copy()

    if selected_data.empty:
        print(f"\nNo data found for '{selected_type}'. Available 'type' values:")
        print(sorted(raw[HEADER_TYPE].dropna().unique(), key=str.lower))
    else:
        plot_price_trend(selected_data, selected_type, show_volume_profile, show_all_prices, show_volume)


def execute_weight_analysis():
    selected_type = input(f"Enter the type to plot (default: '{default_type}'): ").strip() or default_type
    selected_years = input(f"Enter the years to plot (comma-separated, default: '{default_year}'): ").strip() or default_year
    selected_years = [year.strip() for year in selected_years.split(',')]

    print(f"Fetching data for: {selected_type}, years {', '.join(selected_years)}")

    raw = fetch_data(selected_years)
    raw[HEADER_TYPE] = raw[HEADER_TYPE].str.strip()
    
    if selected_type.lower() == "all":
        selected_data = raw.copy()
    else:
        selected_data = raw[raw[HEADER_TYPE].str.lower().str.contains(selected_type.lower(), na=False)].copy()

    if selected_data.empty:
        print(f"\nNo data found for '{selected_type}'. Available 'type' values:")
        print(sorted(raw[HEADER_TYPE].dropna().unique(), key=str.lower))
    else:
        print(selected_data)
        plot_weight_trend(selected_data, selected_type)

if __name__ == "__main__":

    if len(sys.argv) == 1:
        display_help()
        sys.exit(0)

    if '--listtype' in sys.argv:
        listall_index = sys.argv.index('--listtype')
        
        if len(sys.argv) > listall_index + 1:
            years = sys.argv[listall_index + 1].split(',')
        else:
            years = [default_year]
            
        data = fetch_data(years)
        unique_types = sorted(data[HEADER_TYPE].dropna().unique(), key=str.lower)
        for t in unique_types:
                    print(t)

        sys.exit(0)

    if '--listdate' in sys.argv:
        listall_index = sys.argv.index('--listdate')
        
        if len(sys.argv) > listall_index + 1:
            years = sys.argv[listall_index + 1].split(',')
        else:
            years = [default_year]
            
        data = fetch_data(years)
        unique_types = sorted(data[HEADER_DATE].dropna().unique())
        for t in unique_types:
                    print(t)

        sys.exit(0)

    if '--price' in sys.argv:
        execute_price_analysis()

    if '--weight' in sys.argv:
        execute_weight_analysis()

    if '--dryrun' in sys.argv:
        listall_index = sys.argv.index('--dryrun')
        
        if len(sys.argv) > listall_index + 1:
            years = sys.argv[listall_index + 1].split(',')
        else:
            years = [default_year]
            
        data = fetch_data(years)

        sys.exit(0)

    if '--h' in sys.argv:
        display_help()
        sys.exit(1)

    if '--help' in sys.argv:
        display_help()
        sys.exit(1)
        




