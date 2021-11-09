import pandas as pd


class TokenReturn:

    def __init__(self):
        self.launchpad_db_path = '/Users/rodrigow/PycharmProjects/Launchpad_Binance/Launchpad_db/Binance_Launchpad_R1.csv'
        self.token_minute_db_path = '/Users/rodrigow/PycharmProjects/Launchpad_Binance/Token_minute_db/'
        self.token_transform_hour_db_path = '/Users/rodrigow/PycharmProjects/Launchpad_Binance/Token_Transform_db/Minute_BNBUSDT.csv'
        self.token_index = {'BETA':'BNB','C98':'BNB', 'BAR':'USDT', 'TKO':'USDT', 'LINA':'USDT',
                       'DEGO':'USDT', 'ACM':'USDT', 'SFP':'USDT', 'AXS':'BNB', 'INJ':'BNB',
                       'ALPHA':'BNB', 'SAND':'BNB', 'CTSI':'BNB', 'WRX':'BNB', 'TROY':'BNB',
                       'KAVA':'BNB', 'BAND':'BNB', 'PERL':'BNB', 'WIN':'BNB', 'ERD':'BNB',
                       'ONE':'BNB', 'MATIC':'BNB', 'CELR':'BNB', 'FET':'BNB', 'BTT':'BNB', 'BRD':'BNB'}

    @staticmethod
    def generating_launchpad_db():
        """

        :return: get only the tokens that has the BNB compared prices
        Others are duplicated tokens. Set the index to the token names.
        Save into csv.
        """
        df = pd.read_csv('/Users/rodrigow/PycharmProjects/Launchpad_Binance/Launchpad_db/Binance_Launchpad.csv',
                         index_col=1)
        lp_01 = df.drop_duplicates(subset='Token Name')
        lp_02 = lp_01.loc[df['Compared Token Price'] == 'BNB']
        final_launchpad_db = lp_02.drop(['Unnamed: 0'], axis=1)
        return final_launchpad_db

    @staticmethod
    def df_to_csv(data_frame, csv_path_name):
        """

        :param data_frame: data frame that you want to save into csv
        :param csv_path_name: csv file name that you want to save
        :return: data frame
        """
        data_frame.to_csv(csv_path_name)
        return data_frame

    def token_returns(self):
        """

        :return: generate a dictionary with the returns and volume: 1m, 2m, 3m
        """
        final_db = dict()
        contador = 0
        for key, value in self.token_index.items():
            if value == 'BNB':
                # Paths to find TokenBNB files
                minute_path = pd.read_csv(f'{self.token_minute_db_path}{key}{value}.csv')
                launchpad_df = pd.read_csv(self.launchpad_db_path)
                # Returns
                ret_1m = ((minute_path.iloc[1, 1]/launchpad_df.iloc[contador, 2])-1)*100
                ret_2m = ((minute_path.iloc[2, 1]/launchpad_df.iloc[contador, 2])-1)*100
                ret_3m = ((minute_path.iloc[3, 1]/launchpad_df.iloc[contador, 2])-1)*100
                date_launched = launchpad_df.iloc[contador, -1]
                # Save to dict
                final_db[key] = [ret_1h, ret_3h, ret_5h, ret_1d, ret_5d, date_launched]
                contador += 1
            else:

                # Paths to find TokenUSDT files
                hour_path = pd.read_csv(f'{self.token_hour_db_path}{key}{value}.csv')
                daily_path = pd.read_csv(f'{self.token_daily_db_path}{key}{value}.csv')
                launchpad_df = pd.read_csv(self.launchpad_db_path)
                hour_bnb_usdt = pd.read_csv(self.token_transform_hour_db_path)
                daily_bnb_usdt = pd.read_csv(self.tokens_trasnform_daily_br_path)
                # Indexing with the data list
                data_hour_list = hour_bnb_usdt['Date'].tolist()
                data_daily_list = daily_bnb_usdt['Date'].tolist()
                # Returns
                ret_1h = (((hour_path.iloc[1, 1]/hour_bnb_usdt.iloc[data_hour_list.index(hour_path.iloc[1, 0]), 1]) / launchpad_df.iloc[contador, 2]) - 1) * 100
                ret_3h = (((hour_path.iloc[3, 1]/hour_bnb_usdt.iloc[data_hour_list.index(hour_path.iloc[3, 0]), 1]) / launchpad_df.iloc[contador, 2]) - 1) * 100
                ret_5h = (((hour_path.iloc[5, 1]/hour_bnb_usdt.iloc[data_hour_list.index(hour_path.iloc[5, 0]), 1]) / launchpad_df.iloc[contador, 2]) - 1) * 100
                ret_1d = (((daily_path.iloc[1, 1]/daily_bnb_usdt.iloc[data_daily_list.index(daily_path.iloc[1, 0]), 1]) / launchpad_df.iloc[contador, 2]) - 1) * 100
                ret_5d = (((daily_path.iloc[5, 1]/daily_bnb_usdt.iloc[data_daily_list.index(daily_path.iloc[5, 0]), 1]) / launchpad_df.iloc[contador, 2]) - 1) * 100
                date_launched = launchpad_df.iloc[contador, -1]
                # Save to dict
                final_db[key] = [ret_1h, ret_3h, ret_5h, ret_1d, ret_5d, date_launched]
                contador += 1

        return final_db

    @staticmethod
    def final_data_treatment(token_return):
        """

        :param token_return: dictionary of the token returns
        :return: excel table with the token returns and date launch
        """
        # Transforming dict into df and setting column names
        df = pd.DataFrame(token_return).transpose()
        df.rename(columns={0: '1h %', 1: '3h %', 2: '5h %', 3: '1d %', 4: '5d %', 5: 'Date Launched'}, inplace=True)
        # Save into excel
        return df.to_excel('/Users/rodrigow/PycharmProjects/Launchpad_Binance/Return_Results/Final_Results.xlsx')


if __name__ == '__main__':
    token_return_dict = TokenReturn().token_returns()
    TokenReturn().final_data_treatment(token_return_dict)
