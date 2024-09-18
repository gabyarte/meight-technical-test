from dotenv import load_dotenv

load_dotenv(override=True)

import streamlit as st
import pandas as pd

from src.settings import settings
from src.vizualize import plot_outliers, plot_data


st.title('Meight Analytic Tool')

def get_choices(field, tablename):
    with settings.DATABASE_ENGINE.connect() as conn:
        query = f'SELECT DISTINCT {field} FROM {tablename}'
        return pd.read_sql(query, conn)


def get_data(tablename, service_type, trailer_type):
    with settings.DATABASE_ENGINE.connect() as conn:
        query = f"SELECT * FROM {tablename} WHERE service_type = '{service_type}' AND trailer_type = '{trailer_type}'"
        return pd.read_sql(query, conn)


service_type_choices = get_choices('service_type', 'test')
trailer_type_choices = get_choices('trailer_type', 'test')

col1, col2 = st.columns(2)

servive_type = col1.selectbox('Choose service type',
                              options=service_type_choices)
trailer_type = col2.selectbox('Choose trailer type',
                              options=trailer_type_choices)

data = get_data('test', service_type=servive_type, trailer_type=trailer_type)

col1, col2, col3 = st.columns(3)
col1.metric('Percentile 25', value=round(data['price'].quantile(q=0.25), 2))
col2.metric('Percentile 75', value=round(data['price'].quantile(q=0.75), 2))
col3.metric('Average', value=round(data['price'].mean(), 2))

st.pyplot(plot_outliers(data['price'],
                        outliers_mask=data['is_outlier'],
                        threshold=1))

st.header('Price Distribution with Outliers')
st.pyplot(plot_data(data['price']))
st.header('Price Distribution without Outliers')
st.pyplot(plot_data(data.loc[~data['is_outlier'], 'price']))
