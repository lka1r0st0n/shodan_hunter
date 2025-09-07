import shodan
import csv
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# === CONFIGURAÇÕES ===
SHODAN_API_KEY = 'YOUR_API_KEY_HERE'  # <-- Substitua pela sua API Key
QUERY = 'http.favicon.hash:999357577 country:"BR" port:80,8080,443,8443' # <--org:"" city:"" state:""
OUTPUT_CSV = 'shodan_resultados.csv'
RODAR_NMAP = True
THREADS_NMAP = 5  # Número de threads para Nmap

# === INICIALIZA API ===
api = shodan.Shodan(SHODAN_API_KEY)


def salvar_csv(dados, caminho_csv):
    """Salva os resultados em um arquivo CSV."""
    with open(caminho_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['IP', 'Porta', 'Organização', 'ISP', 'Cidade', 'País',
                      'WWW-Authenticate', 'Suspeita admin:admin', 'Banner', 'Nmap']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for linha in dados:
            writer.writerow(linha)


def rodar_nmap(ip, porta):
    """Executa um Nmap -sV no IP e porta informados."""
    try:
        resultado = subprocess.check_output(
            ['nmap', '-sV', '-Pn', '-p', str(porta), ip],
            stderr=subprocess.DEVNULL
        ).decode('utf-8')
        return resultado.strip()
    except subprocess.CalledProcessError:
        return 'Erro ao executar Nmap'


def analisar_banner(banner):
    """Verifica se há autenticação e possíveis credenciais padrão no banner."""
    banner_lower = banner.lower()
    tem_auth = 'www-authenticate' in banner_lower or 'authorization required' in banner_lower
    suspeita_admin = any(keyword in banner_lower for keyword in ['admin', 'default password', 'senha padrão'])
    return tem_auth, suspeita_admin


def processar_resultado(result):
    """Processa um único resultado do Shodan."""
    ip = result.get('ip_str', '')
    port = result.get('port', '')
    org = result.get('org', '')
    isp = result.get('isp', '')
    city = result.get('location', {}).get('city', '')
    country = result.get('location', {}).get('country_name', '')
    banner = result.get('data', '').replace('\n', ' ')[:300]

    tem_auth, suspeita_admin = analisar_banner(banner)

    nmap_resultado = rodar_nmap(ip, port) if RODAR_NMAP else "Nmap não executado"

    return {
        'IP': ip,
        'Porta': port,
        'Organização': org,
        'ISP': isp,
        'Cidade': city,
        'País': country,
        'WWW-Authenticate': "Sim" if tem_auth else "Não",
        'Suspeita admin:admin': "Sim" if suspeita_admin else "Não",
        'Banner': banner,
        'Nmap': nmap_resultado
    }


def main():
    try:
        print("[*] Buscando resultados no Shodan...")
        results = api.search(QUERY)
        total = results.get('total', 0)
        print(f"[✔] {total} resultados encontrados.")

        matches = results['matches']
        resultados_processados = []

        if RODAR_NMAP and THREADS_NMAP > 1:
            print(f"[*] Executando Nmap com {THREADS_NMAP} threads...")
            with ThreadPoolExecutor(max_workers=THREADS_NMAP) as executor:
                future_to_result = {
                    executor.submit(processar_resultado, result): result
                    for result in matches
                }
                for future in tqdm(as_completed(future_to_result), total=len(future_to_result)):
                    try:
                        resultados_processados.append(future.result())
                    except Exception as e:
                        print(f"[!] Erro ao processar resultado: {e}")
        else:
            print("[*] Processando sem threads...")
            for result in tqdm(matches, desc="Processando"):
                try:
                    resultado = processar_resultado(result)
                    resultados_processados.append(resultado)
                except Exception as e:
                    print(f"[!] Erro ao processar {result.get('ip_str', '')}: {e}")

        salvar_csv(resultados_processados, OUTPUT_CSV)
        print(f"\n[✔] Resultados salvos em: {OUTPUT_CSV}")

    except shodan.APIError as e:
        print(f"[!] Erro na API do Shodan: {e}")
    except Exception as e:
        print(f"[!] Erro inesperado: {e}")


if __name__ == "__main__":
    main()

# === FIM DO SCRIPT ===