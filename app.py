import numpy as np
import streamlit as st
import pandas as pd
from payment import calculate_payment_per_unit
import seaborn as sns
import matplotlib.pyplot as plt

def app():
    st.title('Data Visualization')

    # Allow user to set the factors
    base_price = st.sidebar.slider("Base Price", 1.0, 20.0, 10.0)
    active_user_factor = st.sidebar.slider("Active User Factor", 0.0, 2.0, 1.0)
    task_age_factor = st.sidebar.slider("Task Age Factor", 0.0, 2.0, 1.0)
    total_task_factor = st.sidebar.slider("Total Task Factor", 0.0, 2.0, 0.5)
    ether_price_factor = st.sidebar.slider("Ether Price Factor", 0.0, 2.0, 0.5)

    # Read CSV Data
    df = pd.read_csv('random_data.csv')
    df['date'] = pd.to_datetime(df['date'])

    # Calculate the payments for the tasks solved and add it to the dataframe
    df['Payment Per Task'] = df.apply(lambda row: calculate_payment_per_unit(row, 
                                      base_price=base_price, 
                                      active_user_factor=active_user_factor,
                                      task_age_factor=task_age_factor, 
                                      total_task_factor=total_task_factor, 
                                      ether_price_factor=ether_price_factor), 
                             axis=1)
    df['Payment Per Task'] = df['Payment Per Task'].fillna(0)  # fill NaN values with 0 (where no tasks were solved)

    st.subheader('Payment Per Task Over Time')
    st.line_chart(df.set_index('date')['Payment Per Task'])

    # Display data as table
    st.dataframe(df)

    st.subheader('Total Tasks Over Time')
    st.line_chart(df.set_index('date')['Total Tasks'])
    
    st.subheader('Ether to USD Over Time')
    st.line_chart(df.set_index('date')['Ether to USD'])

    st.subheader('Users Over Time')
    st.line_chart(df.set_index('date')['Users'])

    # Correlation matrix
    st.subheader('Correlation Matrix')
    corr = df[['Active Users', 'Total Tasks', 'New Tasks', 'Ether to USD', 'Payment Per Task']].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with the mask and correct aspect ratio
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)
    
    st.pyplot(f)

if __name__ == '__main__':
    app()

