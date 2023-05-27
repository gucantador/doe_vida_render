# BACKEND API


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
