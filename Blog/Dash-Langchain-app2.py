from dash import Dash, dcc, html, callback, Input, Output, State, no_update
from operator import itemgetter

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.vectorstores import FAISS

api_key = "my-api-key"  # https://platform.openai.com/account/api-keys
app = Dash()

app.layout = html.Div([
    html.H1("Summarize Earnings Reports"),
    html.Label("Select earnings report:"),
    dcc.Dropdown(value='tesla-earning-report.txt',
                 id='reports',
                 clearable=False,
                 style={'width':'120px'},
                 options=[
                     {'label':'Tesla', 'value':'tesla-earning-report.txt'},
                     {'label':'Microsoft', 'value':'microsoft-earning-report.txt'}]
                 ),
    dcc.Input(id='question',
              type='text',
              placeholder='type your question...',
              debounce=True,
              style={'width':'500px', 'height':'30px', 'margin-top':20},
              maxLength=100),
    dcc.Loading(id="loading", children=html.Div(id='answer', children=None, style={'margin-bottom':20})),
    html.Hr(),
    html.Div(id='report-content', children=[])
])


@callback(
    Output('answer', 'children'),
    Output('report-content', 'children'),
    Input('question','value'),
    State('reports', 'value'),
    prevent_initial_call=True
)
def update_layout(question_asked, file):
    if question_asked:
        with open(file, encoding="utf8") as f:
            lines = f.readlines()

        vectorstore = FAISS.from_texts(lines, embedding=OpenAIEmbeddings(openai_api_key=api_key))
        retriever = vectorstore.as_retriever()

        template = """Answer the question based only on the following context:
        {context}
    
        Question: {question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        model = ChatOpenAI(openai_api_key=api_key)

        chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | model
                | StrOutputParser()
        )
        display_answer = chain.invoke(question_asked)

        view_selected_report = [
            html.H3("Complete earnings report chosen:"),
            dcc.Markdown(children=lines)

        ]

        return display_answer, view_selected_report

    else:
        return no_update


if __name__ == "__main__":
    app.run_server(debug=True)
