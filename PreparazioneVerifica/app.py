from flask import Flask, render_template, request,  send_file, make_response, url_for, Response, redirect
app = Flask(__name__)
import pandas as pd, pymssql


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
        return redirect(url_for("input"))

@app.route('/numeroProdotti', methods=['GET'])
def numeroProdotti():
    global dfNumeroProdotti
    conn = pymssql.connect(server = '213.140.22.237\SQLEXPRESS', user='tag.alessandro', password='xxx123##', database='tag.alessandro')

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
    fig.autofmt_xdate(rotation=45) ##ruotare le scritte sull asse x del grafico

    # visualizzazione grafico:
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)