import pandas as pd
import os
import requests
import schedule


def get_access_token():
    headers = {
        'Host': 'api-con.arbeitsagentur.de',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Accept-Language': 'en-us',
        'User-Agent': 'Jobsuche/1070 CFNetwork/1220.1 Darwin/20.3.0',
    }
    data = {
        'client_id': 'c003a37f-024f-462a-b36d-b001be4cd24a',
        'client_secret': '32a39620-32b3-4307-9aa1-511e3d7f48a8',
        'grant_type': 'client_credentials'
    }
    response = requests.post('https://api-con.arbeitsagentur.de/oauth/gettoken_cc', headers=headers, data=data)
    access_token = response.json()
    return access_token['access_token']


def get_data():
    url = "https://api-con.arbeitsagentur.de/prod/jobboerse/jobsuche-service/pc/v2/app/jobs?FCT.ANGEBOTSART=PRAKTIKUM_TRAINEE&size=50"
    headers = {
      'Content-Type': 'application/json',
      'Content-Length': '0',
      'Authorization': 'Bearer %s' % get_access_token(),
    }
    response = requests.request("GET", url, headers=headers, data={})
    to_be_process_data = response.json()
    job_search_datas = to_be_process_data["_embedded"]["jobs"]
    job_result = [{
            'ort': data["arbeitsort"]["ort"] if 'arbeitsort' in data and 'ort' in data["arbeitsort"] else False,
            'strasse': data["arbeitsort"]["ort"] if 'arbeitsort' in data and 'ort' in data["arbeitsort"] else False,
            'plz': data["arbeitsort"]["plz"] if 'arbeitsort' in data and 'plz' in data["arbeitsort"] else False,
            'arbeitgeber': data["arbeitgeber"],
            'name_der_ausbildung': data["hauptberuf"],
            'eintrittsdatum' : data["eintrittsdatum"],
        }for data in job_search_datas]
    process_data = pd.DataFrame(job_result)
    process_data.to_excel(os.getcwd() + '/' + 'job_search.xlsx')
schedule.every(2).seconds.do(get_data)
while True:
  schedule.run_pending()
