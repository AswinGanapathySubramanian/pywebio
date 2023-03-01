#importing the libraries 
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chains import ConversationChain
#import streamlit as st
# import uuid
# import secrets
import pywebio
from pywebio.input import input
from pywebio.output import put_text, put_html, put_markdown 
import os
#from pywebio.input import *
#from pywebio.output import *

# def chatbot(template,temp1,questions=""):
#     if temp1=="cust":
#     	prompt_template = PromptTemplate(input_variables=["chat_history"], template=template)
#     elif temp1 =="agt":
#         prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)
    
#     memory = ConversationBufferMemory(memory_key="chat_history")

#     llm_chain = LLMChain(
#         llm=OpenAI(openai_api_key="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",max_tokens=90),
#         prompt=prompt_template,
#         verbose=True,
#         memory=memory,
#     )

#     r=llm_chain.predict(question=questions)
#     return(r)


#@app.route("/")
def main():
    api_Key=os.getenv("api_Key")
    def chatbot(template,temp1,questions=""):
        if temp1=="cust":
            prompt_template = PromptTemplate(input_variables=["chat_history"], template=template)
        elif temp1 =="agt":
            prompt_template = PromptTemplate(input_variables=["chat_history","question"], template=template)
        
        memory = ConversationBufferMemory(memory_key="chat_history")

        llm_chain = LLMChain(
            llm=OpenAI(openai_api_key=api_Key,max_tokens=90),
            prompt=prompt_template,
            verbose=True,
            memory=memory,
        )

        r=llm_chain.predict(question=questions)
        return(r)




    ## Customer 
    template = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
    Scenario: Lets do a quick role play for a customer that is having billing issues.{chat_history}
    Customer:  

    """
    e1="""
    Agent: {question}
    AI:

    """

    #template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
    #Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
    #"""+ c1+e1

    template1 = """You are a agent in a call center. Given the response of the agent, it is your job to write a better response.
    Scenario: Lets do a quick role play for an angry customer that is having billing issues. {chat_history}
    """


    #cust1="Customer: "+c1
    #agent1="Agent: "+a1+"\n"+"Customer:"+"\n"

    template2 = """You are a customer having a call with contact center agent. You generate response for the customer based on the scenario. 
    Scenario: Lets do a quick role play for a customer that is having billing issues.{chat_history}
    """
    #template2=template2+cust1+"\n"+agent1
    flag=0
    count=0
    i=0
    l=[]
    t=[]

    while count>=0:
        if count ==0:
            t.append(template)
            c1= chatbot(template,"cust")
            c1= "Customer: "+c1
            flag=1
            if flag==1:
                #print(c1)
                l.append(c1)
                #st.write(l[i])
                put_text(l[i])
                i+=1
                count+=1
                template2=template2+c1
                flag=0
        if count%2!=0:
            if count==1: 
                template1=template1+"\n"+c1
                t.append(template1+e1+"\n")
                flag=1
                if flag==1:
                    #x=st.text_input("Your response",key=st.session_state.counter)
                    x=input("Your Response")
                    put_text("Your Response: "+x)
                    put_text("Better way of responding might be:")
                    #st.session_state.counter += 1
                    flag=0
                if x!="":
                    #st.session_state.counter += 1
                    a1=chatbot(template1+e1+"\n","agt",x)
                    a2= "Agent: "+a1
                    l.append(a2)
                    #st.write(l[i])
                    put_text(l[i])
                    i+=1
                    count+=1
                    template1=template1+"\n"+a2
                    
            else:
                template1=template1+c2
                t.append(template1+e1+"\n")
                flag=1
                if flag==1:
                    #x1=st.text_input("Your response",key=st.session_state.counter)
                    x1=input("Your Response")
                    put_text("Your Response: "+x1)
                    put_text("Better way of responding might be:")

                    flag=0
                i+=1
                if x1!="":
                    #st.session_state.counter += 1
                    a1=chatbot(template1+e1+"\n","agt",x1)
                    a2= "Agent: "+a1
                    l.append(a2)
                    put_text(l[i])
                    #st.write(l[i])
                    i+=1
                    count+=1
                    template1=template1+"\n"+a2
                
        if count%2==0:
            if count ==2:
                template2=template2+"\n"+a2
                t.append(template2)
                c2=chatbot(template2+"Customer: ","cust")
                if c2 !="":
                    c2="Customer: "+c2
                    
                    #st.write(c2)
                    l.append(c2)
                    put_text(l[i])
                    i+=1
                    template2=template2+"\n"+c2
                    count+=1
            else :
                template2=template2+"\n"+a2
                t.append(template2)
                c2=chatbot(template2+"Customer: ","cust")
                c2="Customer: "+c2
                #st.write(c2)
                
                l.append(c2)
                put_text(l[i])
                i+=1
                count+=1





if __name__ == "__main__":
    import argparse
    from pywebio.platform.tornado_http import start_server as start_http_server
    from pywebio import start_server as start_ws_server

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()

    if args.http:
        start_http_server(main, port=args.port)
    else:
        # Since some cloud server may close idle connections (such as heroku),
        # use `websocket_ping_interval` to  keep the connection alive
        start_ws_server(main, port=args.port, websocket_ping_interval=30)