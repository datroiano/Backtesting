import requests
import pandas as pd
from UseFunctions.date_time import two_date_period, previous_day, get_date_next_friday
from StockClasses.single_stock import SingleStock
from OptionClasses.Contracts.contract_spread import ContractSpread
from OptionClasses.Strategies.straddle import StraddleStrategy


class EarningsLookup:
    def __init__(self, from_date: str, to_date: str, report_time: str = 'any', remove_empties: bool = True,
                 api_key: str = 'sS3gwZ7cycpxe9G7JSAmwigdeOjvN2B4') -> None:
        self.from_date = from_date
        self.to_date = to_date
        self.report_time = report_time
        self.remove_empties = remove_empties
        self.api_key = api_key
        self.raw_data = self._get_earnings()
        self.earnings_output = self._clean_data()

    def _get_earnings(self) -> dict or None:
        url = f"https://financialmodelingprep.com/api/v3/earning_calendar?from={self.from_date}&to={self.to_date}&apikey={self.api_key}"
        response = requests.get(url)

        if response.status_code == 401:
            print("Unauthorized earnings API access. Check your API key.")
            return None

        return response.json()

    def _clean_data(self):
        if self.report_time.lower() == 'any':
            filtered_data = self.raw_data
        else:
            filtered_data = [i for i in self.raw_data if i.get('time') == self.report_time.lower()]

        clean_data = [i for i in filtered_data if
                      {'date', 'symbol', 'time', 'eps', 'revenueEstimated', 'revenue'}.issubset(
                          i.keys()) and '.' not in i.get('symbol', '') and (
                              not self.remove_empties or all(v is not None for v in i.values()))]

        return pd.DataFrame(clean_data)

    def get_specific_company(self, ticker: str) -> pd.DataFrame:
        return self.earnings_output[self.earnings_output['symbol'] == ticker.upper()]


class StrategyTestInputs:
    def __init__(self, tickers, entry_exit_period: tuple, lookup_period_months=3, report_time='any',
                 test_quantity: int = 1, per_contract_commission: float = 0.01,
                 polygon_api_key='r1Jqp6JzYYhbt9ak10x9zOpoj1bf58Zz'):
        self.tickers = tickers
        self.lookup_period_months = lookup_period_months
        self.report_time = report_time
        self.to_search_date, self.from_search_date = two_date_period(lookup_period_months)
        self.entry_exit_period = entry_exit_period
        self.entry1, self.entry2, self.exit1, self.exit2 = self.entry_exit_period
        self.quantity = test_quantity
        self.per_contract_commission = per_contract_commission
        self.polygon_api_key = polygon_api_key
        self.errors_list = []
        self.search_criteria = self._get_search_criteria()
        self.inputs_list = self._get_inputs_list()

    def _get_search_criteria(self):
        earnings_lookup = EarningsLookup(from_date=self.from_search_date, to_date=self.to_search_date,
                                         report_time=self.report_time)
        earnings_output = earnings_lookup.earnings_output

        search_criteria = []
        errors_list = []

        for ticker in self.tickers:
            ticker_earnings = earnings_output[earnings_output['symbol'] == ticker.upper()]
            if not ticker_earnings.empty:
                search_criteria.extend(ticker_earnings.to_dict(orient='records'))
            else:
                errors_list.append({'ticker': ticker, 'error': 'Earnings Calendar Search'})

        self.errors_list = errors_list

        return search_criteria

    def _get_inputs_list(self) -> (list[dict], list[dict]):
        inputs_list = []
        errors_list = []
        for company in self.search_criteria:
            underlying = company['symbol'].upper()
            trade_date = previous_day(company['date']) if company['time'] == 'bmo' else company['date']
            expiration_date = get_date_next_friday(trade_date)
            try:
                average_entry_underlying = SingleStock(ticker=underlying, from_date=trade_date, from_time=self.entry1,
                                                       to_date=trade_date, to_time=self.entry2,
                                                       fill_gaps=False).get_average_price()
            except TypeError:
                errors_list.append({'ticker': underlying, 'error': 'TypeError Stock'})
                continue
            except KeyError:
                errors_list.append({'ticker': underlying, 'error': 'KeyError Stock'})
                continue
            except ValueError:
                errors_list.append({'ticker': underlying, 'error': 'ValueError Stock'})
                continue
            try:
                strike = ContractSpread(
                    underlying, current_underlying=average_entry_underlying,
                    expiration_date_gte=expiration_date,
                    date_as_of=trade_date).get_best_matched_contracts()[0]['strike_price']

                entry = {
                    'ticker': underlying,
                    'strike': strike,
                    'expiration_date': expiration_date,
                    'entry_date': trade_date,
                    'exit_date': trade_date,
                }

                inputs_list.append(entry)
            except TypeError:
                errors_list.append({'ticker': underlying, 'error': 'TypeError Spread'})
                continue
            except KeyError:
                errors_list.append({'ticker': underlying, 'error': 'KeyError Spread'})
                continue
            except ValueError:
                errors_list.append({'ticker': underlying, 'error': 'ValueError Spread'})
                continue

        self.errors_list.extend(errors_list)

        return inputs_list

    def aggregate_ticker_simulations(self) -> (pd.DataFrame, list[dict]):
        all_simulations = []  # List to store all simulation DataFrames`
        errors_list = []
        for input_company in self.inputs_list:
            try:
                sim_inputs = StraddleStrategy(ticker=input_company['ticker'],
                                              strike=input_company['strike'],
                                              expiration_date=input_company['expiration_date'],
                                              quantity=self.quantity,
                                              entry_date=input_company['entry_date'],
                                              exit_date=input_company['exit_date'],
                                              strategy_type='long',
                                              entry_exit_period=self.entry_exit_period,
                                              timespan='minute',
                                              fill_gaps=True,
                                              per_contract_commission=self.per_contract_commission,
                                              multiplier=1,
                                              polygon_api_key=self.polygon_api_key)

                simulation = sim_inputs.run_simulation()

                if simulation is not None:  # Check if simulation is not None
                    all_simulations.append(simulation)  # Append each simulation DataFrame to the list
            except KeyError:
                errors_list.append({'ticker': input_company['ticker'], 'error': 'KeyError Strategy'})
                continue

        full_sims = pd.concat(all_simulations, ignore_index=True)  # Concatenate all simulation DataFrames

        self.errors_list.extend(errors_list)

        return full_sims


tickers = [
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

tickers2 = [
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

x = StrategyTestInputs(tickers, entry_exit_period=('10:30:00', '11:30:00', '15:30:00', '16:00:00'), lookup_period_months=5)
sims = x.aggregate_ticker_simulations()
errors = x.errors_list

