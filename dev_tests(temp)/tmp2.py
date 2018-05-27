from core.etender_data import homePage


def get_home_page():
    print(homePage.get('QA', {}).get('ProzorroQA'))
    return homePage.get('QA', {}).get('ProzorroQA')

if __name__ == "__main__":
    get_home_page()
