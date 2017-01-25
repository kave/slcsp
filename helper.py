import csv


# Turn CSV rows into an array of dictionaries per row
def parse_csv(file_path=None, silver_plan_flag=False):
    data = []
    with open(file_path, 'r') as file_obj:
        reader = csv.DictReader(file_obj)

        if silver_plan_flag:
            for row in reader:
                if row['metal_level'] == 'Silver':
                    data.append(row)
        else:
            for row in reader:
                data.append(row)
        next(reader, None)
    return data



def write_csv(file_path=None, data_dict={}):
    with open(file_path, 'w') as f:
        writer = csv.DictWriter(f, ['zipcode', 'rate'], lineterminator='\n')
        writer.writeheader()

        for zipcode, rates in data_dict.items():
            if len(rates) > 1:
                rates.sort()
                writer.writerow({'zipcode': zipcode, 'rate': rates[1]})
            else:
                writer.writerow({'zipcode': zipcode, 'rate': str(rates)})
