import pandas as pd

def main(filename):
    path = './Data/results/'
    df = pd.read_csv(path + filename + '.csv')
    # print(df.head())

    plates = ['PM1 ', 'PM2A ']
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    cols = [p + l + str(i + 1) for p in plates for l in letters for i in range(12)]
    # print(cols)

    dataframe = {}

    for col in df.columns:
        if col not in cols:
            dataframe[col] = df[col]
            continue
        # print(col)
        v = df[col].values
        m = max(v)
        if m > 0.3:
            dataframe[col] = df[col]

    dataframe = pd.DataFrame(dataframe)
    dataframe.to_csv(path + filename + '_growing.csv')  # save as a csv


files = ['CG23.3 PM Plates', 'CG23.4 PM Plates', 'PL17 PM Plates', 'PL19 PM Plates', 'PL20H PM Plate']
for f in files:
    print(f)
    main(f)
