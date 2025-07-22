import streamlit as st
import pandas as pd
import plotly.express as  px


# App config
st.set_page_config(page_title="Simple Data Analytics App", page_icon="📊")

# title
st.title(':rainbow[Silver Line Analytics Portal]')
st.header('Explore Data with ease.',divider='rainbow')

file = st.file_uploader('Drop csv or excel file',type=['csv','xlsx'])
if(file!=None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.dataframe(data)
    st.info('File is successfully uploaded',icon='🆗')

    st.subheader(':rainbow[Basic information of the dataset]',divider ='rainbow')
    tab1,tab2,tab3,tab4 = st.tabs(['Summary','Top and Bottom','Data Types','Columns'])

    with tab1:
          st.write(f'There are{data.shape[0]} rows in dataset and {data.shape[1]} columns in the dataset')
          st.subheader(':grey[Statistical summary of the dataset]')
          st.dataframe(data.describe())
    with tab2:
        st.subheader(':grey[Top Rows]')
        st.dataframe(data.head())
        st.subheader(':grey[Bottom Rows]')
        st.dataframe(data.tail())

    with tab3:
        st.subheader(':grey[Data types of columns]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(':grey[Column Name]')
        st.dataframe(data.columns)

# --- Missing Values Section ---
    st.subheader(':rainbow[Missing Value Handler]', divider='rainbow')

    with st.expander('Handle Missing Values'):
        st.write('Below are the total missing values per column.')
        missing_data = data.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)

        if missing_data.empty:
            st.success("🎉 No missing values found in the dataset.")
        else:
            st.dataframe(missing_data)

            action = st.radio("Choose an action:", ['Drop rows with missing values', 'Fill missing values'])
            if action == 'Fill missing values':
                fill_method = st.selectbox('Choose fill method',
                                           ['Mean', 'Median', 'Mode', 'Forward Fill', 'Backward Fill', 'Custom Value'])
                if fill_method == 'Custom Value':
                    custom_val = st.text_input("Enter custom value to fill missing data")

                apply_fill = st.button('Apply Filling')

                if apply_fill:
                    for col in data.columns:
                        if data[col].isnull().any():
                            if fill_method == 'Mean' and pd.api.types.is_numeric_dtype(data[col]):
                                data[col].fillna(data[col].mean(), inplace=True)
                            elif fill_method == 'Median' and pd.api.types.is_numeric_dtype(data[col]):
                                data[col].fillna(data[col].median(), inplace=True)
                            elif fill_method == 'Mode':
                                data[col].fillna(data[col].mode()[0], inplace=True)
                            elif fill_method == 'Forward Fill':
                                data[col].fillna(method='ffill', inplace=True)
                            elif fill_method == 'Backward Fill':
                                data[col].fillna(method='bfill', inplace=True)
                            elif fill_method == 'Custom Value':
                                data[col].fillna(custom_val, inplace=True)

                    st.success('Missing values filled successfully.')

            elif action == 'Drop rows with missing values':
                data.dropna(inplace=True)
                st.success("Rows with missing values dropped successfully.")

    st.subheader(':rainbow[Column values To Count]',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose Column name',options=list(data.columns))
        with col2:
            top_rows = st.number_input('Top rows', min_value=1,step=1)

        count = st.button('Count')

        if count:
            result = data[column].value_counts().reset_index().head(top_rows)
            result.columns = [column, 'Count']  # Optional: Rename columns
            st.dataframe(result)
            st.subheader('Visualization',divider = 'gray')
            fig = px.bar(data_frame=result,x=column,y='Count',text='Count')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='Count',text='Count')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=column,values='Count')
            st.plotly_chart(fig)

    st.subheader(':rainbow[Groupby : Simlify your data analysis]',divider='rainbow')
    st.write('The groupby lets you summarize data by specific categories and groups')
    with st.expander('Group By your columns'):
        col1,col2,col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose your column to groupby',options=list(data.columns))
        with col2:
            operation_col = st.selectbox('Choose column for operation',options=list(data.columns))
        with col3:
            operation = st.selectbox('Choose operation',options=['sum','max','min','mean','count'])

    if groupby_cols:
        result = data.groupby(groupby_cols).agg(
            newcol=(operation_col, operation)
        ).reset_index()

        st.dataframe(result)
        st.subheader(':rainbow[Data Visualization]', divider = 'rainbow')
        graphs = st.selectbox('Choose your graphs', options=['line','bar','scatter','pie','sunburst'])

        if(graphs=='line'):
            x_axis = st.selectbox('Choose X axis', options=list(result.columns))
            y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
            color = st.selectbox('Color Information',options=[None] +list(result.columns))
            fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
            st.plotly_chart(fig)

        elif(graphs=='bar'):
            x_axis = st.selectbox('Choose X axis', options=list(result.columns))
            y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
            color = st.selectbox('Color Information', options=[None] + list(result.columns))
            facet_col = st.selectbox('Column Information',options=[None] + list(result.columns))
            fig = px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
            st.plotly_chart(fig)

        elif(graphs=='scatter'):
            x_axis = st.selectbox('Choose X axis', options=list(result.columns))
            y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
            color = st.selectbox('Color Information', options=[None] + list(result.columns))
            size = st.selectbox('Size Column',options=[None] + list(result.columns))
            fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)
            st.plotly_chart(fig)

        elif(graphs=='pie'):
            values = st.selectbox('Choose Numerical Values',options=list(result.columns))
            names =  st.selectbox('Choose labels',options=list(result.columns))
            fig = px.pie(data_frame=result,values=values,names=names)
            st.plotly_chart(fig)

        elif graphs == 'sunburst':
            path = st.multiselect('Choose your path', options=list(result.columns))

            if path:  # Only proceed if user selected at least one column
                fig = px.sunburst(data_frame=result, path=path, values='newcol')
                st.plotly_chart(fig)
            else:
                st.warning("Please select at least one column for the path.")
   
