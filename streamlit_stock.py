import streamlit as st


pages = [ 
    st.Page("main.py", title="Home" , icon=":material/home:"),
    st.Page("stock_query.py", title="股價查詢"),
    st.Page("company_fund.py", title="公司基本面"),
    st.Page("share_holders.py", title="股東持股"),
    st.Page("https://github.com/mymis168", title="GitHub專案"),
]

pgnav = st.navigation(pages=pages, position="top")
pgnav.run()
