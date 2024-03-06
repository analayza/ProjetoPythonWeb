from flask import *
import dao
import dataanalise as da
import plotly.express as px

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def cadastrar_usuario():
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))

    if dao.verificarlogin(nome, senha):
        return render_template('menu.html')
    else:
        return render_template('index2.html')

@app.route('/grafvioleciapib', methods=["POST", "GET"])
def gerarGrafViolenciaPib():
    if request.method == 'POST':
        filtro = int(request.form.get('valor'))
    else:
        filtro = 10

    dados = da.lerdados()
    dados.drop(dados.sort_values(by=['cvli'], ascending=False).head(3).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=False).head(filtro).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=True).head(2).index, inplace=True)

    fig = px.scatter(dados, x='rendapercapita', y='cvli', hover_data=['municipio'])
    return render_template('grafviolenciapib.html', plot=fig.to_html())

@app.route('/grafcorrelacao')
def gerarGrafCorrelacao():
    dados = da.lerdados()
    fig2 = da.exibirmapacorrelacoes(dados)

    return render_template('grafcorrelacao.html', mapa=fig2.to_html())

@app.route('/melhoresedu')
def exibirmelhores():
    data = da.lerdados()

    data['somaedu'] = data['idebanosiniciais'] + data["idebanosfinais"]
    print(data.sort_values(by=["somaedu"], ascending=False, inplace=True))
    fig = da.exibirgraficobarraseduc(data.head(15))
    return render_template("melhoresedu.html", figura=fig.to_html())


#FIM NOVAS FUNCIONALIDADES
@app.route('/emprego')
def exibirgraficoemprego():
    data = da.lerdados()
    fig3 = da.exibirgraficoemprego(data.head(10))
    return render_template('emprego.html', pizza=fig3.to_html())

@app.route('/idh', methods=['POST', 'GET'])
def exibirgraficoidh():
    if request.method == 'POST':
        cidade = int(request.form.get('qtdcidade'))
    else:
        cidade = 10

    dados = da.lerdados()
    dados_top = dados.nlargest(cidade, 'idh')
    fig4 = da.exibirgraficoidebidh(dados_top)
    return render_template('idh.html', cidades=fig4.to_html())


@app.route('/tabela', methods=['POST', 'GET'])
def gerartabela():
    if request.method == 'POST':
        coluna = str(request.form.get('coluna'))
    else:
        coluna = 'pib'

    fig5 = da.gerartabela(coluna)
    return render_template('tabela.html', colunas=fig5.to_html())

#FIM DAS NOVAS FUNCIONALIDADES


@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/')
def motormanda():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)