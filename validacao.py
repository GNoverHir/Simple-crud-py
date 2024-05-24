import re
# https://docs.python.org/pt-br/3/library/re.html
# Boa biblioteca paara se usar quando queremos encontrar padrões em textos


# Verifica se o email está no formato válido
def email_valido(email):

    # o use de re.match ajuda pois ele verifica se a pattern corresponde a string inicial.
    # No caso no primeiro [] ele confere se há  um ou mais caracteres alfanuméricos, ponto, sublinhado, percentual, mais ou hífen.
    # Na segunda parte seguida de @ ele confere a mesma coisa, e na terceir [] ele confere se a pelo menos 2.
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None


# Verifica se o nome de usuário está no formato válido
def nome_usuario_valido(nome_usuario):

    return re.match(r"^[a-zA-Z0-9_]+$", nome_usuario) is not None


# Verifica se o CPF está no formato válido
def cpf_valido(cpf):

    # Analisar se corresponde a 11 digitous ou se usa o formato xxx.xxx.xxx.xx
    # o uso do metacaractere \d é para represetar qualquer numero decimal 0-9.
    return re.match(r"^\d{11}$|^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf) is not None


# Verifica se o RG está no formato válido
def rg_valido(rg):

    # Mesma coisa que o cpf, porem com 9 digitos e formato xx.xxx.xxx.x
    return re.match(r"^\d{9}$|^\d{2}\.\d{3}\.\d{3}-\d{1}$", rg) is not None


# Verifica se a senha cumpre os requisitos
def senha_valida(senha):

    # Verifica se a senha tem pelo menos 15 caracteres
    if len(senha) < 15:
        return False

    # Verifica se a senha tem pelo menos 3 dígitos numéricos.
    # O uso de re.findall tem um padrao de re.findall(padrão, string).
    # Ele percorre o mihna string e encontra todas aas ocorrênciaas de um padrão q eu passar.
    if len(re.findall(r"\d", senha)) < 3:
        return False

    # Verifica se a senha tem pelo menos 3 caracteres maiúsculos
    if len(re.findall(r"[A-Z]", senha)) < 3:
        return False

    # Verifica se a senha tem pelo menos 3 caracteres minúsculos
    if len(re.findall(r"[a-z]", senha)) < 3:
        return False

    # Verifica se a senha tem pelo menos 3 caracteres especiais
    if len(re.findall(r"[!@#$%&*(){}\[\];,.:/\\|]", senha)) < 3:
        return False
    return True


# Valida o login e a senha
def validar_login_e_senha(login, tipo_login, senha):
    if tipo_login == "email" and not email_valido(login):
        return "Formato de email inválido"
    elif tipo_login == "nome_usuario" and not nome_usuario_valido(login):
        return "Formato de nome de usuário inválido"
    elif tipo_login == "cpf" and not cpf_valido(login):
        return "Formato de CPF inválido"
    elif tipo_login == "rg" and not rg_valido(login):
        return "Formato de RG inválido"

    if not senha_valida(senha):
        return "Formato de senha inválido"

    return None
