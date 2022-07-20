import streamlit as st
import firebase_admin
from firebase_admin import db
import pandas as pd
import datetime
@st.cache
def runonce():
    cred=firebase_admin.credentials.Certificate("key.json")
    firebase_admin.initialize_app(cred,{'databaseURL':'https://database-ef85e-default-rtdb.firebaseio.com/'}) 

runonce()
choice=st.sidebar.selectbox("My MENU",("HOME","STUDENT LOGIN","ADMIN LOGIN","READ BOOK ONLINE"))
st.title("LIBRARY MANAGEMENT SYSTEM")
if(choice=="HOME"):
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5iwSinVu1pygDZmERAkDdqYwzGGU2zqZtZ6g6YbczL8T2KsFA2r3fp04E5ENU236hkKs&usqp=CAU",width=500)
    st.header("WELCOME")
    st.text("This Application is developed by Abhinav Srivastava as a part of Course Project ")
elif(choice=="STUDENT LOGIN"):
    if 'login' not in st.session_state:
        st.session_state['login']=False
        st.session_state['id']=0
    data=db.reference("/Student").get()
    st.session_state['id']=st.text_input("Enter ID")
    password=st.text_input("Enter Password")
    btn=st.button("Login")
    if(btn==True):
        for i,p in data.items():
            if(i==st.session_state['id'] and p==password):
                st.session_state['login']=True
    if(st.session_state['login']==True):
        st.subheader("Login Successful")
        c=st.selectbox("What do you want ?",("NONE","SEARCH BOOK","ISSUE BOOK"))
        if(c=="SEARCH BOOK"):
            ref2=db.reference("/Book/").get()
            df=pd.DataFrame.from_dict(ref2,orient="index")
            st.dataframe(data=df)
        elif(c=="ISSUE BOOK"):
            row=st.text_input("Enter any 10 digit random number")
            bookid=st.text_input("Enter Book ID")
            date=st.date_input("Enter the date of issue")
            btn=st.button("ISSUE BOOK")
            if btn:
                ref=db.reference("/Issue/"+row)
                ref.update({"StudentID":st.session_state['id'],"BookID":bookid,"Date of Issue":str(date)})
                st.subheader("Book Issued Successfully")
            
elif(choice=="ADMIN LOGIN"):
    if 'adminlogin' not in st.session_state:
        st.session_state['adminlogin']=False        
    data=db.reference("/Admin").get()
    id=st.text_input("Enter Librarian ID")
    password=st.text_input("Enter Password")
    btn=st.button("Login")
    if(btn==True):
        for i,p in data.items():
            if(i==id and p==password):
                st.session_state['adminlogin']=True
    if(st.session_state['adminlogin']==True):
        st.subheader("Login Successful")
        c=st.selectbox("What do you want to do?",("NONE","ADD NEW BOOK","CHECK ISSUED BOOK"))
        if(c=="ADD NEW BOOK"):
            row=st.text_input("Enter any 10 digit random number")
            bookid=st.text_input("Enter Book ID")
            bookname=st.text_input("Enter Book Name")
            author=st.text_input("Enter Author Name")
            btn=st.button("ADD NEW BOOK")
            if btn:
                ref=db.reference("/Book/"+row)
                ref.update({"BookID":bookid,"Author":author,"BookName":bookname})
                st.subheader("Book Added Successfully") 
        elif(c=="CHECK ISSUED BOOK"):
            ref2=db.reference("/Issue/").get()
            df=pd.DataFrame.from_dict(ref2,orient="index")
            st.dataframe(data=df)
elif(choice=="READ BOOK ONLINE"):
    c=st.selectbox("Choose Book",("NONE","SHERLOCK HOLMES","PYTHON"))
    if(c=="SHERLOCK HOLMES"):
        st.markdown('<iframe src="https://sherlock-holm.es/stories/pdf/a4/1-sided/advs.pdf" width="100%" height="500" title="sherlock"></iframe>',unsafe_allow_html=True)
    elif(c=="PYTHON"):
        st.markdown('<iframe src="http://www.halvorsen.blog/documents/programming/python/resources/Python%20Programming.pdf" width="100%" height="500" title="sherlock"></iframe>',unsafe_allow_html=True)
