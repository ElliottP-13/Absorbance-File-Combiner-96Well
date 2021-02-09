# File Combiner

Author: Elliott Pryor

## Run:

Run File_combiner.py

You will need to change the very last line of the File_Combiner.py to change which organism to combine.
You will change 
```python
main('YOUR ORGANISM')
```
The ```'YOUR ORGANISM'``` needs to match the folder name in which the files you wish to combine are.

For example, if the files are stored in ```CG23.4 PM Plates``` it would be 

```python
main('CG23.4 PM Plates')
```

## Adding Data:

When inputting more data (xlsx files). Put them within the ```Data/``` folder. 
The program assumes that all data files are stored there.
If you wish to change this, change
```python
path_to_files = 'Data/'
```
at the top of ```File_Combiner.py``` to the path of where the data files are stored

## Output format

The default is to output into a csv format. 
You can then save this as an excel (xlsx) or anything you want.
If you do this, Excel will automatically detect the time and date and format the cells accordingly 
(no need to do the process listed below)

If you want to save directly as an excel you can uncomment lines 111-114
```python
    dataframe['time'] = pd.to_datetime(dataframe['time'], format="%H:%M")
    dataframe['date'] = pd.to_datetime(dataframe['date'], format="%m/%d")

    dataframe.to_excel(path_to_files + '/results/' + organism + '.xlsx')  # save as Excel
```

The time and date columns in the resulting .xlsx file will be just a sequence of '#' symbols.
You will need to select these columns, right click, format, then time/date in order for them to be human-legible.
