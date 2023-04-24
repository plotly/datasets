from dash import Dash, html, dcc       # pip install dash
import dash_mantine_components as dmc  # pip install dash-mantine-components
import pandas as pd                    # pip install pandas
import plotly.express as px

style = {
    "border": f"1px solid {dmc.theme.DEFAULT_COLORS['indigo'][4]}",
    "textAlign": "center",
}

df = pd.read_excel("https://github.com/plotly/datasets/blob/master/supermarket_sales.xlsx?raw=true", sheet_name='January')

# To see all months in one data set:
# list_of_dfs = [pd.read_excel("https://github.com/plotly/datasets/blob/master/supermarket_sales.xlsx?raw=true", sheet_name=x) for x in ['January', 'February', 'March']]
# df = pd.concat([x for x in list_of_dfs])
# df['Month'] = df['Date'].dt.month

fig1 = px.histogram(df, x='City', y='Total', color='Payment', histfunc='avg', barmode='group')#, facet_col='Month')
fig2 = px.box(df, x='City', y='Unit price', color='City')#, facet_col='Month')
fig3 = px.density_heatmap(df, x='Unit price', y='Rating')#, facet_col='Month')
fig4 = px.strip(df, x="gross income", y="Product line")#, color='Month')

app = Dash(__name__)
server = app.server

app.layout=dmc.Container([
    html.H1("Python App from Excel"),
    dmc.Grid([
        dmc.Col(dcc.Graph(figure=fig1, style=style), span=6),
        dmc.Col(dcc.Graph(figure=fig2, style=style), span=6),
        dmc.Col(dcc.Graph(figure=fig3, style=style), span=6),
        dmc.Col(dcc.Graph(figure=fig4, style=style), span=6),
    ], gutter="sm")

], fluid=True)


if __name__=='__main__':
    app.run_server(debug=True)
