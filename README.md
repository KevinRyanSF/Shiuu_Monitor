# Shiuu Monitor

## Visão Geral
O **Shiuu Monitor** é um sistema para monitoramento de níveis de ruído, utilizando um medidor de decibéis simulado por algoritmo. Ele permite o armazenamento de histórico diário, alertas para picos prejudiciais à saúde, configuração de limites personalizáveis e envio de notificações por e-mail. Além disso, o sistema possibilita a geração de relatórios em PDF com o histórico e informações detalhadas sobre os picos de ruído.

## Funcionalidades
- 🔔 **Alertas para níveis sonoros prejudiciais**
- 📅 **Registro do histórico de medições**
- 📩 **Notificações por e-mail**
- 📄 **Relatórios em PDF com histórico e dados de pico**
- ⚙️ **Configuração de limites personalizáveis**

## Tecnologias Utilizadas
- **Linguagem:** Python
- **Banco de Dados:** SQLite
- **Padrões de Projeto:** Singleton, Facade, Observer, Command, Strategy, Proxy
- **Bibliotecas:**
  - `maskpass` (para ocultação de senhas)
  - `requests` (para requisições HTTP)
  - `fpdf` (para geração de relatórios em PDF)
  - `subprocess` (para execução de processos)
  - `threading` (para execução assíncrona)

## Estrutura do Projeto
```
Shiuu_Monitor/
│── Hardware_decibéis/         # Simulação de medições de decibéis
│── Shiuu_monitor/
│   │── Classes/               # Definição de classes e estrutura do sistema
│   │── Commands/              # Implementação do padrão Command
│   │── Proxy/                 # Implementação do padrão Proxy para login
│   │── Strategy/              # Estratégias para manipulação de usuários
│   │── database.py            # Gerenciamento do banco de dados
│   │── monitorar_ambiente.py  # Função principal de monitoramento
│   │── main.py                # Ponto de entrada do sistema
│── README.md                  # Documentação do projeto
```

## Como Executar o Projeto
### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/Shiuu_Monitor.git
cd Shiuu_Monitor
```
### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```
### 3. Executar o Sistema
```bash
python Shiuu_monitor/main.py
```
---
**Desenvolvido por:** [Kevin Ryan, Demétrio Luna, Thiago Barbosa]
