# Import python packages
import streamlit as st
from snowflake.connector import connect
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.session import SnowparkClientExceptionMessages

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(""" Choose the fruits you want in your custom Smoothie! """)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake 연결 설정
snowflake_username = 'jhum'
snowflake_password = '!Q2w3e4r'
snowflake_account = 'XZGJBJC-QC25280'
snowflake_database = 'SMOOTHIES'
snowflake_schema = 'PUBLIC'

# Snowflake에 연결하여 세션을 만듭니다.
def create_snowflake_session():
    try:
        conn = connect(
            user=snowflake_username,
            password=snowflake_password,
            account=snowflake_account,
            database=snowflake_database,
            schema=snowflake_schema
        )
        return conn.cursor()
    except Exception as e:
        st.error(f"Error creating Snowflake session: {str(e)}")

# Snowflake 세션을 가져옵니다.
def get_snowflake_session():
    try:
        session = create_snowflake_session()
        return session
    except Exception as e:
        st.error(f"Error getting Snowflake session: {str(e)}")

session = get_snowflake_session()
if session:
    my_dataframe = session.execute("SELECT FRUIT_NAME FROM fruit_options")
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:'
        , [row[0] for row in my_dataframe.fetchall()]  # fetchall()을 사용하여 데이터를 가져옵니다.
        , max_selections=5
        )

    if ingredients_list:
        st.write(ingredients_list)
        st.text(ingredients_list)
        
        ingredients_string = ', '.join(ingredients_list)

        my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients)
                            VALUES ('{ingredients_string}')"""

        time_to_insert = st.button('Submit Order')
        
        if time_to_insert:
            session.execute(my_insert_stmt)
            st.success('Your Smoothie is ordered!', icon="✅")
else:
    st.error("Snowflake session is not available.")
