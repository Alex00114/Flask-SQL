from flask import Flask, render_template, request, send_file, make_response, url_for, Response, redirect
app = Flask(__name__)
import io
import geopandas
import contextily
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

@app.route('/selezione', methods=['GET'])
def selezione():
    scelta = request.args["Scelta"]
    if scelta == "Es1":
        return redirect(url_for("numeroProdotti"))
    elif scelta == "Es2":
        return redirect(url_for("numeroOrdini"))
    elif scelta == "Es3":
        return redirect(url_for("ProdottiBrand"))
    else:
        return render_template('input.html')

@app.route('/numeroProdotti', methods=['GET'])
def numeroProdotti():
    global dfNumeroProdotti
    
    query = 'select category_name, count(*) as prodotti_per_categoria from production.categories inner join production.products on production.categories.category_id = production.products.category_id group by category_name order by prodotti_per_categoria desc'
    dfNumeroProdotti = pd.read_sql(query, conn)
    return render_template('numeroProdotti.html', nomiColonne = dfNumeroProdotti.columns.values, dati = list(dfNumeroProdotti.values.tolist()))

@app.route('/grafico', methods=['GET'])
def grafico():
    # costruzione del grafico:
    fig, ax = plt.subplots(figsize = (12,6))

    ax.bar(dfNumeroProdotti["category_name"], dfNumeroProdotti["prodotti_per_categoria"], color = "c") 

    fig.suptitle("Grafico a Barre Verticali")
    ax.set_xlabel('Numero Prodotti',color = "black")
    ax.set_ylabel('Categorie',color = "black")

    plt.rcParams.update({"font.size": 12 })
    fig.autofmt_xdate(rotation=45)

    # visualizzazione grafico:
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/numeroOrdini', methods=['GET'])
def numeroOrdini():
    global dfNumeroOrdini

    query ='select store_name, count(*)as ordini_per_store from sales.orders inner join sales.stores on sales.orders.store_id = sales.stores.store_id group by store_name order by ordini_per_store desc'
    dfNumeroOrdini = pd.read_sql(query, conn)
    return render_template('numeroOrdini.html', nomiColonne = dfNumeroOrdini.columns.values, dati = list(dfNumeroOrdini.values.tolist()))

@app.route('/grafico2', methods=['GET'])
def grafico2():
    fig, ax = plt.subplots(figsize = (12,6))

    ax.barh(dfNumeroOrdini["store_name"], dfNumeroOrdini['ordini_per_store'], color = "c")

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/ProdottiBrand', methods=['GET'])
def ProdottiBrand():
    global dfProdottiBrand

    query ='select brand_name, count(*)as protti_per_brand from production.brands inner join production.products on production.products.brand_id = production.brands.brand_id group by brand_name order by protti_per_brand desc'
    dfProdottiBrand = pd.read_sql(query, conn)
    return render_template('prodottiBrand.html', nomiColonne = dfProdottiBrand.columns.values, dati = list(dfProdottiBrand.values.tolist()))

@app.route('/grafico3', methods=['GET'])
def grafico3():
    fig, ax = plt.subplots(figsize = (15,9))

    ax.pie(dfProdottiBrand['protti_per_brand'], labels = dfProdottiBrand['brand_name'])

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/result', methods=['GET'])
def result():
    NomeProdotto = request.args['NomeProdotto']
    query = f"select * from production.products where product_name LIKE '{NomeProdotto}%'"
    dfprodotti = pd.read_sql(query, conn)
    # visualizzare le informazioni 
    return render_template('result.html', nomiColonne = dfprodotti.columns.values, dati = list(dfprodotti.values.tolist()))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)