<div>
  <div align="center">
    <img src="./assets/logo_advice.png" />
  </div>
  
  <h2>Teste técnico para vaga de Desenvolvedor Python na AdviceHealth</h2>
</div>

O projeto AdviceHealth car API é uma aplicação web desenvolvida utilizando Flask e PostgreSQL, implantada em contêineres Docker. Ele oferece uma plataforma para gerenciar os carros da CarFord e seus proprietários.

<br/>

## Endpoints

**POST /cars**<br/>
> Adiciona um carro novo para um proprietário específico.
- Exemplo
```ts
curl -X POST -H "Content-Type: application/json" -d '{"color":"blue", "model":"sedan", "owner_id":1}' http://localhost:5000/cars
```

**POST /owners**<br/>
> Adiciona um novo proprietário de carro.
- Exemplo
```ts
curl -X POST -H "Content-Type: application/json" -d '{"name":"Caio Lucas", "email":"caio@example.com"}' http://localhost:5000/car_owners
```

**GET /owners**<br/>
> Retorna uma lista de todos os proprietários de carros registrados.
- Exemplo
```ts
curl http://localhost:5000/car_owners
```

**GET /owners/<owner_id>/cars**<br/>
> Recupera uma lista de carros pertencentes ao proprietário especificado por owner_id.
- Exemplo
```ts
curl http://localhost:5000/car_owners/1/cars
```

**DELETE /owners/<owner_id>**<br/>
> Remove um proprietário de carro específico pelo seu ID, juntamente com todos os carros associados.
- Exemplo
```ts
curl -X DELETE http://localhost:5000/car_owners/1
```

**DELETE /cars/<car_id>**<br/>
> Remove um carro específico pelo seu ID.
- Exemplo
```ts
curl -X DELETE http://localhost:5000/cars/1
```

<br/>

## Instalação Windows

```bash
git clone https://github.com/willyanmiranda/advicehealth-car-api.git

cd advicehealth-car-api
```

Crie um ambiente virtual para isolar suas dependências de outros projetos usando venv:

```bash
python -m venv venv
```

Para ativar o ambiente virtual, use:

```bash
venv\Scripts\activate
```

Instale as dependências listadas no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

Inicie o container
```bash
docker-compose up --build
```

## Instalação Linux

```bash
git clone https://github.com/willyanmiranda/advicehealth-car-api.git

cd advicehealth-car-api
```

Crie um ambiente virtual para isolar suas dependências de outros projetos usando venv:

```bash
python -m venv venv
```

Para ativar o ambiente virtual, use:

```bash
source venv/bin/activate
```

Instale as dependências listadas no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

Inicie o container
```bash
make build
```
<br/>

## Tecnologias
- Docker
- Python
- Flask
- SQLAlchemy
- PostgreSQL