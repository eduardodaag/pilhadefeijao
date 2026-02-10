import instaloader
import pandas as pd
import re
import os
from git import Repo
import time

# --- CONFIGURAÇÕES ---
USUARIO_INSTA = "oficialorgulhobrasil"
SENHA_INSTA = "!@#123!@#a"
URL_POST_DESAFIO = "https://www.instagram.com/p/DUlPXj9gCcQ/" 
ARQUIVO_SAIDA = 'palpites.csv'

# --- CONFIGURAÇÕES GITHUB (IMPORTANTE) ---
GITHUB_TOKEN = ""
GITHUB_REPO = "eduardodaag/pilhadefeijao" # Ex: guivieira/pilhadefeijao
CAMINHO_LOCAL_REPOS = "./" # Pasta onde está o seu .git local

def subir_para_github():
    try:
        repo = Repo(CAMINHO_LOCAL_REPOS)
        repo.index.add([ARQUIVO_SAIDA])
        repo.index.commit("Atualização automática: " + time.strftime("%d/%m %H:%M"))
        origin = repo.remote(name='origin')
        url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
        origin.set_url(url)
        origin.push()
        print("✅ Dados enviados ao GitHub!")
    except Exception as e:
        print(f"❌ Erro no GitHub: {e}")

def rodar_extrator():
    L = instaloader.Instaloader()
    try:
        L.login(USUARIO_INSTA, SENHA_INSTA)
        shortcode = URL_POST_DESAFIO.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        
        dados_brutos = []
        for comment in post.get_comments():
            numeros = re.findall(r'\d+', comment.text)
            if numeros:
                palpite = int(numeros[0])
                # FILTRO DO INTERVALO: 0 a 30.000
                if 0 <= palpite <= 30000:
                    dados_brutos.append({
                        'usuario': comment.owner.username,
                        'palpite': palpite,
                        'data_postagem': comment.created_at_utc
                    })

        df = pd.DataFrame(dados_brutos)
        if not df.empty:
            df = df.sort_values('data_postagem')
            df = df.drop_duplicates(subset=['usuario'], keep='first')
            df = df.drop_duplicates(subset=['palpite'], keep='first')
            df.to_csv(ARQUIVO_SAIDA, index=False)
            subir_para_github()
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    while True:
        print("Iniciando atualização...")
        rodar_extrator()
        print("Aguardando 5 minutos para a próxima coleta...")
        time.sleep(300) # Atualiza sozinho a cada 5 min