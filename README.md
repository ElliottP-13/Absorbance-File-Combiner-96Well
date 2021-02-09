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