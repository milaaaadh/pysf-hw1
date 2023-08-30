# import library


from flask import Flask, jsonify, request
import json
import requests


### define functions

# create comment on issue

def create_comment(vts_key, message):
    headers = {
        'authority': 'jira.snappfood.ir',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'content-type': 'application/json',
        'Authorization': 'Basic bWVoZGkuaGFiaWJpOnV2NWFqcGcxMjg4M2s5NjJkM2ZzdW9jZTVxYTRsNjY1OA==',
        'origin': 'https://jira.snappfood.ir',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    json_data = {
        "body": f"{message}",
        'properties': [
            {
                'key': 'sd.public.comment',
                'value': {
                    'internal': True,
                },
            },
        ]}
    response = requests.post(f'https://jira.snappfood.ir/rest/api/2/issue/{vts_key}/comment', headers=headers,
                             json=json_data)
    return response.json()


# get vendor id and manager phone number

def get_vendor_id(issue_key):
    headers = {
        'authority': 'jira.snappfood.ir',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'cache-control': 'max-age=0',
        'Authorization': 'Basic bWVoZGkuaGFiaWJpOnV2NWFqcGcxMjg4M2s5NjJkM2ZzdW9jZTVxYTRsNjY1OA==',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'fields': [
            'customfield_10305',
            'customfield_10302',
        ],
    }

    response = requests.get(f'https://jira.snappfood.ir/rest/api/2/issue/{issue_key}', params=params, headers=headers)
    vendor_id = response.json()['fields']['customfield_10305']
    manager_phone = response.json()['fields']['customfield_10302']
    return vendor_id, manager_phone


# search issues for get last day tickets


def search_issue(vendor_id):
    headers = {
        'authority': 'jira.snappfood.ir',
        '__amdmodulename': 'jira/issue/utils/xsrf-token-header',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Authorization': 'Basic bWVoZGkuaGFiaWJpOnV2NWFqcGcxMjg4M2s5NjJkM2ZzdW9jZTVxYTRsNjY1OA==',
        'origin': 'https://jira.snappfood.ir',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-atlassian-token': 'no-check',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'startIndex': '0',
        'filterId': '-4',
        'jql': f'project = ZS AND summary ~ "درخواست آموزش نرم افزار دخل" AND "Vendor ID" ~ "{vendor_id}" AND created >= -24h ORDER BY updated DESC, created DESC',
        'layoutKey': 'split-view',
    }

    response = requests.post('https://jira.snappfood.ir/rest/issueNav/1/issueTable', headers=headers, data=data)
    return response.json()['issueTable']['total']


# send sms on pishgaman


def send_sms(number, message):
    headers = {
        'accept': 'application/json',
        'Authorization': '907C2D6D63481A64B93A7EF5FB6A5A647DDF51E2F3723E2BB785F86149927BD77D0F0D14AA29ACFA96448FDFFFE8CBC73C414743D8786C30CC031E68D1DD58B7245528ED498CEA180B364EFC2E43669FDA1E29B35A4F065850CFBC925C1C5F27E11C4D11B50924E2989A45134F143B1F',
        'Content-Type': 'application/json',
    }
    json_data = {
        'messageBodies': [f"{message}"],
        'recipientNumbers': [
            f'{number}',
        ],
        'senderNumber': '50003311',
    }

    response = requests.post('https://api.pishgamrayan.com/Send', headers=headers, json=json_data)
    return response


# call automation jira

def automation(issues):
    headers = {
        'authority': 'jira.snappfood.ir',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
        'content-type': 'application/json',
        'Authorization': 'Basic bWVoZGkuaGFiaWJpOnV2NWFqcGcxMjg4M2s5NjJkM2ZzdW9jZTVxYTRsNjY1OA==',
        'origin': 'https://jira.snappfood.ir',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    json_data = {
        "issues": [issues

                   ]
    }
    response = requests.post(
        f'https://jira.snappfood.ir/rest/cb-automation/latest/hooks/75cacffa93dc4cbd9b808ee641a67d24e68f3eb5',
        headers=headers, json=json_data)
    return response


# Flask webhook

app = Flask(__name__)


@app.route('/jira_sms', methods=['POST', 'GET'])
def login():
    # send_sms = 303
    # pend_ticket = 505
    vts_link = request.args.get('vts_link')
    message = "همکار گرامی اسنپ فود\nبا توجه به درخواست شما به شماره " + vts_link + "  ، لطفا در صورتی که نیازمند نصب یا آموزش نرم افزار دخل هستید به آدرس زیر مراجعه نمایید.\nآدرس :\nyun.ir/Dakhl\nهمچنین در صورت عدم رفع مشکل، لطفا مجددا درخواست ثبت نمایید\n\nبا تشکر از همکاری شما"
    vendor_id, manager_phone = get_vendor_id(vts_link)
    result_search = search_issue(vendor_id)
    print(vendor_id, manager_phone, result_search, type(result_search))
    file_path = '/home/mehdi.habibi/JiraWebhook./test.txt'
    file1 = open(file_path, "a")

    if result_search <= 1:
        sms_details = send_sms(manager_phone, message)
        print(sms_details)
        automation(vts_link)
        new_data = {vts_link: {"vendor_id": vendor_id, "result_search": result_search, "ersal_sms": sms_details.json()}}
        file1.write(f"{new_data} \n")
        file1.close()
        print(new_data)
        return json.dumps({'status': 'Send Sms'}), 303
    if result_search >= 2:
        new_data = {vts_link: {"vendor_id": vendor_id, "result_search": result_search, "ersal_sms": "False"}}
        create_comment(vts_link, "ویدئو قبلا ارسال شده")
        file1.write(f"{new_data} \n")
        file1.close()
        print(new_data)
        return json.dumps({'status': 'Pending ticket'}), 505


if __name__ == '__main__':
    app.run('192.168.20.149', port='8100')
