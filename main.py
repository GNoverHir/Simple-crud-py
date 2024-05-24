import validacao
import banco_dados
from datetime import datetime


# Função para capturar entrada do usuário
def obter_entrada(mensagem):
    return input(mensagem).strip()


# Função para registrar um novo usuário
def registrar_usuario():
    tipo_login = obter_entrada("Digite o tipo de login (email, nome_usuario, cpf, rg): ").lower()
    login = obter_entrada(f"Digite o {tipo_login}: ")
    senha = obter_entrada("Digite a senha: ")

    erro = validacao.validar_login_e_senha(login, tipo_login, senha)
    if erro:
        print(f"Erro: {erro}")
        return

    email = obter_entrada("Digite o email: ")
    nome = obter_entrada("Digite o nome: ")
    rg = obter_entrada("Digite o RG: ")
    cpf = obter_entrada("Digite o CPF: ")
    data_nascimento = obter_entrada("Digite a data de nascimento (AAAA-MM-DD): ")
    endereco = obter_entrada("Digite o endereço: ")
    role = obter_entrada("Digite o papel (admin/usuario): ")

    dados_usuario = {
        'login': login,
        'tipo_login': tipo_login,
        'email': email,
        'nome': nome,
        'rg': rg,
        'cpf': cpf,
        'data_nascimento': data_nascimento,
        'hash_senha': banco_dados.hash_senha(senha),
        'endereco': endereco,
        'role': role
    }

    banco_dados.inserir_usuario(dados_usuario)
    print("Usuário registrado com sucesso!")


# Função para realizar login
def logar_usuario():
    tipo_login = obter_entrada("Digite o tipo de login (email, nome_usuario, cpf, rg): ").lower()
    login = obter_entrada(f"Digite o {tipo_login}: ")
    senha = obter_entrada("Digite a senha: ")

    if banco_dados.autenticar_usuario(login, senha):
        usuario = banco_dados.obter_usuario_por_login(login)
        print(f"Bem-vindo, {usuario[4]}!")
        return usuario
    else:
        print("Falha na autenticação. Verifique suas credenciais.")
        return None


# Função para atualizar a senha do usuário
def atualizar_senha_usuario(usuario):
    usuario_id = usuario[0]
    senha_atual = obter_entrada("Digite a senha atual: ")

    if banco_dados.autenticar_usuario(usuario[1], senha_atual):
        nova_senha = obter_entrada("Digite a nova senha: ")
        erro = validacao.senha_valida(nova_senha)

        if erro:
            print(f"Erro: {erro}")
            return

        banco_dados.atualizar_senha_usuario(usuario_id, nova_senha)
        print("Senha atualizada com sucesso!")
    else:
        print("Senha atual incorreta.")


# Função para deletar um usuário
def deletar_usuario():
    nome = obter_entrada("Digite o nome dos usuários a serem listados: ")
    usuarios = banco_dados.obter_usuarios_por_nome(nome)

    for usuario in usuarios:
        print(f"ID: {usuario[0]}, Nome: {usuario[4]}, Role: {usuario[10]}")

    usuario_id = int(obter_entrada("Digite o ID do usuário a ser deletado: "))
    banco_dados.deletar_usuario(usuario_id)
    print("Usuário deletado com sucesso!")


# Função principal
def main():
    while True:
        print("1. Registrar Usuário")
        print("2. Login")
        print("3. Atualizar Senha")
        print("4. Deletar Usuário")
        print("5. Sair")

        escolha = obter_entrada("Digite sua escolha: ")

        if escolha == '1':
            registrar_usuario()
        elif escolha == '2':
            usuario = logar_usuario()
            if usuario:
                print("1. Atualizar Senha")
                print("2. Logout")
                sub_escolha = obter_entrada("Digite sua escolha: ")
                if sub_escolha == '1':
                    atualizar_senha_usuario(usuario)
        elif escolha == '3':
            if usuario:
                atualizar_senha_usuario(usuario)
        elif escolha == '4':
            deletar_usuario()
        elif escolha == '5':
            break
        else:
            print("Escolha inválida. Tente novamente.")


main()
