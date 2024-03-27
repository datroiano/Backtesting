from UseFunctions.entries import remove_repeated_strings

sim_tickers_1 = [
    'aapl', 'msft', 'amzn', 'goog', 'fb',     # Big Tech
    'brk', 'jpm', 'v', 'pg', 'ma',            # Finance and Consumer Goods
    'jnj', 'hd', 'unh', 'intc', 'tsla',       # Healthcare and Automobile
    'wmt', 'baba', 't', 'crm', 'ko',          # Retail and Communications
    'cmcsa', 'dis', 'nflx', 'pep', 'abt',     # Media and Consumer Goods
    'adbe', 'nke', 'mcd', 'hon', 'bud',       # Consumer Goods and Beverage
    'tmus', 'axp', 'cost', 'vz', 'mrk',       # Telecom and Pharmaceuticals
    'orcl', 'pfe', 'amgn', 'abbv', 'mdt',     # Technology and Healthcare
    'dhr', 'now', 'acb', 'twtr', 'nclh',      # Healthcare and Social Media
    'tsm', 'amd', 'cat', 'ba', 'sbux',        # Technology and Aerospace
    'csco', 'fdx', 'ge', 'gm', 'hpe',         # Technology and Automotive
    'ibm', 'low', 'lmt', 'mo', 'ups',         # Technology and Retail
    'xom', 'snap', 'tsn', 'mt', 'cl',         # Energy and Consumer Goods
    'k', 'gis', 'clx', 'bmy', 'gild',         # Consumer Goods and Pharmaceuticals
    'tgt', 'wba', 'mnst', 'kmb', 'tjx',       # Retail and Consumer Goods
    'pm', 'mdlz', 'avgo', 'txn', 'mu',        # Technology and Semiconductors
    'nflx', 'nke', 'ko', 'pep', 'bud',        # Beverage and Consumer Goods
    'mo', 'cl', 'k', 'pg', 'pg', 'ko',        # Consumer Goods and Beverage
    'pep', 'mo', 'bmy', 'gild', 'abt',        # Pharmaceuticals and Healthcare
    'dhr', 'tgt', 'wba', 'mnst', 'kmb',       # Retail and Consumer Goods
    'cost', 'tjx', 'pm', 'mdlz', 'cl',        # Consumer Goods
    'k', 'avgo', 'txn', 'mu',                 # Semiconductors and Technology
    'msft', 'amzn', 'goog', 'fb', 'brk',      # Big Tech and Finance
    'jpm', 'v', 'pg', 'ma', 'jnj',            # Finance and Healthcare
    'hd', 'unh', 'intc', 'tsla', 'wmt',       # Retail and Automobile
    'baba', 't', 'crm', 'ko', 'cmcsa',        # Retail and Communications
    'dis', 'pep', 'abt', 'adbe', 'nke',       # Consumer Goods and Media
    'mcd', 'hon', 'bud', 'tmus', 'axp',       # Consumer Goods and Telecom
    'cost', 'vz', 'mrk', 'orcl', 'pfe',       # Pharmaceuticals and Technology
    'amgn', 'abbv', 'mdt', 'dhr', 'now',      # Healthcare and Technology
    'crm', 'acb', 'twtr', 'nclh', 'tsm',      # Social Media and Technology
    'amd', 'cat', 'ba', 'sbux', 'csco',       # Technology and Retail
    'fdx', 'ge', 'gm', 'hpe', 'ibm',          # Technology and Automotive
    'low', 'lmt', 'mo', 'ups', 'xom',         # Energy and Retail
    'snap', 'tsn', 'mt', 'cl', 'k',           # Consumer Goods and Beverage
    'gis', 'clx', 'pg', 'pg', 'ko',           # Consumer Goods and Beverage
    'pep', 'mo', 'bmy', 'gild', 'abt',        # Pharmaceuticals and Healthcare
    'dhr', 'tgt', 'wba', 'mnst', 'kmb',       # Retail and Consumer Goods
    'cost', 'tjx', 'pm', 'mdlz', 'cl',        # Consumer Goods
    'k', 'avgo', 'txn', 'mu'                  # Semiconductors and Technology
]
sim_tickers_1 = remove_repeated_strings(sim_tickers_1)

