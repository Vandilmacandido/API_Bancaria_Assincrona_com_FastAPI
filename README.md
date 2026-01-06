# Guia da API Bancária (Banking API Walkthrough)

**FastAPI**.

## Funcionalidades Implementadas

* **FastAPI**: Aplicação com suporte nativo a `AsyncIO`.
* **Banco de Dados**: SQLite com **SQLAlchemy (Async)** para persistência de dados.
* **Autenticação JWT**: Segurança para acesso aos endpoints.
* **Transações**: Depósito, Saque e Extrato.
* **Validações**: Verificação de saldo insuficiente e de valores positivos.

## Estrutura do Projeto

```text
app/
├── main.py           # Ponto de entrada (Entry point)
├── models.py         # Modelos do banco de dados (SQLAlchemy)
├── schemas.py        # Esquemas de validação (Pydantic)
├── database.py       # Configuração da conexão assíncrona
├── security.py       # Lógica de segurança (JWT, Hash de senha)
└── routes/
    ├── auth.py       # Endpoints de Login e Registro
    └── transactions.py # Operações bancárias (Saque, depósito, extrato)

##Como Executar

1. Instalar Dependências

pip install -r requirements.txt

2. Rodar o Servidor

Bash
uvicorn app.main:app --reload

3. Acessar Documentação
Abra o navegador em http://127.0.0.1:8000/docs para visualizar a interface interativa do Swagger UI.

Resultados da Verificação
Utilizei o script verify_api.py para testar os endpoints. Autenticação, Depósitos, Saques e consulta de Extrato estão funcionando conforme esperado.

Exemplo de Saída (Script de Verificação)
Registrando Usuário...

Success: {'username': 'testuser', 'id': 1, 'balance': 0.0, 'transactions': []}

Fazendo Login...

Success: Got Token

Depositando 100.0...

Status: 200

Response: {'username': 'testuser', 'id': 1, 'balance': 200.0, ...}

Sacando 50.0...

Status: 200

Response: {'username': 'testuser', 'id': 1, 'balance': 150.0, ...}

Obtendo Extrato...

Balance: 150.0

Transactions Count: 3

Principais Decisões de Design
SQLAlchemy Assíncrono: Uso de selectinload e gerenciamento de sessões assíncronas para alta performance.

JWT (JSON Web Tokens): Autenticação stateless robusta com python-jose e passlib.

Pydantic: Validação de dados rigorosa para garantir a integridade de todas as entradas da API.


