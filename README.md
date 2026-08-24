# SearchHub
---
Aplicação Fullstack composta por APIs e interface web para validação, consulta e exportação de clientes, títulos e operações financeiras, voltada para operações de FGTS.

---

## Principais capacidades:
• Autenticação e autorização por perfil;
• Consultas de clientes e títulos;
• Processamento de planilhas;
• Geração de relatórios;
• Download de documentos via AWS S3;
• Cálculo de valor presente;
• Monitoramento de usuários;
• Auditoria de operações.


# Arquitetura e stack

---

A aplicação utiliza uma arquitetura simples e modular, separando a camada de apresentação, a API responsável pelas regras de negócio e a persistência dos dados.

            ┌──────────────────────────────┐
            │        Frontend Web          │
            │   HTML + CSS + JavaScript    │
            └──────────────┬───────────────┘
                           │
                      Fetch API / HTTP
                           │
                           ▼
            ┌──────────────────────────────┐
            │         API Backend          │
            │           FastAPI            │
            │    Rotas • Validação • CORS  │
            └──────────────┬───────────────┘
                           │
                          SQL
                           │
                           ▼
            ┌──────────────────────────────┐
            │         Banco de Dados       │
            │       SQLite / MariaDB       │
            └──────────────────────────────┘



# Stack utilizada:

| Camada | Tecnologia | Responsabilidade |
|------|------:|--------|
| Linguagem | Python | Implementação da lógica e regras da aplicação |
| Frontend | HTML5, CSS3, JavaScript | Interface e interação com o usuário |
| Comunicação | Fetch API | Comunicação assíncrona com o backend |
| Framework | FastAPI | Construção da API, rotas e processamento das requisições |
| Servidor | Uvicorn | Execução da aplicação ASGI |
| Banco de Dados | SQLite/MariaDB | Persistência dos clientes e operações |
| Integração | CORS Middleware | Controle de requisições entre origens |

• As bibliotecas utilizadas pelo projeto podem ser vistas nos arquivos que estão na raiz do projeto:
    • requirements.txt

---
# Funcionalidades

1. Buscar Clientes

O sistema permite pesquisar por:
• Nome do cliente;
• CPF/Documento;
• Número de contrato;
• Empresa / Originador;
• Empresa / Fundo.

E retorna os resultados de forma instantânea em uma interface dinâmica e com paginação de 1000 clientes por aba.

• Quando elegível, sistema também indica caminho para download do lastro que está no Bucket AWS S3 da empresa, permitindo baixar direto pela sua interface com apenas um clique.

• Funcionalidade também permite visualizar fluxo de parcelas do cliente apertando no título desejado, assim é aberto um pop-up que carrega o fluxo com informações como "Data de Vencimento", "Valor nominal" e se a parcela foi paga ou se está em aberto;

• Funcionalidade também permite o download de uma planilha Excel com todo o retorno da busca feita pelo usuário. Esse Excel pode ser baixado tanto por contrato resumido, como por parcela.

---
2. Buscar Clientes (Planilha)

Assim como a funcionalidade "1.", essa retorna os clientes, mas o usuário busca utilizando uma planilha.

Sistema aceita upload de uma planilha contendo colunas "CPF, Nome Cliente e Contrato", e o sistema preenche cada linha com o nome da operação a qual aqueles contratos pertencem.

3. Relatórios

Funcionalidade criada para o download de operações inteiras.
Usuário seleciona uma operação, quais cessões deseja baixar - uma, múltiplas ou todas. -, quais colunas deseja e realiza o download de uma planilha contendo todos os contratos que atinjam os critérios definidos pelo usuário.

4. Calculadora

Funcionalidade é uma calculadora de valor presente de contratos criada pelo setor Operacional/Ativos e inclusa para melhoria de processo.

---

# Interface

A interface foi projetada para operação rápida e simples:
• Barra de pesquisa centralizada;
• Feedback imediato de busca;
• Tabela organizada estilo CRM;
• Mensagens de status "Status Code": Buscando, erro, sem resultados, etc.

---

# Como executar o projeto

1. Instalar dependências
pip install fastapi uvicorn

2. Rodar o servidor
uvicorn main:app --reload

3. Acessar no navegador
http://127.0.0.1:8000/

Estrutura do Projeto:

Projeto/
├── database/
├── logs/
├── modelos/
├── rotas/
├── static/
├──templates/
├── main.py

# Exemplo de busca

Entrada: João
Exemplo fictício de Saída:

| Cliente | Empresa | Contrato |
|------|------:|--------|
| João Silva | Empresa 1 | xpto |
| João Andrade | Empresa 2 | abcd |
| João Ferreira | Empresa 1 | xyz |

---

## Segurança, Controle de Acesso e Governança

O sistema possui uma camada de autenticação, autorização e auditoria responsável por controlar o acesso às funcionalidades e manter a rastreabilidade das operações realizadas pelos usuários.

### Autenticação

* Tela de **login obrigatória** para acesso ao sistema.
* Usuários não autenticados são direcionados para a tela de login.
* O acesso às funcionalidades depende de uma **sessão de usuário válida**.
* Ao realizar logout, a sessão é encerrada e o usuário retorna ao login.
* O acesso direto às URLs das funcionalidades também é protegido, impedindo que usuários não autenticados contornem a tela de login.

### Controle de Acesso

O sistema utiliza **níveis de acesso baseados no perfil do usuário**, permitindo controlar quais funcionalidades cada usuário pode utilizar.

| Perfil            | Nível de acesso                                                     |
| ----------------- | ------------------------------------------------------------------- |
| **Operacional**   | Acesso restrito às funcionalidades necessárias para suas atividades |
| **Administrador** | Acesso completo às funcionalidades do sistema                       |

As permissões são verificadas no acesso às funcionalidades, garantindo que um usuário não consiga utilizar recursos que não estejam disponíveis para o seu perfil simplesmente alterando a URL ou tentando acessar diretamente uma rota.

### Governança

O modelo de acesso segue o princípio de **permissão conforme a responsabilidade do usuário**, permitindo:

* Separação de responsabilidades entre usuários.
* Restrição de funcionalidades por perfil.
* Controle centralizado de permissões.
* Proteção contra acesso não autenticado.
* Bloqueio de acesso indevido a funcionalidades restritas.
* Estrutura preparada para inclusão de novos perfis e níveis de permissão.


### Painel Administrativo e Auditoria

O sistema possui um painel administrativo destinado ao gerenciamento e acompanhamento dos usuários e da utilização da aplicação.

Entre os recursos disponíveis estão:

• Visualização dos usuários cadastrados.
• Visualização de usuários aguardando aprovação.
• Monitoramento de usuários atualmente online.
• Identificação de usuários utilizando o sistema.
• Desconexão imediata de usuários ativos.
• Acompanhamento dos eventos realizados dentro da aplicação.

### Auditoria e Logs

As principais ações realizadas no sistema são registradas por meio de logs de auditoria, criando uma trilha de rastreabilidade das operações executadas.

Entre os eventos registrados estão:

• Login e logout.
• Abertura de funcionalidades.
• Consultas realizadas.
• Pesquisas.
• Downloads.
• Geração de relatórios.
• Outras operações relevantes realizadas pelos usuários.

Os registros podem ser acompanhados pelo administrador em tempo real, permitindo monitoramento da utilização do sistema, identificação de comportamentos indevidos e maior controle sobre os processos operacionais.

Esse mecanismo contribui para a segurança, rastreabilidade, responsabilização e governança da aplicação, mantendo um histórico das ações executadas pelos usuários.