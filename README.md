# DefectFlow API

API desenvolvida como parte do MVP da disciplina **Desenvolvimento Full Stack Básico**.

O **DefectFlow API** é o back-end de uma aplicação web para registro, triagem e acompanhamento inicial de defeitos. A solução permite cadastrar defeitos, consultar registros, atualizar status, remover registros e sugerir automaticamente o tipo de comitê aplicável com base na severidade e no possível impacto de segurança.

---

## Objetivo do projeto

O objetivo do projeto é apoiar a rastreabilidade inicial de defeitos, permitindo que informações mínimas sejam registradas de forma estruturada.

A API oferece recursos para:

- cadastrar defeitos;
- listar todos os defeitos cadastrados;
- buscar um defeito específico por ID;
- atualizar o status de um defeito;
- remover um defeito;
- gerar um código amigável para rastreabilidade, como `DEF-0001`;
- sugerir automaticamente o comitê aplicável, como `CRB` ou `ECRB`.

---

## Tecnologias utilizadas

- Python
- Flask
- flask-openapi3
- Flask-CORS
- SQLAlchemy
- SQLAlchemy-Utils
- Pydantic
- SQLite

---

## Estrutura principal do projeto

```text
mvp-defectflow-api
│
├── app.py
├── logger.py
├── requirements.txt
├── README.md
│
├── database
│   └── db.sqlite3
│
├── model
│   ├── __init__.py
│   ├── base.py
│   └── defeito.py
│
└── schemas
    ├── __init__.py
    ├── defeito.py
    └── error.py
```

---

## Modelo de dados principal

A entidade principal da API é o **Defeito**.

Campos principais:

- `id`: identificador técnico do banco de dados;
- `codigo_defeito`: código amigável gerado a partir do ID, como `DEF-0001`;
- `titulo`: título resumido do defeito;
- `descricao`: descrição detalhada do defeito;
- `origem`: origem do defeito;
- `componente`: componente ou módulo impactado;
- `categoria`: categoria técnica ou processual do defeito;
- `severidade`: classificação de severidade;
- `impacto_operacional`: descrição do impacto operacional;
- `impacto_seguranca`: indicação booleana de possível impacto à segurança;
- `comite_sugerido`: sugestão automática de comitê;
- `responsavel`: responsável pela análise;
- `status`: status atual da tratativa.

---

## Regras de negócio implementadas

A API sugere automaticamente o comitê aplicável conforme a lógica abaixo:

```text
Se impacto_seguranca = true
    então comite_sugerido = ECRB

Se severidade = S1 ou S2
    então comite_sugerido = ECRB

Se severidade = S3 ou S4
    então comite_sugerido = CRB

Caso contrário
    então comite_sugerido = Não definido
```

Também é gerado um código amigável para cada defeito:

```text
id = 1  → DEF-0001
id = 2  → DEF-0002
id = 15 → DEF-0015
```

---

## Rotas disponíveis

### Documentação

```text
GET /
```

Redireciona para a documentação OpenAPI/Swagger da API.

---

### Cadastrar defeito

```text
POST /defeito
```

Cadastra um novo defeito na base de dados.

Exemplo de dados:

```json
{
  "titulo": "Falha na abertura de tela operacional",
  "descricao": "Usuário reportou erro ao acessar funcionalidade crítica do sistema.",
  "origem": "Teste interno",
  "componente": "Interface operacional",
  "categoria": "Falha de interface",
  "severidade": "S2",
  "impacto_operacional": "Funcionalidade indisponível para parte dos usuários.",
  "impacto_seguranca": false,
  "responsavel": "Time Técnico",
  "status": "Aberto"
}
```

---

### Listar defeitos

```text
GET /defeitos
```

Retorna todos os defeitos cadastrados.

---

### Buscar defeito por ID

```text
GET /defeito
```

Busca um defeito específico a partir do ID.

Exemplo:

```text
GET /defeito?id=1
```

---

### Atualizar status de defeito

```text
PUT /defeito
```

Atualiza o status de um defeito cadastrado.

Exemplo:

```json
{
  "id": 1,
  "status": "Em análise técnica"
}
```

---

### Deletar defeito

```text
DELETE /defeito
```

Remove um defeito a partir do ID.

Exemplo:

```text
DELETE /defeito?id=1
```

---

## Status disponíveis

Os status aceitos pela API são:

- `Aberto`
- `Em triagem`
- `Em análise técnica`
- `Aguardando comitê`
- `Plano de ação definido`
- `Em correção`
- `Encerrado`
- `Rejeitado`

---

## Origens disponíveis

As origens aceitas pela API são:

- `Cliente`
- `Teste interno`
- `Operação`
- `Monitoramento`
- `Auditoria`
- `Outro`

---

## Categorias disponíveis

As categorias aceitas pela API são:

- `Fadiga`
- `Desgaste`
- `Sobrecarga`
- `Fluência`
- `Falha de interface`
- `Falha de comunicação`
- `Falha de configuração`
- `Falha operacional`
- `Outro`

---

## Severidades disponíveis

As severidades aceitas pela API são:

- `S1`
- `S2`
- `S3`
- `S4`

---

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone <link-do-repositorio>
```

### 2. Acessar a pasta do projeto

```bash
cd mvp-defectflow-api
```

### 3. Criar ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

### 6. Executar a API

Para executar a API localmente, acesse a pasta do projeto e rode:

```bash
python -m flask --app app run --host 127.0.0.1 --port 5000
```

### 7. Acessar a documentação Swagger

Abra no navegador:

```text
http://localhost:5000
```

Ou diretamente:

```text
http://localhost:5000/openapi/swagger
```

---

## Banco de dados

A aplicação utiliza SQLite como banco de dados local.

O banco é criado automaticamente na pasta:

```text
database/db.sqlite3
```

Caso o arquivo não exista, a aplicação cria a estrutura necessária ao iniciar.

---

## Observações

Este projeto foi desenvolvido com fins acadêmicos, como parte de um MVP para a disciplina **Desenvolvimento Full Stack Básico**.

O escopo foi limitado de forma intencional para representar um produto mínimo viável, priorizando:

- clareza da lógica de negócio;
- separação entre API, banco e documentação;
- uso de rotas REST;
- armazenamento em SQLite;
- documentação via Swagger/OpenAPI;
- estrutura simples para posterior integração com front-end.

---

## Próximas melhorias possíveis

Algumas melhorias futuras possíveis seriam:

- criação de autenticação de usuário;
- inclusão de perfis de acesso;
- criação de histórico detalhado de alterações;
- adição de comentários ou tratativas por defeito;
- filtros por severidade, status, categoria e comitê sugerido;
- dashboard de indicadores;
- integração com ferramentas externas de rastreabilidade.