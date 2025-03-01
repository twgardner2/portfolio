import pandas as pd

accounts_config = {
    # 'dummy_account': {
    #     'class': 'Bank_Account',
    #     'label':'USAA Savings',
    #     'category': 'bank',
    # },
    'usaa_savings': {
        'class': 'Bank_Account',
        'label':'USAA Savings',
        'category': 'bank',
    },
    'usaa_checking': {
        'class': 'Bank_Account',
        'label':'USAA Checking',
        'category': 'bank',
    },
    'usaa_cd': {
        'class': 'Bank_Account',
        'label':'USAA CD',
        'category': 'bank',
    },
    'wells_fargo_checking': {
        'class': 'Bank_Account',
        'label':'Wells Fargo Checking',
        'category': 'bank',
    },
    'empower_401k': {
        'class': 'Bank_Account',
        'label':'Summit 401K',
        'category': 'retirement',
        'note': '''This is an investment account but I can\'t get the 
                   transaction details, so I treat it like a bank account''',
    },
    't_ira': {
        'class': 'Inv_Account',
        'label':'T IRA',
        'category': 'retirement',
    },
    'j_ira': {
        'class': 'Inv_Account',
        'label': 'J IRA',
        'category': 'retirement',
    },
    'brokerage': {
        'class': 'Inv_Account',
        'label': 'Brokerage',
        'category': 'retirement',
    },
    'trey_529': {
        'class': 'Inv_Account',
        'label': '529 - Trey',
        'category': 'college',
    },
    'louisa_529': {
        'class': 'Inv_Account',
        'label': '529 - Louisa',
        'category': 'college',
    },
    'george_529': {
        'class': 'Inv_Account',
        'label': '529 - George',
        'category': 'college',
    },
    'metron_401k': {
        'class': 'Inv_Account',
        'label': 'Metron 401K',
        'category': 'retirement',
    },
    'thrivent': {
        'class': 'Inv_Account',
        'label': 'Thrivent',
        'category': 'retirement',
    },
    'thrivent_match': {
        'class': 'Inv_Account',
        'label': 'Thrivent Match',
        'category': 'retirement',
    },
    'tsp_civ': {
        'class': 'Inv_Account',
        'label': 'TSP - Civilian',
        'category': 'retirement',
    },
    'tsp_mil': {
        'class': 'Inv_Account',
        'label': 'TSP - Military',
        'category': 'retirement',
    },
    'elston_lane': {
        'class': 'Home_Equity',
        'label': '5236 Elston Lane',
        'category': 'home_equity',
    },
    'chipper_lane': {
        'class': 'Home_Equity',
        'label': '4903 Chipper Lane',
        'category': 'home_equity',
    },
}

annotations = [
    {
        'date': pd.to_datetime('20130531'),
        'text': 'Last Day in Navy',
    },
    {
        'date': pd.to_datetime('20130731'),
        'text': 'Bought Sienna',
    },
    {
        'date': pd.to_datetime('20180630'),
        'text': 'Bought Prius',
    },
    {
        'date': pd.to_datetime('20191016'),
        'text': 'Bought 4903 Chipper Lane',
    },
    {
        'date': pd.to_datetime('20200501'),
        'text': 'Started at Metron',
    },
    {
        'date': pd.to_datetime('20200515'),
        'text': 'Julia started at LOL',
    },
    {
        'date': pd.to_datetime('20150602'),
        'text': 'Started at Summit',
    },
    {
        'date': pd.to_datetime('20210402'),
        'text': 'Sold 5236 Elston Lane',
    },
]

category_annotations = [
    {
        'date': pd.to_datetime('20130531'),
        'text': 'Last Day in Navy',
        'point_to': 'bank' 
    },
    {
        'date': pd.to_datetime('20130731'),
        'text': 'Bought Sienna',
        'point_to': 'bank',
    },
    {
        'date': pd.to_datetime('20180630'),
        'text': 'Bought Prius',
    },
    {
        'date': pd.to_datetime('20191001'), # actual 20191016
        'text': 'Bought 4903 Chipper Lane',
        'point_to': 'bank',
    },
    {
        'date': pd.to_datetime('20200501'),
        'text': 'Started at Metron',
    },
    {
        'date': pd.to_datetime('20200515'),
        'text': 'Julia started at LOL',
    },
    {
        'date': pd.to_datetime('20150602'),
        'text': 'Started at Summit',
    },
    {
        'date': pd.to_datetime('20210402'),
        'text': 'Sold 5236 Elston Lane',
    },
    {
        'date': pd.to_datetime('20210926'),
        'text': 'Started at USAF',
    },
]
