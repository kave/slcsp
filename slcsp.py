import argparse
from collections import OrderedDict
import csv
import helper

parser = argparse.ArgumentParser(description='Parser to calculate second lowest cost silver plan (SLCSP)')
parser.add_argument('-s', '--slcsp', help='CSV containing zipcodes of associated silver plans', required=True)
parser.add_argument('-p', '--plans', help='CSV containing all the health plans in the U.S. on the marketplace',
                    required=True)
parser.add_argument('-z', '--zips', help='a mapping of ZIP Code to county/counties & rate area(s)', required=True)

args = vars(parser.parse_args())

# Turn csv's into lists of dictionaries to maintain order
slcsp = helper.parse_csv(args['slcsp'], False)
plans = helper.parse_csv(args['plans'], True)
zips = helper.parse_csv(args['zips'], False)

silver_rate_area_state = OrderedDict()
for silver_plans in slcsp:
    silver_zip = silver_plans['zipcode']
    for zip in zips:
        if silver_zip == zip['zipcode']:
            if silver_zip in silver_rate_area_state:
                # Verifies if that zipcode already has a rate_area, if rate_area differs provide blank answer
                if silver_rate_area_state[silver_zip]['rate_area'] != zip['rate_area']:
                    silver_rate_area_state[silver_zip] = None
                break
            else:
                silver_rate_area_state[silver_zip] = {'rate_area': zip['rate_area'], 'state': zip['state']}

silver_plans = []
answers = OrderedDict()
for zipcode, rate_area_state in silver_rate_area_state.items():
    if not silver_rate_area_state[zipcode]:  # if this valuates to None then set to a blank answer
        answers[zipcode] = ''
    else:
        for plan in plans:
            if rate_area_state['rate_area'] == plan['rate_area'] and rate_area_state['state'] == plan['state']:
                if zipcode in answers:
                    answers[zipcode].append(plan['rate'])
                else:
                    answers[zipcode] = [plan['rate']]

    if zipcode not in answers:
        # Zipcode doesn't have a rate_area/state in plans.csv
        answers[zipcode] = ''

# Write each dictionary of second lowest silver plans to slcsp.csv
helper.write_csv(args['slcsp'], answers)
