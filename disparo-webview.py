import requests
import re
import json
import sys
import time
import uuid
import pandas as pd
import os
import argparse
from pathlib import Path

# Lê canais do channel.json
def carregar_canais(channel_json_path):
    with open(channel_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    canais = {}
    for k, v in data['env'].items():
        canais[k] = v['channel_id']
    return canais

channel_json_path = 'channel.json'
canal_dict = carregar_canais(channel_json_path)
canal_nomes = list(canal_dict.keys())


print("\nCanais disponíveis para teste:")
for nome in canal_nomes:
    print(f"- {nome}")
print("\nInforme os canais desejados usando --channels canal1,canal2 ...\n")
parser = argparse.ArgumentParser(description="Dispara frases para webview e captura respostas.")
parser.add_argument("input_file", nargs="?", help="Nome do arquivo de entrada na pasta input (.txt, .csv, .xlsx)")
parser.add_argument("--channels", type=str, help=f"Canais a executar, separados por vírgula. Opções: {', '.join(canal_nomes)}")
parser.add_argument("--env", type=str, default="pro", help="Ambiente: pro, pre, est")
args = parser.parse_args()
env = args.env

session = requests.Session()
session.headers.update({
    "accept": "*/*",
    "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "origin": f"https://svc-br-{env}.auracognitive.com",
    "priority": "u=1, i",
    "referer": f"https://svc-br-{env}.auracognitive.com/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
    "x-ms-bot-agent": "DirectLine/3.0 (directlinejs 0.15.6)",
    "x-requested-with": "XMLHttpRequest",
    # "authorization" será definido dinamicamente para cada requisição com o token extraído do HTML
    # "content-type" será definido por requests automaticamente
    # "cookie": "...",  # adicione se necessário
})

# Substitui blocos estáticos de input/output por argumentos e lógica dinâmica
def strip_html_tags(text):
    if not text:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


print("\nCanais disponíveis para teste:")
for nome in canal_nomes:
    print(f"- {nome}")
print("\nInforme os canais desejados usando --channels canal1,canal2 ...\n")
parser = argparse.ArgumentParser(description="Dispara frases para webview e captura respostas.")
parser.add_argument("input_file", nargs="?", help="Nome do arquivo de entrada na pasta input (.txt, .csv, .xlsx)")
parser.add_argument("--channels", type=str, help=f"Canais a executar, separados por vírgula. Opções: {', '.join(canal_nomes)}")
args = parser.parse_args()



# Se não foi informado input_file, busca o primeiro arquivo válido na pasta input
if args.input_file:
    input_file = args.input_file
    if not os.path.isabs(input_file):
        input_file = os.path.join('input', input_file) if not input_file.startswith('input' + os.sep) else input_file
else:
    import glob
    arquivos = glob.glob(os.path.join('input', '*'))
    arquivos_validos = [f for f in arquivos if f.lower().endswith(('.txt','.csv','.xlsx','.xls'))]
    if arquivos_validos:
        input_file = arquivos_validos[0]
        print(f"Arquivo de entrada detectado automaticamente: {input_file}")
    else:
        print("Nenhum arquivo válido (.txt, .csv, .xlsx, .xls) encontrado na pasta input.")
        sys.exit(1)

def get_default_headers(env):
    return {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "origin": f"https://svc-br-{env}.auracognitive.com",
        "priority": "u=1, i",
        "referer": f"https://svc-br-{env}.auracognitive.com/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "x-ms-bot-agent": "DirectLine/3.0 (directlinejs 0.15.6)",
        "x-requested-with": "XMLHttpRequest",
        # "authorization" será definido dinamicamente para cada requisição com o token extraído do HTML
        # "content-type" será definido por requests automaticamente
        # "cookie": "...",  # adicione se necessário
    }

if args.channels:
    channels_selecionados = [c.strip() for c in args.channels.split(',')]
else:
    canais_input = input("Digite os canais desejados separados por vírgula: ")
    channels_selecionados = [c.strip() for c in canais_input.split(',')]

for canal in channels_selecionados:
    if canal not in canal_dict:
        print(f"Canal '{canal}' não encontrado em channel.json. Opções: {', '.join(canal_nomes)}")
        sys.exit(1)


import glob
# Aceita qualquer arquivo .txt, .csv ou .xlsx/.xls na pasta input
if not os.path.isfile(input_file):
    # Tenta encontrar arquivo na pasta input com o nome base
    base_name = Path(input_file).stem
    possiveis = glob.glob(os.path.join('input', f'{base_name}.*'))
    possiveis = [f for f in possiveis if f.lower().endswith(('.txt','.csv','.xlsx','.xls'))]
    if possiveis:
        input_file = possiveis[0]
    else:
        print(f"Arquivo de entrada '{input_file}' não encontrado na pasta input. Certifique-se de que existe um arquivo .txt, .csv ou .xlsx/.xls com esse nome.")
        sys.exit(1)

ext = Path(input_file).suffix.lower()
if ext in [".xlsx", ".xls"]:
    df_in = pd.read_excel(input_file)
    # usa coluna 'frase' se existir, senão a primeira coluna
    if "frase" in df_in.columns:
        frases = df_in["frase"].astype(str).tolist()
    else:
        frases = df_in.iloc[:, 0].astype(str).tolist()
elif ext == ".csv":
    df_in = pd.read_csv(input_file)
    if "frase" in df_in.columns:
        frases = df_in["frase"].astype(str).tolist()
    else:
        frases = df_in.iloc[:, 0].astype(str).tolist()
elif ext == ".txt":
    with open(input_file, "r", encoding="utf-8") as f:
        frases = [linha.strip() for linha in f if linha.strip()]
else:
    print(f"Extensão de arquivo '{ext}' não suportada. Use .txt, .csv ou .xlsx/.xls na pasta input.")
    sys.exit(1)

# Loop para cada canal selecionado

for canal in channels_selecionados:

    channel_id = canal_dict[canal]
    print(f"\n=== Executando para canal: {canal} (channel_id: {channel_id}) ===")
    base = Path(input_file).stem
    output_xlsx = os.path.join('output', f"output_{base}_{canal}.xlsx")
    resultados = []

    url = f"https://svc-br-{env}.auracognitive.com/aura-services/v1/aura-widget/web?locale=pt-BR&skin=newui&auraId=dc6ece38-6e2e-4848-8be6-16afced1c059&conversationId=&channelId={channel_id}&token=&apiKey=bbc71501a7228fe7c1cd6c7e72183a88f1e4333964b5aa60ab06ddc12bad29321dbed291cdc4e15cd2bc2d31fd807a65c62b10db6a22bc247e168799721ee34d77c057b58f4862b8aca9e06009f58fc7a697fddf9296b2f452c92fb2bc9270a8cdd95682e56c837cfff24a6ec7112449aebb0515674e6563f912f9d9e355102f3a32f0e6a397067e868c0854af20037fecc47afa71f95f0e1c84e340b8ade55c75c79cfbff398f8428fd1185ce72521eefd290b8c3091e53221a8b9275869d31445a725b66e84e0cbff0eb292c7b66b1"
    headers = {
        "Content-Type": "application/json"
    }

    print("Executando os testes...")
    start_time = time.time()  # Início da contagem do tempo

    for idx, frase in enumerate(frases, 1):
        print(f"\n[{idx}/{len(frases)}] Processando frase: {frase}")
        print("Solicitando nova sessão/conversa...")

        session = requests.Session()
        session.headers.update(get_default_headers(env))

        response = session.post(url, json={"message": "init"}, headers=headers)
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response.text, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            page_props = data.get("props", {}).get("pageProps", {})
            stream_url = page_props.get("streamUrl")
            token = page_props.get("token")
            print(f"streamUrl: {stream_url}")
            print(f"token: {token}")
            conv_match = re.search(r'/conversations/([^/]+)/', stream_url)
            if conv_match:
                conversation_id = conv_match.group(1)
                print(f"conversationId: {conversation_id}")
                directline_url = f"https://directline.botframework.com/v3/directline/conversations/{conversation_id}/activities"
                dl_headers = get_default_headers(env)
                dl_headers["authorization"] = f"Bearer {token}"
                dl_headers["content-type"] = "application/json"
                # appId fixo igual ao webview
                app_id = "06320f84-a9a6-4112-bdb8-7bc5bc8e1f91"
                dl_payload = {
                    "from": {"id": "dc6ece38-6e2e-4848-8be6-16afced1c059"},
                    "type": "message",
                    "text": frase,
                    "channelData": {
                        "msisdn": "dc6ece38-6e2e-4848-8be6-16afced1c059",
                        "input": "webview",
                        "appContext": {
                            "channel": {
                                "appId": app_id
                            }
                        },
                        "customData": {
                            "shouldHideMessage": False,
                            "appVivo": {
                                "isAndroid": False,
                                "isIOS": False,
                                "isWeb": True
                            }
                        },
                        "token": token
                    }
                }
                dl_response = session.post(directline_url, headers=dl_headers, json=dl_payload)
                print(f"Status envio mensagem: {dl_response.status_code}")
                time.sleep(3)
                print("Buscando resposta do bot...")
                acts_response = session.get(directline_url, headers=dl_headers)
                print(f"Status busca atividades: {acts_response.status_code}")
                acts_json = acts_response.json()
                activities = acts_json.get("activities", [])
                resposta = ""
                resposta_raw = ""
                for act in reversed(activities):
                    if act.get("from", {}).get("id") != "dc6ece38-6e2e-4848-8be6-16afced1c059" and act.get("type") == "message":
                        resposta = act.get("text", "")
                        resposta_raw = json.dumps(act, ensure_ascii=False)
                        break
                if not resposta:
                    resposta_final = "[ERRO OU SEM RESPOSTA] " + resposta_raw
                else:
                    resposta_final = strip_html_tags(resposta)
                resultados.append((frase, resposta_final))
                print(f"Frase: {frase}\nResposta: {resposta_final}\n")
            else:
                print("Não foi possível extrair o conversationId do streamUrl.")
                resultados.append((frase, "[ERRO] Não foi possível extrair o conversationId"))
        else:
            print("Não foi possível extrair o streamUrl e token.")
            resultados.append((frase, "[ERRO] Não foi possível extrair o streamUrl/token"))

    print("Salvando resultados em arquivo XLSX...")
    os.makedirs('output', exist_ok=True)
    df = pd.DataFrame(resultados, columns=["frase", "resposta"])
    df.to_excel(output_xlsx, index=False)
    print(f"Arquivo de saída salvo em: {output_xlsx}")

    end_time = time.time()  # Fim da contagem do tempo
    tempo_total = end_time - start_time
    print(f"Tempo total de execução dos testes: {tempo_total:.2f} segundos")

def strip_html_tags(text):
    if not text:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def get_default_headers(env):
    return {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "origin": f"https://svc-br-{env}.auracognitive.com",
        "priority": "u=1, i",
        "referer": f"https://svc-br-{env}.auracognitive.com/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
        "x-ms-bot-agent": "DirectLine/3.0 (directlinejs 0.15.6)",
        "x-requested-with": "XMLHttpRequest",
        # "authorization" será definido dinamicamente para cada requisição com o token extraído do HTML
        # "content-type" será definido por requests automaticamente
        # "cookie": "...",  # adicione se necessário
    }



# Salva apenas em XLSX
df = pd.DataFrame(resultados, columns=["frase", "resposta"])
df.to_excel(output_xlsx, index=False)
print(f"Arquivo de saída salvo em: {output_xlsx}")

end_time = time.time()  # Fim da contagem do tempo
tempo_total = end_time - start_time
print(f"Tempo total de execução dos testes: {tempo_total:.2f} segundos")