import psycopg2
def verificarlogin(nome, senha, conexao):
    cur = conexao.cursor()
    cur.execute(f"SELECT count(*) FROM usuario WHERE login = '{nome}' AND senha = '{senha}'")
    recset = cur.fetchall()
    conexao.close()
    if recset[0][0] == 1:
        return True
    else:
        return False



def conectardb():
    con = psycopg2.connect(
        host='localhost',
        database='aplicacao',
        user='postgres',
        password='1234'
    )

    return con


def inserirusuer(login, senha, conexao):
    cur = conexao.cursor()
    exito = False
    try:
        sql = f"INSERT INTO usuario (login, senha) VALUES ('{login}', '{senha}' )"
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito



def listarUsuarios(conexao):
    cur = conexao.cursor()
    cur.execute('select * from usuario')
    recset = cur.fetchall()
    conexao.close()

    return recset