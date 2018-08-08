res = {'success': True,
       'result': {'list':
                      [
                          {'responsibles': None, 'tenderNewId': '388279296f7d4e37beec30a0c958a93f', 'userId': 1247, 'asHead': True},
                          {'responsibles': None, 'tenderNewId': 'e1cda0297dd842f2813ca530ee9ca6b8', 'userId': 1247, 'asHead': True},
                          {'responsibles': None, 'tenderNewId': '4300ccc932a846e1a04b2569bd27236f', 'userId': 1247, 'asHead': True},
                      ]
       },
       'error': None,
       'unAuthorizedRequest': False}

chain = [
    {"tenderNewId": "388279296f7d4e37beec30a0c958a93f", "userId": 1247},
    {"tenderNewId": "e1cda0297dd842f2813ca530ee9ca6b8", "userId": 1247},
    {"tenderNewId": "4300ccc932a846e1a04b2569bd27236f", "userId": 1248}
        ]


def assure_tender_list_assigned_to_user(assignment_result, tender_user_chains):
    c = 0
    chains_count = len(tender_user_chains)
    for i in assignment_result['result']['list']:
        for j in tender_user_chains:
            if i['tenderNewId'] == j['tenderNewId'] and i['userId'] == j['userId']:
                c += 1
            else:
                pass
    if chains_count == c:
        return True
    else:
        return False


if __name__ == '__main__':
    print(assure_tender_list_assigned_to_user(res, chain))


