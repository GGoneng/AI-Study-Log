import csv

def get_index_of_age_csv():
    with open("age.csv", encoding = "euc_kr") as f:
        data = csv.reader(f)
        header = next(data)

        print("-" * 50)
        print("  age.csv index ")
        print("-" * 50)

        for i in range(len(header)):
            print(F"[{i:3}]: {header[i]}")

get_index_of_age_csv()