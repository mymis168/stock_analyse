import streamlit as st


pages = [ 
    st.Page("main.py", title="Home" , icon=":material/home:"),
    st.Page("stock_query.py", title="股價查詢")
]

pgnav = st.navigation(pages=pages, position="top")
pgnav.run()
