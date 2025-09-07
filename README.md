# 🔐 Shodan Hunter: Scanner de Dispositivos Web e Análise de Segurança

Este projeto automatiza buscas na [API do Shodan](https://shodan.io) para identificar dispositivos potencialmente expostos na internet (como roteadores, DVRs, Câmeras IP, etc.). Ele foca especialmente em interfaces HTTP que podem usar **credenciais fracas (ex: `admin:admin`)**. Para complementar, ele também executa varreduras com **Nmap** para coletar mais informações dos serviços expostos.

---

## ⚙️ Funcionalidades

- ✅ Pesquisa automatizada na API do Shodan.
- ✅ Verificação de dispositivos com *headers* de autenticação (`WWW-Authenticate`).
- ✅ Detecção de possíveis credenciais padrão como `admin:admin`.
- ✅ Execução opcional do Nmap para identificar serviços e versões nas portas encontradas.
- ✅ Resultados exportados para um arquivo `.csv` de fácil visualização.
- ✅ Suporte a execução com múltiplas *threads* para otimizar o tempo de varredura.
- ✅ Barra de progresso (`tqdm`) para acompanhar o andamento do processo.

---

## 🚀 Como usar

### 1. Pré-requisitos

Certifique-se de que você tem:

* **Python 3.7+** instalado.
* **Nmap** instalado. Se você usa Linux, pode instalá-lo facilmente com:

    ```bash
    sudo apt install nmap
    ```

### 2. Instalação

1.  Clone o repositório:

    ```bash
    git clone [https://github.com/lka1r0st0n/shodan_hunter.git](https://github.com/lka1r0st0n/shodan_hunter.git)
    cd shodan_hunter
    ```

2.  Instale as dependências Python:

    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuração

1.  Edite o arquivo **`shodan_hunter.py`** e substitua `YOUR_API_KEY_HERE` pela sua chave da API do Shodan:

    ```python
    SHODAN_API_KEY = 'YOUR_API_KEY_HERE'
    ```

    *Para obter sua chave, crie uma conta em [shodan.io](https://shodan.io).*

2.  Se desejar, altere a variável `QUERY` para focar a busca em outros dispositivos, organizações ou regiões.

### 4. Execução

Execute o script a partir do terminal:

```bash
python3 shodan_hunter.py
``` 

### 📄 Output

O script irá criar um arquivo chamado shodan_resultados.csv no mesmo diretório, contendo todos os dados coletados.

### 🧠 Exemplo de Uso Ético

Este projeto foi desenvolvido com propósitos educacionais e éticos, como:

Auditorias de segurança autorizadas.

Análise de exposição de ativos em ambientes controlados.

Simulações de resposta a incidentes.

Geração de relatórios de risco.

⚠️ Importante: O uso deste script para acessar sistemas sem permissão é ilegal e antiético. Use a ferramenta apenas em sistemas para os quais você tem autorização expressa. Siga sempre os princípios da ética hacker e as leis vigentes (ex: Marco Civil da Internet, LGPD, etc).

### 📦 Estrutura do Projeto

📁 shodan_hunter/
├── shodan_hunter.py      # Script principal
├── requirements.txt      # Dependências Python
├── README.md             # Documentação do projeto
└── shodan_resultados.csv # Arquivo de saída gerado após a execução