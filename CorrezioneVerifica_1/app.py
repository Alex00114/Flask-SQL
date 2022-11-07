from flask import Flask, render_template, request, send_file, make_response, url_for, Response, redirect
app = Flask(__name__)
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import pymssql
conn = pymssql.connect(server = '213.140.22.237\SQLEXPRESS', user='tag.alessandro', password='xxx123##', database='tag.alessandro')


@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@app.route('/ricerca', methods=['GET'])
def ricerca():
    store = request.args["Scelta"]
    query = f"select sales.staffs.first_name, sales.staffs.last_name, sales.stores.store_name from sales.staffs inner join sales.stores on sales.staffs.store_id = sales.stores.store_id where sales.stores.store_name = '{store}'"
    dfDipendenti = pd.read_sql(query, conn)
    if dfDipendenti.values.tolist() == []:
        return render_template("error.html")
    else:
        return render_template("dipendenti.html", nomiColonne = dfDipendenti.columns.values, dati = list(dfDipendenti.values.tolist()))










if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)