sim_tickers_2 = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'GOOG', 'FB', 'TSLA', 'BRK.B', 'NVDA', 'JPM',
    'JNJ', 'V', 'PYPL', 'HD', 'MA', 'DIS', 'ADBE', 'BAC', 'CRM', 'XOM',
    'INTC', 'CMCSA', 'VZ', 'NFLX', 'PEP', 'ABT', 'T', 'KO', 'CSCO', 'NKE',
    'MRK', 'PFE', 'WMT', 'ABBV', 'TMO', 'CVX', 'UNH', 'MDT', 'ORCL', 'ACN',
    'AMGN', 'IBM', 'HON', 'TXN', 'UPS', 'LMT', 'DHR', 'NEE', 'AVGO',
    'PM', 'QCOM', 'LOW', 'SBUX', 'LIN', 'PYPL', 'RTX', 'MMM', 'COST', 'GS',
    'BDX', 'CAT', 'AMD', 'BLK', 'BA', 'GE', 'CHTR', 'INTU', 'MS', 'BMY',
    'SPGI', 'TFC', 'ISRG', 'VRTX', 'FIS', 'NOW', 'CVS', 'ANTM', 'TMUS',
    'CCI', 'ZTS', 'CI', 'AMAT', 'AXP', 'MU', 'TJX', 'SYK', 'ADI', 'CSX',
    'LRCX', 'AON', 'PLD', 'NSC', 'USB', 'TGT', 'D', 'ICE', 'SO', 'MET',
    'EQIX', 'DE', 'CL', 'TMO', 'TMO', 'DOW', 'BKNG', 'MDLZ', 'WM', 'VRTX',
    'ZM', 'APD', 'AEP', 'SCHW', 'DUK', 'ILMN', 'SO', 'EMR', 'COF', 'GD',
    'PSX', 'FDX', 'CB', 'ECL', 'GM', 'CME', 'COP', 'KMB', 'ADP', 'ETN',
    'WBA', 'A', 'REGN', 'MCD', 'ROP', 'BDX', 'EOG', 'BIIB', 'ROP', 'KLAC',
    'CCI', 'CI', 'WELL', 'SRE', 'PEG', 'SHW', 'LHX', 'FISV', 'NOC', 'CCI',
    'ED', 'ITW', 'ROST', 'GLW', 'KMI', 'TRV', 'HUM', 'ALGN', 'DTE', 'AIG',
    'MMC', 'MMC', 'SYY', 'PGR', 'WEC', 'ALL', 'AFL', 'KLAC', 'APH', 'MET',
    'EL', 'SYF', 'DFS', 'XLNX', 'IDXX', 'PSA', 'IT', 'KLAC', 'PPL', 'APH',
    'KHC', 'SJM', 'AWK', 'TEL', 'PCAR', 'HCA', 'RMD', 'STZ', 'EXC', 'VLO',
    'GL', 'CNC', 'MNST', 'ABC', 'ESS', 'CDW', 'MXIM', 'LNT', 'FAST', 'ULTA',
    'CTXS', 'PXD', 'DLR', 'ALB', 'DG', 'IQV', 'YUM', 'RE', 'CHD', 'AVB',
    'WLTW', 'VRSK', 'FRC', 'FTV', 'INFO', 'ETR', 'ODFL', 'MSI', 'MKC',
    'AWK', 'VFC', 'HIG', 'AMCR', 'FRT', 'VTRS', 'VMC', 'CBRE', 'NDAQ',
    'DGX', 'HPE', 'TT', 'ETSY', 'ORLY', 'CINF', 'RSG', 'WST', 'OKE', 'BKR',
    'TSCO', 'EFX', 'AMP', 'CTLT', 'CMS', 'IFF', 'ANSS', 'JBHT', 'BR', 'GPC',
    'LKQ', 'KEYS', 'ALXN', 'LUV', 'GRMN', 'AES', 'WY', 'EXPD', 'TTWO', 'TXT',
    'TRMB', 'FLT', 'URI', 'KEY', 'TDG', 'AVY', 'MTB', 'FANG', 'VAR', 'AEE',
    'NCLH', 'FMC', 'PWR', 'BXP', 'TDY', 'BIO', 'EXR', 'PKI', 'ARNC', 'LDOS',
    'WDC', 'ANET', 'HPE', 'PFG', 'BKR', 'PKG', 'SLG', 'KSU', 'IP', 'NTRS',
    'EXPE', 'FTNT', 'WRB', 'HES', 'JBHT', 'NUE', 'LH', 'PAYX', 'EVRG',
    'GLNG', 'FTI', 'FE', 'DRI', 'RCL', 'MGM', 'NVR', 'JBHT', 'AOS', 'ALK',
    'DISCK', 'DISCA', 'POOL', 'IFF', 'LW', 'HII', 'J', 'LEG', 'WRK', 'CINF',
    'F', 'VIAC', 'NVR', 'VIAC', 'SEE', 'UA', 'IPG', 'WRK', 'FLS', 'ALK',
    'HII', 'CF', 'DISCK', 'BEN', 'APA', 'DISCA', 'PWR', 'TAP', 'FLIR', 'CNP',
    'KMX', 'LEG', 'BWA', 'NVR', 'FTI', 'IPGP', 'JWN', 'NLSN', 'ROL', 'PNR',
    'HRB', 'NOV', 'XRX', 'DISCK', 'XRAY', 'ROL', 'UAA', 'XRX', 'SEE', 'EXPD',
    'TXT', 'NVR', 'WRB', 'NCLH', 'CARR', 'PVH', 'J', 'UA', 'DXC', 'FLS',
    'CF', 'NVR', 'DISCA', 'UA', 'BWA', 'HRB', 'FLS', 'PKG', 'NVR', 'VIAC',
    'BEN']

sim_tickers_2 = remove_repeated_strings(sim_tickers_2)

sim_tickers_3 = ['aapl', 'msft']

sim_tickers_3 = remove_repeated_strings(sim_tickers_3)