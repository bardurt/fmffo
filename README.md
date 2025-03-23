# FMFO

The project contains data that has been scraped from [Faroe Fish Market](https://fmf.fo/), and compiled into csv files by year. 

Included in the project is a python script that allows the user to analyze the compiled data.

| csv | python    | 
| :---:   | :---: |
| ![Demo2](img/demo2.png) | ![Demo1](img/demo1.png)


### Running the script

Execute the command
```
python3 fmf.py
```

The script will prompt you for an item to plot
```
Enter the type to plot (default: 'Hysa 1 MSC'): [INPUT YOUR ITEM HERE, ex : Toskur 1]
```
Afer the item, the script will ask for a year (At the moment data is only available for 20205)
```
Enter the year to plot (default: '2025'): 

```
Script will start to analyse the data based on the input given
```
Plotting data for: Toskur 1, year 2025
```
![Demo](img/demo1.png)