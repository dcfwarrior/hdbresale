# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 21:47:17 2023

@author: qhkev
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 16:09:12 2023

@author: qhkev
"""
import streamlit as st

import pandas as pd
import plotly.express as px

#st.set_page_config(layout="wide")


@st.cache_data
def get_data():
    source_df = pd.read_csv("ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv")
    #source_df = pd.read_csv("https://s3.ap-southeast-1.amazonaws.com/table-downloads-ingest.data.gov.sg/d_8b84c4ee58e3cfc0ece0d773c8ca6abc.csv?AWSAccessKeyId=ASIAU7LWPY2WGCYBNDFC&Expires=1698570049&Signature=fQ5QUHCIk7pQ08Y8bJg1dAkD1Cw%3D&X-Amzn-Trace-Id=Root%3D1-653e1130-7da4d75f13af54e33e3a7c1c%3BParent%3D519f57647ce7cfee%3BSampled%3D1%3BLineage%3D80cb18ff%3A0&response-content-disposition=attachment%3B%20filename%3D%22ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv%22&x-amz-security-token=IQoJb3JpZ2luX2VjEJD%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLXNvdXRoZWFzdC0xIkcwRQIgMvQotaBah7nq1lOo6QOcytomW3%2BPweuuCc09uHL5N%2F0CIQCCKl%2FEb0P%2FnVxlkcDKzVW75ZY2PdjB8M%2BLT%2Bqih8zFaCqxAwi5%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAQaDDM0MjIzNTI2ODc4MCIMcuWkyxLtu35mMAQQKoUDbTGKGNMlRY%2Bn9p%2BefE7UiegHbng5EtWpeFieUJhtr9u4tB6v1BlkwVbDbw3lAuVA2ugKqkFHaveuyYfJ7Jw4ILreGWw9nQVL836jcVK6vWINJDCKXF0MKVuPyyqnFhPHzq%2Fe0GIKPJeaU0Eyzuuef9TDkhYG1hEOoKgQesxjjr5ym5I9ETZpZgiL7eOrg7DwDoL3rQW6o4HRRFvHjuWqmSa%2F7fsLD1zQGd9HqIjAz%2Bm6sx8IA1KAPKEq80PpWbhcVGzgCLguNbu8I1xqYm5JwrTMvOZnBr1ZdsYvCmkTbv5%2B1JoG5Yxp15C1rh0OAjC0I1J2capwmat7ixZ07s0fySH1pzjRwXJD0t8AheV2McEI%2BIs7M4SZ5OalTMG6i3c%2BBCpcJ6q51RaBiwRX8PvSxHxzYjV47yspRb2xRcZOZgaTJyQlt8eDL5Jsw0p31D9GwgCPdtcdlqtDWjXDdzlXWnG80jCQiFCWIGJmQSBxiW6sg6UwetY9ruBuWVw7gJeAm%2BGCW3EwiaL4qQY6nQFQwEAwQHeYLqBIj5U9u770vw48Jgpdzh9aJHOEGBurxgUvYJlA7RRNz0LzN8T8b0lkotwJHjFxYB3BTwGK%2BfiHyUdaiB%2B3YGMAodZvcRLVR8UpytSukGY0%2FiB0OMw7YsYxITRPtYXmPuSUzmxwPJnG%2Bp18kepshX5DcmM1lAg5%2FH5FabcucVAqS1RtAaUEiuxO861dpKGRNO%2Fb%2F43V")
    source_df["date"] = pd.to_datetime(source_df["month"], infer_datetime_format = True )
    source_df["year"] = source_df['date'].dt.year
    source_df["month"] = source_df['date'].dt.month
    
    c1 = source_df.pop("year")
    source_df.insert(0,c1.name, c1)
    c1 = source_df.pop("date")
    source_df.insert(0,c1.name, c1)
    
    return source_df


st.title("HDB Resale Price Analysis")

source_df = get_data()

filter_source_df = source_df.copy()

#filter data##

col_1 = st.columns((1,1))

with col_1[0]:
    year = st.multiselect('Please select the years',
                          options = filter_source_df['year'].unique(),
                          default= list(filter_source_df['year'].unique())
                                        )
    
    filter_source_df = filter_source_df[source_df['year'].isin(year)]

with col_1[1]:
    month = st.multiselect('Please select the months',
                      options = filter_source_df['month'].unique(),
                      default= list(filter_source_df['month'].unique())
                                    )

    filter_source_df = filter_source_df[filter_source_df['month'].isin(month)]

town = st.multiselect('Please select the towns',
                  options = filter_source_df['town'].unique(),
                  default= list(filter_source_df['town'].unique())
                                )

filter_source_df = filter_source_df[filter_source_df['town'].isin(town)]

street_name = st.multiselect('Please select the street name',
                  options = filter_source_df['street_name'].unique(),
                  default= list(filter_source_df['street_name'].unique())
                                )

filter_source_df = filter_source_df[filter_source_df['street_name'].isin(street_name)]

col_2 = st.columns((1,1))

with col_2[0]:
    flat_type = st.multiselect('Please select the flat type',
                      options = filter_source_df['flat_type'].unique(),
                      default= list(filter_source_df['flat_type'].unique())
                                    )
    
    filter_source_df = filter_source_df[filter_source_df['flat_type'].isin(flat_type)]

with col_2[1]:
    storey = st.multiselect('Please select the storey',
                      options = filter_source_df['storey_range'].unique(),
                      default= list(filter_source_df['storey_range'].unique())
                                    )
    
    filter_source_df = filter_source_df[filter_source_df['storey_range'].isin(storey)]


block_filter = st.text_input('Input the block you wish to filter')

filter_source_df = filter_source_df[filter_source_df['block'].str.contains(block_filter)]




## Chart 1

agg_mean_source_df = filter_source_df.groupby(by=['date','town'], as_index = False).mean()
agg_count_source_df = filter_source_df.groupby(by=['date','town'], as_index = False).count()



fig1 = px.line(agg_mean_source_df, x="date", y="resale_price", color='town')
fig2 = px.bar(agg_count_source_df, x="date", y="resale_price", color='town')

col1 = st.columns((1))
col1[0] = st.plotly_chart(fig1, use_container_width=True)

col2 = st.columns((1))
col2[0] = st.plotly_chart(fig2, use_container_width=True)


## Chart 2

agg_mean_street_source_df = filter_source_df.groupby(by=['date','town', 'street_name'], as_index = False).mean()
fig3 = px.line(agg_mean_street_source_df, x="date", y="resale_price", color='street_name')


col3 = st.columns((1))
col3[0] = st.plotly_chart(fig3, use_container_width=True)



st.dataframe(filter_source_df)
st.dataframe(agg_mean_source_df)
st.dataframe(agg_count_source_df)
