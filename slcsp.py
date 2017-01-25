import argparse
from collections import OrderedDict
import csv

parser = argparse.ArgumentParser(description='Parser to calculate second lowest cost silver plan (SLCSP)')
parser.add_argument('-s', '--slcsp', help='CSV containing zipcodes of associated silver plans', required=True)
parser.add_argument('-p', '--plans', help='CSV containing all the health plans in the U.S. on the marketplace',
                    required=True)
parser.add_argument('-z', '--zips', help='a mapping of ZIP Code to county/counties & rate area(s)', required=True)

args = vars(parser.parse_args())

def parse_csv(arg_name, silver_plan_flag):
    data = []
    with open(args[arg_name], 'r') as file_obj:
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


# Turn csv's into lists of dictionaries to maintain order
slcsp = parse_csv('slcsp', False)
plans = parse_csv('plans', True)
zips = parse_csv('zips', False)

count = 0
silver_rate_area_state = OrderedDict()
for silver_plans in slcsp:
    silver_zip = silver_plans['zipcode']
    for zip in zips:
        if silver_zip == zip['zipcode']:
            silver_rate_area_state[silver_zip] = {'rate_area': zip['rate_area'], 'state': zip['state']}

silver_plans = []
answers = OrderedDict()
for zip, rate_area_state in silver_rate_area_state.items():
    for plan in plans:
        if rate_area_state['rate_area'] == plan['rate_area'] and rate_area_state['state'] == plan['state']:
            if zip in answers:
                answers[zip].append(plan['rate'])
            else:
                answers[zip] = [plan['rate']]

for zip, rates in answers.items():
    if len(rates) > 1:
        rates.sort()
        print zip + ', %s' % rates[1]
    else:
        print zip + ', ' + rates[0]
