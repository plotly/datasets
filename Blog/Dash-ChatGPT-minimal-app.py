import os
import openai  # pip install openai
from dash import Dash,dcc, html, Input, Output, State  # pip install dash

# Set up OpenAI API credentials
# Create .env file and insert your api key like so:
# OPENAI_API_KEY="your-key-goes-here"
openai.api_key = os.getenv("OPENAI_API_KEY")   # pip install python-dotenv

# Initialize the ChatGPT model
model_engine = 'text-davinci-003'

# Instantiate the Dash app
app = Dash(__name__)

app.layout = html.Div([
   html.H1("Dash-ChatGPT Example"),
   dcc.Input(id='input-text', type='text', placeholder='Type your message here', style={'width':500}),
   html.Button('Send', id='submit-button', n_clicks=0),
   dcc.Loading(
       children=[
           html.Div(id='output-text')
       ],
       type="circle",
   )
])

# Define the callback function
@app.callback(
  Output('output-text', 'children'),
  Input('submit-button', 'n_clicks'),
  State('input-text', 'value')
)
def update_output(n_clicks, input_text):
  if n_clicks >0:
      # Get the response from ChatGPT
      response = openai.Completion.create(
          engine=model_engine,
          prompt=f"{input_text}\n",
          max_tokens=4000,
          n=1,
          stop=None,
          temperature=0.7,
      )

      # Extract the generated text from the response
      generated_text = response.choices[0].text

      # Return the generated text as the output
      return generated_text

if __name__ == '__main__':
  app.run_server(debug=True)
