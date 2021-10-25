import re


# Regular expressions

rx_dumb_date = re.compile(r'(\d{2})/(\d{2})/(\d{4})')
rx_dollar_sign = re.compile(r'\$')
rx_space_should_be_comma = re.compile(r'(?<=\d)\s+(?=[a-zA-Z]+)|(?<=[a-zA-Z])\s+(?=\d)|(?<=\d)\s+(?=\d?)')
rx_newline = re.compile(r'\n')
rx_NEWLINE = re.compile(r'NEWLINE')
rx_zeros = re.compile(r'0\.00, ')
rx_six_columns = re.compile(r'(.*), (.*), (.*), (.*), (.*), (.*)')
rx_four_columns = re.compile(r'(.*), (.*), (.*), (.*)')

# Cleaning function
def clean_file(in_file, acct_name, symbol) :
    with open(in_file) as f:
        lines = f.read()

    cleaned = rx_newline.sub(r'NEWLINE', lines)
    cleaned = rx_dumb_date.sub(r'\g<3>\g<1>\g<2>', cleaned)
    cleaned = rx_dollar_sign.sub(r'', cleaned)
    cleaned = rx_space_should_be_comma.sub(r', ', cleaned)
    cleaned = rx_zeros.sub(r'', cleaned)
    cleaned = rx_NEWLINE.sub(r'\n', cleaned)
    cleaned = rx_six_columns.sub(r'\g<1>, \g<2>, \g<5>, \g<6>', cleaned)
    cleaned = rx_four_columns.sub(fr'{acct_name}, \g<1>, {symbol}, \g<2>, \g<4>, \g<3>', cleaned)

    print(cleaned)

    with open(f'output/{acct_name}_{symbol}.csv', 'w') as f:
        f.writelines(cleaned)


    
clean_file(in_file='data/tsp_g', acct_name='tsp_mil', symbol='g_fund')
clean_file(in_file='data/tsp_c', acct_name='tsp_mil', symbol='c_fund')
clean_file(in_file='data/tsp_s', acct_name='tsp_mil', symbol='s_fund')
clean_file(in_file='data/tsp_l2050', acct_name='tsp_mil', symbol='l2050')

# 
# 
# with open('data/tsp_l2050') as f:
#     lines = f.read()

