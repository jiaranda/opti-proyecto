import pandas as pd
import requests
import json
from math import isnan


data = pd.read_csv('./data/database.csv', sep=';')

# medical centers

def add_id_to_medical_centers(data):
    medical_centers = data.CENTRO.unique()
    # fix string format
    for i in range(len(medical_centers)):
        medical_centers[i] = medical_centers[i].replace('\xa0', ' ')

    enumerated = dict()
    for mc_id, name in enumerate(medical_centers, start=1):
        enumerated[name] = mc_id

    for index, row in data.iterrows():
        for key, value in enumerated.items():
            if row['CENTRO'] == key:
                data.loc[index, 'ID_LUGAR'] = value
    return medical_centers, enumerated


medical_centers, enumerated = add_id_to_medical_centers(data)


# modules, days, months and medics

modules = [1, 2]
days = list(range(1, 25))
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
medics = data.ID_MEDICO.unique().tolist()


# medical center boxes

medical_center_boxes = dict()
for med_id in data.ID_LUGAR.unique():
    medical_center_boxes[med_id] = list(range(1,21))


# connect to Google Maps API to get times between medical centers

def get_data_from_maps_api(medical_centers, enumerated):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric'
    headers = {
        'authority': 'maps.googleapis.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'es-419,es;q=0.9,en;q=0.8',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }


    # get all medical center combinations
    medical_centers_combinations = list()
    for i in medical_centers:
        for j in medical_centers:
            medical_centers_combinations.append((i, j))

    time_between = dict()

    for pair in medical_centers_combinations:
        origin = pair[0] + ' REDSALUD, CHILE'
        destination = pair[1] + ' REDSALUD, CHILE'
        request_text = url + '&origins=' + origin + '&destinations=' + destination + '&key=AIzaSyBVVOTvCC_sbViOkqq8q64563ss5zafdAM'
        req = requests.get(request_text, headers=headers)
        res = req.json()
        time_between[(enumerated[pair[0]], enumerated[pair[1]])] = int(res['rows'][0]['elements'][0]['duration']['value'])/(60*60) # from seconds to hours
    return time_between

time_between = get_data_from_maps_api(medical_centers, enumerated)


# Medic notification rate

def get_notification_rates(data):
    medic_stats = dict()
    for med_id in data.ID_MEDICO.unique():
        medic_stats[med_id] = {'notified': 0, 'not_notified': 0, 'not_ges': 0}
    for index, row in data.iterrows():
        # notified
        if not isnan(row['ID_AGRUPADOR']):
            medic_stats[row['ID_MEDICO']]['notified'] += 1
        # not notified but should
        elif isnan(row['ID_AGRUPADOR']) and (not isnan(row['POTENCIAL_1']) or not isnan(row['POTENCIAL_2']) or not isnan(row['POTENCIAL_3'])):
            medic_stats[row['ID_MEDICO']]['not_notified'] += 1
        elif not isnan(row['ID_AGRUPADOR']) and not isnan(row['POTENCIAL_1']) and not isnan(row['POTENCIAL_2']) and not isnan(row['POTENCIAL_3']):
            medic_stats[row['ID_MEDICO']]['not_ges'] += 1
    notification_rates = dict()
    for key, value in medic_stats.items():
        notification_rates[key] = value['notified']/(value['not_notified'] + value['notified']) if value['not_notified'] != 0 else 1.0
    return notification_rates

notification_rates = get_notification_rates(data)
