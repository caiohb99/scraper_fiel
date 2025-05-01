from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Verifica a página atual e tenta encontrar o texto "Esgotado" ou o botão de comprar
def verificar_ou_comprar(driver):
    try:

        max_tentativas = 10000  # Número máximo de tentativas
        tentativas = 0
        while tentativas < max_tentativas:
            try:
                # Tentar localizar o texto "Comprar"
                comprar_text = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Comprar')]"))
                )
                print("Texto 'Comprar' encontrado!!")
                # Aqui você pode adicionar o código para clicar no botão de compra, se necessário
                break  # Sai do loop se o texto foi encontrado

            except Exception as e:
                print(f"Erro ao localizar 'Comprar': {e}")
                tentativas += 1
                print("Esperando 5 segundos antes de dar F5...")

                driver.refresh()  # Atualiza a página para tentar novamente
                if tentativas == max_tentativas:
                    print("Número máximo de tentativas alcançado. Encerrando.")

        elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main-content"]/div/div/a/div/div[2]/div[2]/p'))
        )
        elemento.click()
    except Exception as e:
        print(f"Erro ao ao verificar se esta esgotado: {e}")



def escolher_zona(driver):
    id = [

        'leste-inferior-lateral',
        'leste-superior-lateral',
        'leste-superior-central',
        'leste-inferior-central'
         # ,'oeste-superior'

    ]

    while True:
        # Verifica se algum botão foi clicado
        for ids in id:
            try:
                # Aguarda até que o botão esteja clicável
                elemento = WebDriverWait(driver, 0.4).until(
                    EC.element_to_be_clickable((By.ID, ids))

                )

                url_anterior = driver.current_url

                elemento.click()

                mudou_pagina = url_anterior == driver.current_url

                if mudou_pagina == False:
                    print(f"Elemento clicado com sucesso:")
                    elemento = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.disable-on-submit"))
                    )
                    elemento.click()
                    checkbox = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.NAME, "dependentes"))
                    )
                    if not checkbox.is_selected():
                        checkbox.click()

                    botao = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "submit_fieltorcedor_booking_by_dependente_form"))
                    )
                    botao.click()

                    return  # Sai da função se a página mudou
                else:
                    print(f"Cliquei, mas a página não mudou:")

                print(f"Elemento clicado com sucesso: {ids}")

            except Exception as e:
                # Caso não consiga clicar, exibe o erro e continua verificando os outros botões
                print(f"Erro ao tentar clicar em {ids}: {e}")

        # Caso nenhum botão tenha sido clicado, recarrega a página e tenta novamente
        print("Nenhum botão clicável encontrado. Recarregando a página e tentando novamente.")
        driver.refresh()



def run():
    # ⚙️ CONFIGURAÇÕES
    EMAIL = "46533814885"  # 🔹 Substitua pelo seu email do Fiel Torcedor
    SENHA = "982309C@io"  # 🔹 Substitua pela sua senha
    URL_LOGIN = "https://www.fieltorcedor.com.br/auth/login/"

    # 🔥 ABRINDO O NAVEGADOR
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    # Acessando a página de login
    driver.get(URL_LOGIN)

    # Espera até os campos de login (email e senha) estarem visíveis
    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))  # Espera o campo de email carregar por "name"
        )
        email_field.send_keys(EMAIL)
    except Exception as e:
        print(f"Erro ao localizar o campo de email: {e}")

    try:
        senha_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))  # Espera o campo de senha carregar por "name"
        )
        senha_field.send_keys(SENHA)
    except Exception as e:
        print(f"Erro ao localizar o campo de senha: {e}")

    # Agora, o script vai aguardar que você resolva o CAPTCHA manualmente
    print("Por favor, resolva o CAPTCHA manualmente e depois pressione Enter para continuar...")
    input("Pressione Enter depois de resolver o CAPTCHA...")

    # Submeter o formulário de login
    senha_field.send_keys(Keys.RETURN)

    # Espera um pouco para garantir que o login seja realizado
    time.sleep(5)

    # Verifica se estamos na página de 'Minha Conta', e redireciona para a página de jogos
    current_url = driver.current_url
    if "minha-conta" in current_url:
        print("Estamos na página de 'Minha Conta', redirecionando para os jogos...")
        driver.get("https://www.fieltorcedor.com.br/jogos/")
    else:
        print("Já estamos na página correta de jogos.")

    # Espera até que o botão "COMPRE AGORA" esteja visível na página de jogos
    try:
        compra_agora_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'COMPRE AGORA')]"))
        )
        compra_agora_button.click()  # Clica no botão de compra
    except Exception as e:
        print(f"Erro ao localizar o botão de 'COMPRE AGORA': {e}")

    # Espera carregar a página do jogo
    time.sleep(5)

    # Chama a função de verificar o status e comprar


    verificar_ou_comprar(driver=driver)
    escolher_zona(driver=driver)


    # Fechar o navegador após a execução
    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    run()