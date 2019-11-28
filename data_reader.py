import pandas as pd

folder_name = 'data_generation/'
case_name = 'Prime1m_10_false_Thread_200_99th/'

data = pd.read_csv(folder_name + '99th_percentile.csv')

throughput = data.iloc[:, 0]
