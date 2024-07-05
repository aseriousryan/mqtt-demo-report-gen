import os
import time

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import streamlit as st
from io import BytesIO
# from streamlit import cli
# from streamlit.report_thread import get_report_ctx
# from watchdog.events import FileSystemEventHandler

import plot

# Sample DataFrame for illustration purposes
file_path = r'/home/seriousco/Documents/adli/machinery_data/dummy_data.csv'
df_A = plot.read_csv(file_path)



# Streamlit app
st.title('Report Generator with Graphs')

# Sidebar for selection parameters
st.sidebar.header('Selection Parameters')
machine = st.sidebar.text_input('Machine ID', 'SM365POM240001')
company_name = st.sidebar.text_input('Company Name', 'Example Company')
channels = st.sidebar.multiselect('Select Channels', options=df_A.columns[2:].tolist(), default=df_A.columns[2:].tolist())
date_taken = st.sidebar.date_input('Select Date', pd.to_datetime('2024-06-15'))

report_details = {
    'Machine ID': machine,
    'Company Name': company_name,
    'Channels': channels,
    'start_date': pd.to_datetime(date_taken),
    'end_date': pd.to_datetime(date_taken) + pd.DateOffset(days=1)
}


#Getting the date
df_A_1date = df_A[(df_A['Datetime'] >= report_details[list(report_details.keys())[3]]) & (df_A['Datetime'] < report_details[list(report_details.keys())[4]])]
df_A_1date[channels] = df_A_1date[channels].apply(pd.to_numeric, errors='coerce')



# Generate and display plots
if st.sidebar.button('Generate Report'):
    st.subheader('Report Preview')
    fig = plot.create_plots(df_A_1date,channels,report_details)
    st.pyplot(fig)

    # # Save the figure to a PDF
    pdf_path = 'report.pdf'
    # with PdfPages('report.pdf') as pdf:
    #     pdf.savefig(fig)

    # st.success('Report generated and saved as report.pdf')
    st.download_button(label="Download Report", data=open(pdf_path, 'rb').read(), file_name="report.pdf")
