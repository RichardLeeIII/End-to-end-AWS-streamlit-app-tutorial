import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



df = pd.read_csv("quarterly_canada_population.csv", dtype={'Quarter': str, 
                            'Canada': np.int32,
                            'Newfoundland and Labrador': np.int32,
                            'Prince Edward Island': np.int32,
                            'Nova Scotia': np.int32,
                            'New Brunswick': np.int32,
                            'Quebec': np.int32,
                            'Ontario': np.int32,
                            'Manitoba': np.int32,
                            'Saskatchewan': np.int32,
                            'Alberta': np.int32,
                            'British Columbia': np.int32,
                            'Yukon': np.int32,
                            'Northwest Territories': np.int32,
                            'Nunavut': np.int32})
st.title("Population of Canada")
st.markdown("source table is from [here](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)")

years = df['Quarter'].str.split().str[1].astype(int)
min_year=years.min()
max_year=years.max()

with st.expander("see full data here"):
    st.write(df)

with st.form("population-form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("select the starting date")
        start_quarter= st.selectbox('Quarter', options=["Q1","Q2","Q3","Q4"],index=2, key="start_q")
        start_year=st.slider('Year', min_value=min_year,max_value=max_year,value=min_year,step=1,key="start_y")

    with col2:
        st.write("select the endind date")
        ending_quarter= st.selectbox('Quarter', options=["Q1","Q2","Q3","Q4"],index=0, key="ending_q")
        ending_year=st.slider('Year', min_value=min_year,max_value=max_year,value=max_year,step=1,key="ending_y")

    with col3:
        st.write("select the region")
        target=st.selectbox("choose location",options=df.columns[1:], index=0)

    submit_button=st.form_submit_button("Analyze", type="primary")

start_date = f"{start_quarter} {start_year}"
end_date = f"{ending_quarter} {ending_year}"

def format_date_for_comparison(date):
    if date[1] == 2:
        return float(date[2:])+0.25
    elif date[1] == 3:
        return float(date[2:])+0.5
    elif date[1] == 4:
        return float(date[2:])+0.75
    else:
        return float(date[2:])
    

def end_before_start(start_date, end_date):
    num_start_date = format_date_for_comparison(start_date)
    num_end_date = format_date_for_comparison(end_date)

    if num_start_date > num_end_date:
        return True
    else:
        return False

def display_population(start_date,end_date, target):
    tab1, tab2 = st.tabs(["Population change","Compare"])

    with tab1:
        st.subheader(f"Population change from {start_date} to {end_date}")

        col1, col2 = st.columns(2)

        with col1:
            initial = df.loc[df['Quarter']==start_date, target].item()
            final = df.loc[df['Quarter']==end_date, target].item()

            percentage_diff= round((final-initial)/initial * 100, 2)
            delta = f"{percentage_diff}%"
            st.metric(start_date, value=f"{initial:,}")
            st.metric(end_date,value=f"{final:,}", delta=delta)

        with col2:
            start_idx = df.loc[df["Quarter"] == start_date].index.item()
            end_idx = df.loc[df["Quarter"] == end_date].index.item()
            filtered_df = df.iloc[start_idx:end_idx+1]

            fig, ax = plt.subplots()
            ax.plot(filtered_df['Quarter'], filtered_df[target])
            ax.set_xlabel('Time')
            ax.set_ylabel('Population')
            ax.set_xticks([filtered_df["Quarter"].iloc[0],filtered_df["Quarter"].iloc[-1]])
            fig.autofmt_xdate()
            st.pyplot(fig)
    
    with tab2:
        st.subheader("select regions to compare")
        all_targets= st.multiselect("Choose other locations", options=filtered_df.columns[1:], default=target)

        fig, ax = plt.subplots()
        for each in all_targets:
                ax.plot(filtered_df['Quarter'], filtered_df[each])
        ax.set_xlabel('Time')
        ax.set_ylabel('Population')
        ax.set_xticks([filtered_df["Quarter"].iloc[0],filtered_df["Quarter"].iloc[-1]])
        fig.autofmt_xdate()
        st.pyplot(fig)

if start_date not in df["Quarter"].tolist() or end_date not in df["Quarter"].tolist():
    st.error("No data available. check your quarter and year selection")
elif end_before_start(start_date,end_date):
    st.error("Dates do not work. Start date must come before end date.")
else:
    display_population(start_date,end_date,target)