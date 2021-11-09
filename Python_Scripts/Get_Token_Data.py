from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd


class RequestTokenData:

    def __init__(self):
        self.api_key = ''
        self.api_secret = ''
        self.time_frame = ['1d', '1h']
        self.directory_path = ['/Users/rodrigow/PycharmProjects/launchpad_binance_r1/Token_daily_db/',
                               '/Users/rodrigow/PycharmProjects/launchpad_binance_r1/Token_hour_db/']

    def initialize(self, token_name, time_frame, csv_name):
        """

        :param token_name: token name to get data from Binance API
        :param time_frame: time frame that you want the token informations
        :param csv_name: csv file name to save the data
        :return:
        """
        # Initializing the API
        client = Client(self.api_key, self.api_secret)
        timestamp = client._get_earliest_valid_timestamp(token_name, time_frame)
        bars = client.get_historical_klines(token_name, time_frame, timestamp, limit=1000)
        # Deleting unwanted data
        for line in bars:
            del line[7:]
        # Transforming into df
        btc_df = pd.DataFrame(bars, columns=['Date',
                                             'Open',
                                             'High',
                                             'Low',
                                             'Close',
                                             'Volume',
                                             'Close Time'])
        btc_df.set_index('Date', inplace=True)
        # Export the df to csv
        return btc_df.to_csv(f'{csv_name}.csv')

    @staticmethod
    def save_dict_txt(text_file_name, token_dict):
        """

        :param text_file_name: txt file name that you want to save
        :param token_dict: dictionary that you want to save
        :return: dictionary saved into a local txt file
        """
        with open(f'{text_file_name}.txt', 'w') as f:
            for key, value in token_dict.items():
                f.write(f'{key}:{value}')
        return f'File {text_file_name}.txt saved successfully.'

    def get_daily_db(self):
        """

        :return: get daily db of launchpad tokens
        """
        data = pd.read_csv('/Users/rodrigow/PycharmProjects/launchpad_binance_r1/Launchpad_db/Binance_Launchpad.csv')
        token_list = list(data.iloc[:, 1])
        index_dict = dict()
        for token in token_list:
            try:
                token_name = (token+'BNB')
                RequestTokenData().initialize(token_name, self.time_frame[0], ((self.directory_path[0])+token_name))
                index_dict[token] = 'BNB'
            except BinanceAPIException:
                token_name = (token + 'USDT')
                RequestTokenData().initialize(token_name, self.time_frame[0], ((self.directory_path[0])+token_name))
                index_dict[token] = 'USDT'
        RequestTokenData().save_dict_txt('/Users/rodrigow/PycharmProjects/launchpad_binance_r1/Dict_indexes/Index_Daily_Dict', index_dict)
        return index_dict

    def get_hour_db(self):
        """

        :return: get hour db of launchpad tokens
        """
        data = pd.read_csv('/Users/rodrigow/PycharmProjects/launchpad_binance_r1/Launchpad_db/Binance_Launchpad.csv')
        token_list = list(data.iloc[:, 1])
        index_dict = dict()
        for token in token_list:
            try:
                token_name = (token + 'BNB')
                RequestTokenData().initialize(token_name, self.time_frame[1], ((self.directory_path[1]) + token_name))
                index_dict[token] = 'BNB'
            except BinanceAPIException:
                token_name = (token + 'USDT')
                RequestTokenData().initialize(token_name, self.time_frame[1], ((self.directory_path[1]) + token_name))
                index_dict[token] = 'USDT'
        RequestTokenData().save_dict_txt('/Users/rodrigow/PycharmProjects/launchpad_binance_r1/Dict_indexes/Index_Hour_Dict', index_dict)
        return index_dict


if __name__ == '__main__':
    RequestTokenData().get_hour_db()
    RequestTokenData().get_daily_db()
    RequestTokenData().initialize('BNBUSDT', '1d', '/Users/rodrigow/PycharmProjects/launchpad_binance_r1/Token_Transform_db/Daily_BNBUSDT')
    RequestTokenData().initialize('BNBUSDT', '1h', '/Users/rodrigow/PycharmProjects/launchpad_binance_r1/Token_Transform_db/Hour_BNBUSDT')


