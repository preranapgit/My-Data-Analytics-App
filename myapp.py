import pandas as pd
#import plotly.express as  px
import streamlit as st

st.set_page_config(
    page_title="my analytics app",
    page_icon='📊'
    
)
st.title(':rainbow[DATA ANALYTICS PORTAL]')
st.subheader(':grey[Explore data with ease.]',divider='rainbow')
file=st.file_uploader('Drop csv or excel file',type=['csv','xlsx'])
if(file!=None):
    if(file.name.endswith('excel')):
        data = pd.read_excel(file)
    else:
        data = pd.read_csv(file)    
    st.dataframe(data)
    st.info("file is successfully uploaded", icon="🔥")
    st.subheader(':rainbow[Basic information of the Dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4=st.tabs(['summary','Top and bottom rows','Data types','Columns'])
    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in the dataset')
        st.subheader(':gray[Statastical summary of the dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows=st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(':gray[Bottom Rows]')
        bottomrows=st.slider('Number of rows you want',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':grey[Data types of column]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(':grey[Column names in dataset]')
        st.write(list(data.columns))

    st.subheader(':rainbow[Column Values To Count]',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2 = st.columns(2)
        with col1:
            column  = st.selectbox('Choose Column Name',options=list(data.columns))
        with col2:
            toprows = st.number_input('Top_rows',min_value=1,step=1)

        count = st.button('count')
        if(count== True):
            result=data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='grey')
            fig = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='count',text='count')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)
    st.subheader(':rainbow[Groupby : Simplify Your Data Analysis]',divider='rainbow')
    st.write('The groupby lets you summerize data by categories and groups')
    with st.expander('Group By your columns'):
        col1,col2,col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose your columns to groupby',options= list(data.columns))
        with col2:
            operation_cols= st.selectbox('Choose column for operation',options=list(data.columns))
        with col3:
            operation = st.selectbox('Choose operation',options=['sum','max','min','mean','median','count'])
        
        if(groupby_cols):
            result= data.groupby(groupby_cols).agg(
                newcol = (operation_cols,operation)
            ).reset_index()
            st.dataframe(result)
            st.subheader(':gray[Data Visualization]',divider='gray')
            graphs=st.selectbox('Choose your graphs',options=['line','bar','scatter','pie','sunbrust'])
            if(graphs=='line'):
                x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                color = st.selectbox('Color Information',options=[None] +list(result.columns))
                fig=px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)
            elif(graphs=='bar'):
                x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                color = st.selectbox('Color Information',options=[None] +list(result.columns))
                facet_col=st.selectbox('Column Information',options=[None]+list(result.columns))
                fig=px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)
            elif(graphs=='scatter'):
                x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                color = st.selectbox('Color Information',options=[None] +list(result.columns))
                size = st.selectbox('Size Column',options=[None]+list(result.columns))
                fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)
                st.plotly_chart(fig)
            elif(graphs=='pie'):
                values = st.selectbox('Choose numerical values',options=list(result.columns))
                names=st.selectbox('Choose labels',options=list(result.columns))
                fig=px.pie(data_frame=result,values=values,names=names)
                st.plotly_chart(fig)
            elif(graphs=='sunbrust'):
                path=st.multiselect('Choose your path',options=list(result.columns))
                fig=px.sunburst(data_frame=result,path=path,values='newcol')
                st.plotly_chart(fig)
                                    





        







