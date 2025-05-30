# FMFO

The project contains data that has been scraped from [Faroe Fish Market](https://fmf.fo/), and compiled into csv files by year. 

Included in the project is a python script that allows the user to analyze the compiled data.

## Overview
| CSV Data | Python Script | 
| :---:   | :---: |
| ![Demo2](img/demo2.png) | ![Demo1](img/demo1.png)

## Usage

### Prerequisites
The script relies on the following Python libraries:

`pandas`: Data manipulation and analysis.

`matplotlib`: Plotting data on chart.

`numpy`: Used for numerical operations.

#### Install the required libraries:
you can install all the dependencies from the **requirements.txt** file using the following command:
```
pip install -r requirements.txt
```

### Running the script

Execute the command
```
python fmf.py --price
```

The script will prompt you for an item to plot
```
Enter the type to plot (default: 'Hysa 1 MSC'): [INPUT YOUR ITEM HERE, ex : Toskur 1]
```
After the item, the script will ask for a year
```
Enter the year to plot (default: '2025'): 
```
Finally, the script will ask for volume profile, if it should be activated or not
```
Show Volume Profile Y / N (Default: Y)
```
Script will start to analyze the data based on the input given
```
Plotting data for: Toskur 1, years 2025, volume profile: True
```
![Demo](img/demo1.png)

---
<br/>

### Listing Available Types

To display all available **types**, run:

```
python fmf.py --listtype 2024
```
and the script will output all **unique** types for the given year
```
Available types:
Hysa 1 MSC
Hysa 2 MSC
Hysa 3 MSC
Hysa 4 MSC
Hysa MSC
Toskur 1
Toskur 2
Toskur 3
Toskur 4
Toskur 5
Hvitlingur
Upsi 1 MSC
Upsi 2 MSC
Upsi 1-2 MSC
Upsi 3 MSC
Upsi 4 MSC
Upsi 5 MSC
.....
```

---
<br/>

### Analysing Weight
The script comes with a function that allows the user to analyse the Total Daily Weight for a sepecif type. Execute the command
```
python fmf.py --weight
```
The script will prompt you for an type to plot
```
Enter the type to plot (default: 'Hysa 1 MSC'): [INPUT YOUR ITEM HERE, ex : Toskur 1]
```
After the item, the script will ask for a year, you can add multiple year by adding a command separated list (2023,2024,2025)
```
Enter the year to plot (default: '2025'): 
```
Script will start to analyze the data based on the input given
![Demo](img/demo3.png)

## Note
The data is collected by an AI-powered crawler that decodes image files (JPEG, PNG) into CSV format. As a result, some text may have inconsistent spelling, particularly with Nordic characters, as the crawler may struggle with properly decoding these letters.

