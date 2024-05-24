import oracledb
import hashlib
# https://docs.python.org/3/library/hashlib.html
from datetime import datetime


# Função para obter a conexão com o banco de dados
def obter_conexao():


    dsn = oracledb.makedsn("oracle.fiap.com.br", 1521, service_name="ORCL")

    conn = oracledb.connect(user="rm553873", password="110804", dsn=dsn)

    return conn

# Função para hash da senha
def hash_senha(senha):

    # Com uso da hashlib foi possivel converter a senha para bytes com .encode e retornar o demical com .hexdigest()
    #https://docs.python.org/3/library/hashlib.html#hashlib.sha256
    return hashlib.sha256(senha.encode()).hexdigest()


# Função para inserir um usuário no banco de dados
def inserir_usuario(dados_usuario):
    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO usuarios (login, tipo_login, email, nome, rg, cpf, data_nascimento, hash_senha, endereco, role)
        VALUES (:login, :tipo_login, :email, :nome, :rg, :cpf, TO_DATE(:data_nascimento, 'YYYY-MM-DD'), :hash_senha, :endereco, :role)
    ''', dados_usuario)

    cursor.execute('''
        INSERT INTO login_senha (usuario_id, login, hash_senha)
        VALUES ((SELECT usuario_id FROM usuarios WHERE login = :login), :login, :hash_senha)
    ''', {'login': dados_usuario['login'], 'hash_senha': dados_usuario['hash_senha']})

    conn.commit()
    cursor.close()
    conn.close()


# Função para obter um usuário pelo login
def obter_usuario_por_login(login):
    conn = obter_conexao()
    cursor = conn.cursor()

    # Seleciona o usuário pelo login
    cursor.execute('SELECT * FROM usuarios WHERE login = :login', {'login': login})
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    return usuario


# Função para obter usuários pelo prefixo do nome
def obter_usuarios_por_nome(nome):
    conn = obter_conexao()
    cursor = conn.cursor()

    # Seleciona os usuários cujo nome começa com o prefixo fornecido
    cursor.execute('SELECT * FROM usuarios WHERE nome LIKE :nome', {'nome': f'{nome}%'})
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return usuarios


# Função para atualizar a senha de um usuário
def atualizar_senha_usuario(usuario_id, nova_senha):
    conn = obter_conexao()
    cursor = conn.cursor()

    hash_senha_atualizada = hash_senha(nova_senha)
    cursor.execute('UPDATE usuarios SET hash_senha = :hash_senha WHERE usuario_id = :usuario_id',
                   {'hash_senha': hash_senha_atualizada, 'usuario_id': usuario_id})
    cursor.execute('UPDATE login_senha SET hash_senha = :hash_senha WHERE usuario_id = :usuario_id',
                   {'hash_senha': hash_senha_atualizada, 'usuario_id': usuario_id})

    conn.commit()
    cursor.close()
    conn.close()


# Função para deletar um usuário
def deletar_usuario(usuario_id):
    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM login_senha WHERE usuario_id = :usuario_id', {'usuario_id': usuario_id})
    cursor.execute('DELETE FROM usuarios WHERE usuario_id = :usuario_id', {'usuario_id': usuario_id})

    conn.commit()
    cursor.close()
    conn.close()


# Função para autenticar um usuário
def autenticar_usuario(login, senha):
    conn = obter_conexao()
    cursor = conn.cursor()

    cursor.execute('SELECT hash_senha FROM login_senha WHERE login = :login', {'login': login})
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado:
        hash_senha_armazenada = resultado[0]
        return hash_senha_armazenada == hash_senha(senha)

    return False
