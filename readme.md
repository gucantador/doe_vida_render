# DOE VIDA API

A API utiliza JWT tokens. A lógica funciona da seguinte maneira:
- Para toda requisição em rotas protegitas com JWT é necessário passar o JWT token no headers do request.
- Para conseguir o token, é necessário ter uma conta (se não tiver basta criar, utilizando o POST da rota users) e fazer o login.
- Após o login, serão retornados o Accsses Token e o Refresh token. O Access tem a duração de 1 hora, e o Refresh tem a duração de 30 dias.
- Caso o access token espire, é necessário fazer uma requisição para a rota de repfresh passando o refresh token.

## ROTAS

NOTA: Substituir a URL base caso esteja usando localhost!

### USERS

```git
https://doevida.onrender.com/users
```
POST
- Cria um novo usuario.

```git
{
    "password": "secret_pass",
    "username": "example@gmail.com"    
}
```

GET
- Retorna todos os usúarios cadastrados.
- Necessita JWT token.

### LOGIN

```git
https://doevida.onrender.com/login
```
POST
- Cria um novo usuario
- Retorna um access e um refresh token.

```git
{
    "password": "secret_pass",
    "username": "example@gmail.com"    
}
```

### refresh

```git
https://doevida.onrender.com/refresh
```
POST
- Enviar com o refresh token no headers.
- Retorna um novo access token.

### users/usuario

Nota: Consideramos usuario o email do cadastrado.

```git
https://doevida.onrender.com/users/usuario
```
PUT
- Necessita JWT token.
- Realiza o update de um usuário.
- Não é necessário passar tudo de uma vez no JSON.

```git
{
    "birthdate": "10/01/2001",
    "blood_type": "A+",
    "city": "Campinas",
    "date_last_donation": null,
    "first_name": "jason",
    "id": "12",
    "last_name": "roberts",
    "password": "changed_password",
    "phone": "19914598",
    "qty_donations": "4",
    "sex": false,
    "state": "ceara",
    "username": "jeffersondsad"
}
```

GET
- Retorna o usuario.
- Necessita JWT token.

DELETE
- Deleta o usuário.
- Necessita JWT token.

### hospitals

```git
https://doevida.onrender.com/hospitals
```
POST
- Cadastra um novo hospital.

```git
{
    "city_name": "campinas",
    "hospital_name": "Hemocentro Campinas",
    "state": 1
}
```

GET
- Retorna todos os hospitais cadastrados.

### hospitals/hospital

```git
https://doevida.onrender.com/hospitals/hospital_name
```

GET
- Retorna o hospital.
- Necessita JWT.

PUT
- Necessita JWT
- Atualiza informações de um hospital
```git
{
    "city_name": "campinas",
    "hospital_name": "Hemocentro Campinas",
    "state": 1,
    "donations_orders": 1,
    "donations_orders_done":1,
    "donations_orders_cancelled":3
}
```
DELETE
- Deleta um hospital
- Necessita JWT.

### donations_orders

```git
https://doevida.onrender.com/donations_orders
```

GET
- Retorna todos os pedidos de doações.

POST
- Necessita JWT.
- Adiciona um novo pedido de doação.
- Caso o hospital seja novo, cadastra o hospital no banco.
- Adiciona um pedido de doação para o hospital.

```git
{	
	"patient_name":"jailson",
	"blood_type":1,
	"description":"donation",
	"qty_bags":4,
	"hospital":"dolores",
    "requester":1,
    "city_name": "campinas",
    "state": 1
}
```
### donations_orders/donation

```git
https://doevida.onrender.com/donations_orders/donation_id
```

GET
- Retorna a doação.
- Necessita JWT.

PUT
- Atualiza a doação.
- Utilizar para mudar o status da doação.
- Quando altera o status da doação, altera na tabela dos hospitais as quantidades de ordens completadas e canceladas.

```git
Exemplo de alteração de status.

{	
    "status": "cancelled"
}
```

Mas caso queira alterar algum outro aspecto da doação também pode.

```git
{	
	"patient_name":"jailson",
	"blood_type":1,
	"description":"donation",
	"qty_bags":4,
	"hospital":"dolores",
    "requester":1,
    "city_name": "campinas",
    "state": 1
    "status": "cancelled"
}
```


## COMO RODAR A API

### CLONAR O REPOSITORIO EM UMA PASTA DO SEU COMPUTADOR
```git
git clone https://github.com/Doe-Vida/BackEnd.git
cd .\BackEnd\
```

### CRIAR UM AMBIENTE VIRTUAL PARA INSTALAR AS LIBS PYTHON QUE UTILIZAMOS
```git
python -m venv venv
cd venv
.\Scripts\activate
cd ..
pip install -r requirements.txt
```

### ADICIONAR O ARQUIVO .ENV QUE ESTÁ NO DRIVE DO PROJETO NO DIRETORIO DO PROJETO

### DEPOIS DE INSTALADO TUDO E COM A VENV ATIVADA
```git
python app.py
```
### Caso tenha algum erro de nao reconhecer alguma lib
```git
pip install <lib_name>
```

## BASICO DA ARQUITETURA

O arquivo main.py importa o app (variavel na qual instanciamos nosso objeto flask) e com isso 
usa o metodo run para rodar a aplicação. Ou seja, para rodar a aplicação, basta ativar a venv
e rodar "python main.py" no terminal, com isso vai inicializar um servidor e podemos utilizar 
ele para chamar os requests e rotas da API. A principio está num local host, mas precisamos 
descobrir como fica essa parte quando fizermos o deploy.

O diretorio flask_app é um pocote, pois tem o arquivo __init__.py. No init instanciamos e configuramos o objeto flask e o objeto do banco de dados.

No arquivo models estão definidos os modelos do banco de dados, cade classe que herda o model representa uma tabela no banco de dados, cada variavel uma coluna. Dentro da classe também precisamos criar um metodo to_dict pois o python não reconhece o json diretamente, entao precisamos sempre transformar dicionários em json. Também, dentro das classes, criamos métodos para lidar com informações do banco, como o metodo de criptografia na parte da password.

No arquivo routes, estao definidas as rotas e as funções e metodos para interagir com 
o banco de dados.

O arquivo utils é um local para criarmos funções utilitarias que vamos utilizar dentro do pacote flask_app.

## TESTES

### RODAR OS TESTES
Para rodar os testes basta instalar o requirements.txt dentro dos testes, pode criar uma venv pra isso se quiser ou não. 

Após instalar o requirements.txt dos testes e com o terminal estando no caminho do projeto:
```git
pytest -s
```
Esse comando vai rodar todos os testes, ele le tudo que começar com "test" e roda. 
