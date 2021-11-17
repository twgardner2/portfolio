import pandas as pd

accounts_config = {
    'usaa_savings': {
        'label':'USAA Savings',
        'category': 'bank'
    },
    'usaa_checking': {
        'label':'USAA Checking',
        'category': 'bank'
    },
    'wells_fargo_checking': {
        'label':'Wells Fargo Checking',
        'category': 'bank'
    },
    't_ira': {
        'label':'T IRA',
        'category': 'retirement'
        },
    'j_ira': {
        'label': 'J IRA',
        'category': 'retirement'
        },
    'brokerage': {
        'label': 'Brokerage',
        'category': 'retirement',
        },
    'trey_529': {
        'label': '529 - Trey',
        'category': 'college',
        },
    'louisa_529': {
        'label': '529 - Louisa',
        'category': 'college',
        },
    'george_529': {
        'label': '529 - George',
        'category': 'college',
        },
    'metron_401k': {
        'label': 'Metron 401K',
        'category': 'retirement',
        },
    'thrivent': {
        'label': 'Thrivent',
        'category': 'retirement',
        },
    'tsp_civ': {
        'label': 'TSP - Civilian',
        'category': 'retirement',
        },
    'tsp_mil': {
        'label': 'TSP - Military',
        'category': 'retirement',
        },
}

annotations = [
    {'date': pd.to_datetime('20130531'),
     'text': 'Last Day in Navy',
    },
    {'date': pd.to_datetime('20130731'),
     'text': 'Bought Sienna'
    },
    {'date': pd.to_datetime('20180630'),
     'text': 'Bought Prius'
    },
    {'date': pd.to_datetime('20191016'),
     'text': 'Bought 4903 Chipper Lane'
    },
    {'date': pd.to_datetime('20200501'),
     'text': 'Started at Metron'
    },
    {'date': pd.to_datetime('20150602'),
     'text': 'Started at Summit'
    },
    {'date': pd.to_datetime('20210402'),
     'text': 'Sold 5236 Elston Lane'
    },
]

category_annotations = [
    {'date': pd.to_datetime('20130531'),
     'text': 'Last Day in Navy',
     'point_to': 'bank' 
    },
    {'date': pd.to_datetime('20130731'),
     'text': 'Bought Sienna',
     'point_to': 'retirement'
    },
    {'date': pd.to_datetime('20180630'),
     'text': 'Bought Prius'
    },
    {'date': pd.to_datetime('20191016'),
     'text': 'Bought 4903 Chipper Lane'
    },
    {'date': pd.to_datetime('20200501'),
     'text': 'Started at Metron'
    },
    {'date': pd.to_datetime('20150602'),
     'text': 'Started at Summit'
    },
    {'date': pd.to_datetime('20210402'),
     'text': 'Sold 5236 Elston Lane'
    },
]
