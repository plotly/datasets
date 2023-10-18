from dash import Dash, dcc, html, callback, Input, Output
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}")
api_key = "my-api-key-goes-here"
model = ChatOpenAI(openai_api_key=api_key)
chain = prompt | model

app = Dash()

app.layout = html.Div([
   html.H1("Joke-Generating App"),
   html.Label("Tell me a joke about: "),
   dcc.Input(id='subject', debounce=True, maxLength=15),
   html.Hr(),
   html.Div(id='joke-placeholder')
])

@callback(
   Output('joke-placeholder', 'children'),
   Input('subject', 'value'),
   prevent_initial_call=True
)
def update_layout(input_value):
   joke = chain.invoke({"foo": input_value})
   output = joke.content
   return output


if __name__ == "__main__":
   app.run_server(debug=True)
