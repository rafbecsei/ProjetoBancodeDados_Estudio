from faker import Faker
from faker.providers import DynamicProvider
from random import randint
import psycopg2
from dotenv import load_dotenv
import os

fake = Faker('pt_BR')
fake2 = Faker('en_US')

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

#Providers do faker
sexo = DynamicProvider(
    provider_name = "sexo_provider", elements = ["feminino","masculino"]
)
categoria = DynamicProvider(
    provider_name = "categoria_provider", elements = ["set","executivo","elenco","objetos"]
)
genero = DynamicProvider(
    provider_name = "genero_provider", elements = [ 
    "Ação",
    "Aventura",
    "Comédia",
    "Drama",
    "Fantasia",
    "Ficção Científica",
    "Terror",
    "Suspense",
    "Mistério",
    "Animação",
    "Romance",
    "Musical",
    "Documentário",
    "Biografia",
    "Guerra",
    "Policial",
    "Faroeste",
    "Histórico",
    "Esporte",
    "Crime"
])

fake.add_provider(sexo)
fake.add_provider(categoria)
fake.add_provider(genero)

#Funções ligadas ao banco
def insercao(dicionario, tabela): #função para inserção de dados no banco de dados. Virou função para ter mais reusabilidade sem sujar o código inteiro. TEM QUE ESTAR DEPOIS DA CONEXÃO COM O BANCO. 
        """
        Inserção dos dados vindos de um dicionário para dentro do banco de dados.

        Args:
            dicionario(string): dicionario do qual serão retiradas as informações para inserir no banco de dados
            tabela(string): nome da coluna da tabela do banco de dados na qual serão inseridos os dados do dicionário 

        Returns:
        nada kkkkkkk
        """
        tabelaNome = tabela #tabela na qual as informações serão inseridas
        query = "INSERT INTO " + tabelaNome + "("  #começo da query
        query1 = "" #query com todas as colunas
        query2 = "" #query com todos os valores que serão inseridos
        for chave, valor in dicionario.items(): #navegar pelo dicionario para adicionar os nomes e valores à query
            query1+=   chave + "," #string das colunas exemplo: nome,id,departamento,RA,
            query2+= "'" + valor + "'" + "," #string dos valores | exemplo: jeremias,1234,robotica,24.123.035-8
        query1 = query1.rstrip(",") # tira a última vírgula da string | exemplo: ANTES: nome,id,departamento,RA,  DEPOIS: nome,id,departamento,RA
        query2 = query2.rstrip(",") #mesma coisa do comentário acima(linha 48)

        print(query1) #imprimir cada parte da query para ver como está 
        print(query2)
        query+= query1 + ") VALUES ("  #final da parte INSERT INTO tabela(coluna1,coluna2,coluna3) e começo da inserção dos valores
        query+= query2 + ")" #inserção dos valores na query e fechamento de parenteses do VALUES()
        print(query) #imprimir query completa para checar

    

        cursor.execute(query) #execução da query para inserir no banco de dados 
        cursor.execute("commit") # confirmação da alteração no banco de dados 
def resetarDB():
        cursor.execute('ALTER TABLE filme DROP CONSTRAINT IF EXISTS id;')
        tabelas = [
        'gravacao',
        'elenco',
        'filme',
        'producao',
        'roteirista',
        'diretor',
        'produtor',
        'ator'
        ]
        for tabela in tabelas:
            cursor.execute(f'DROP TABLE IF EXISTS {tabela} CASCADE;')
        cursor.execute("commit")
def criarDB():
     cursor.execute("""
        create table ator(
            id varchar(10)
            ,nome varchar(30)
            ,sexo varchar(10)
            ,idade varchar(3)
            ,primary key (id)
        );

        create table produtor(
            id varchar(10)
            ,nome varchar(30)
            ,sexo varchar(10)
            ,idade varchar(3)
            ,categoria varchar(30)
            ,primary key (id)
        );

        create table diretor(
            id varchar(10)
            ,nome varchar(30)
            ,sexo varchar(10)
            ,idade varchar(3)
            ,primary key (id)
        );

        create table roteirista(
            id varchar(10)
            ,nome varchar(30)
            ,sexo varchar(10)
            ,idade varchar(3)
            ,primary key (id)
        );

        create table producao(
            id varchar(10)
            ,id_set varchar(10)
            ,id_executivo varchar(10)
            ,id_elenco varchar(10)
            ,id_objetos varchar(10)
            ,primary key (id)
            ,foreign key (id_set) references produtor(id)
            ,foreign key (id_executivo) references produtor(id)
            ,foreign key (id_elenco) references produtor(id)
            ,foreign key (id_objetos) references produtor(id)
        );

        create table filme(
            id varchar(10)
            ,genero varchar(30)
            ,nome varchar(30)
            ,ano_lancamento varchar(4)
            ,tempo varchar(3)
            ,id_producao varchar(10)
            ,id_diretor varchar(10)
            ,id_roteirista varchar(10)
            --,id_sequencia varchar(10)
            ,primary key (id)
            ,foreign key (id_producao) references producao(id)
            ,foreign key (id_diretor) references diretor(id)
            ,foreign key (id_roteirista) references roteirista(id)
        );

        create table elenco(
            id_filme varchar(10)
            ,id_ator varchar(10)
            ,foreign key (id_filme) references filme(id)
            ,foreign key (id_ator) references ator(id)
        );
                    
    """)
     cursor.execute("commit")

#Funções para gerar os dados
def gerarAtores(n):
    atores = []
    nomes = []
    ids = []
    for i in range(n):
        aux = 1
        sexo = fake.sexo_provider()
        if sexo == "feminino":
            n1 = fake.first_name_female()
        else:
            n1 = fake.first_name_male()
        n2 = fake.last_name()
        nome = n1 + " " + n2
        while aux == 1:
            if nome in nomes:
                if sexo == "feminino":
                    n1 = fake.first_name_female()
                else:
                    n1 = fake.first_name_male()
                n2 = fake.last_name()
                nome = n1 + " " + n2
            else:
                aux = 0
        aux = 1
        id = fake.numerify(text='AT%%%')
        while aux == 1:
            if id in ids:
                id = fake.numerify(text='AT%%%')
            else:
                aux = 0
        idade = randint(18,75)
        ator = {"id": id, "nome": nome, "sexo": sexo, "idade": str(idade)}
        ids.append(id)
        nomes.append(nome)
        atores.append(ator)
    return atores

def gerarProdutor(n):
    produtores = []
    nomes = []
    ids = []
    categorias = []
    for i in range(n):
        aux = 1
        id = fake.numerify(text='PR%%%')
        while aux == 1:
            if id in ids:
                id = fake.numerify(text='PR%%%')
            else:
                aux = 0
        idade = randint(25,75)
        aux = 1
        sexo = fake.sexo_provider()
        if sexo == "feminino":
            n1 = fake.first_name_female()
        else:
            n1 = fake.first_name_male()
        n2 = fake.last_name()
        nome = n1 + " " + n2
        while aux == 1:
            if nome in nomes:
                if sexo == "feminino":
                    n1 = fake.first_name_female()
                else:
                    n1 = fake.first_name_male()
                n2 = fake.last_name()
                nome = n1 + " " + n2
            else:
                aux = 0
        
        categoria = fake.categoria_provider()
        aux = 1
        while aux == 1:
            if categoria in categorias:
                categoria = fake.categoria_provider()
            else:
                aux = 0
        categorias.append(categoria)
        if len(categorias) == 4:
            categorias.clear()
        produtor = {"id": id, "nome": nome, "sexo": sexo, "idade": str(idade), "categoria": categoria}
        ids.append(id)
        nomes.append(nome)
        produtores.append(produtor)
    return produtores
        
def gerarDiretores(n):
    diretores=[]
    nomes=[]
    sexo=[]
    ids=[]
    for i in range(n):
        aux = 1
        sexo = fake.sexo_provider()
        if sexo == "feminino":
            n1 = fake.first_name_female()
        else:
            n1 = fake.first_name_male()
        n2 = fake.last_name()
        nome = n1 + " " + n2
        while aux == 1:
            if nome in nomes:
                if sexo == "feminino":
                    n1 = fake.first_name_female()
                else:
                    n1 = fake.first_name_male()
                n2 = fake.last_name()
                nome = n1 + " " + n2
            else:
                aux = 0
        aux = 1
        id = fake.numerify(text='DR%%%')
        while aux == 1:
            if id in ids:
                id = fake.numerify(text='DR%%%')
            else:
                aux = 0
        idade = randint(35,75)
        diretor = {"id": id, "nome": nome, "sexo": sexo, "idade": str(idade)}
        ids.append(id)
        nomes.append(nome)
        diretores.append(diretor)
    return diretores

def gerarRoteiristas(n):
    roteiristas=[]
    nomes=[]
    sexo=[]
    ids=[]
    for i in range(n):
        aux = 1
        sexo = fake.sexo_provider()
        if sexo == "feminino":
            n1 = fake.first_name_female()
        else:
            n1 = fake.first_name_male()
        n2 = fake.last_name()
        nome = n1 + " " + n2
        while aux == 1:
            if nome in nomes:
                if sexo == "feminino":
                    n1 = fake.first_name_female()
                else:
                    n1 = fake.first_name_male()
                n2 = fake.last_name()
                nome = n1 + " " + n2
            else:
                aux = 0
        aux = 1
        id = fake.numerify(text='RT%%%')
        while aux == 1:
            if id in ids:
                id = fake.numerify(text='RT%%%')
            else:
                aux = 0
        idade = randint(35,75)
        roteirista = {"id": id, "nome": nome, "sexo": sexo, "idade": str(idade)}
        ids.append(id)
        nomes.append(nome)
        roteiristas.append(roteirista)
    return roteiristas

def gerarProducao(id,set,executivo,elenco,objetos):
    producao = {"id": id, "id_set": set, "id_executivo": executivo, "id_elenco": elenco, "id_objetos": objetos}
    return producao

def gerarElenco(filme,ator):
    elenco = {"id_filme": filme, "id_ator": ator}
    return elenco

def gerarFilme(n):
    filmes = []
    ids = []
    for i in range(n):
        aux = 1 
        id = fake.numerify(text='%%%')
        while aux == 1:
            if id in ids:
                id = fake.numerify(text='%%%')
            else:
                aux = 0
        ids.append(id)
        genero = fake.genero_provider()
        ano = randint(2000,2025)
        n1 = fake2.word()
        n2 = fake2.word()
        n1 = n1.capitalize()
        n2 = n2.capitalize()
        nome = n1 + " " + n2
        tempo = randint(40,240)
        filme = {"id": id, "genero": genero, "nome": nome, "ano_lancamento": str(ano), "tempo": str(tempo), "id_producao": None, "id_diretor": None, "id_roteirista": None}
        filmes.append(filme)
    return filmes

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    ) #dados para conseguir conectar com o banco de dados (usar arquivo .env)
    print("Connection successful!")
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)
    
    #main
    resetarDB()
    criarDB()

    n = randint(20,30)
    atores = gerarAtores(6*n)
    for ator in atores:
         insercao(ator,"ator")
    
    diretores = gerarDiretores(n - 6)
    for diretor in diretores:
        insercao(diretor,"diretor")
    
    roteiristas = gerarRoteiristas(n - 4)
    for roteirista in roteiristas:
        insercao(roteirista,"roteirista")
    
    produtores = gerarProdutor(4*n)
    for produtor in produtores:
        insercao(produtor,"produtor")

    psets = []
    pexecutivos = []
    pelencos = []
    pobjetos = []
    for i in range(len(produtores)):
        if produtores[i]["categoria"] == "set":
            psets.append(produtores[i]["id"])
        elif produtores[i]["categoria"] == "executivo":
            pexecutivos.append(produtores[i]["id"])
        elif produtores[i]["categoria"] == "elenco":
            pelencos.append(produtores[i]["id"])
        elif produtores[i]["categoria"] == "objetos":
            pobjetos.append(produtores[i]["id"])

    producoes = []
    laux = []
    for i in range(n):
        r = randint(0,len(psets) - 1)  
        aux = 1
        id = fake.numerify(text='P-%%%')
        while aux == 1:
            if id in laux:
                id = fake.numerify(text='P-%%%')
            else:
                aux = 0
        laux.append(id)
        producao = gerarProducao(id,psets[r],pexecutivos[r],pelencos[r],pobjetos[r])
        producoes.append(producao)
    laux.clear()

    for producao in producoes:
        insercao(producao,"producao")

    lr = []
    ld = []
    filmes = gerarFilme(n)
    for i in range(len(filmes)):
        filmes[i]["id_producao"] = producoes[i]["id"]
        r = randint(0, len(roteiristas)-1)
        rot = roteiristas[r]["id"]
        if len(lr) != len(roteiristas):
            aux = 1
            while aux == 1:
                if rot in lr:
                    r = randint(0, len(roteiristas)-1)
                    rot = roteiristas[r]["id"]
                else: 
                    aux = 0
            lr.append(rot)
        filmes[i]["id_roteirista"] = rot

        r = randint(0, len(diretores)-1)
        dir = diretores[r]["id"]
        if len(ld) != len(diretores):
            aux = 1
            while aux == 1:
                if dir in ld:
                    r = randint(0, len(diretores)-1)
                    dir = diretores[r]["id"]
                else: 
                    aux = 0
            ld.append(dir)
        filmes[i]["id_diretor"] = dir

    for filme in filmes:
        insercao(filme,"filme")

    laux.clear()
    elencos = []
    for i  in range(len(filmes)):
        filme = filmes[i]["id"]
        laux2 = []
        for j in range(randint(4,8)):
            r = randint(0,len(atores)-1)
            ator = atores[r]["id"]
            if len(laux) < len(atores):
                aux = 0
                while aux == 0:
                    if ator in laux:
                        r = randint(0,len(atores)-1)
                        ator = atores[r]["id"]
                    elif ator in laux2:
                        r = randint(0,len(atores)-1)
                        ator = atores[r]["id"]
                    else:
                        aux = 1
            aux = 0
            while aux == 0:
                if ator in laux2:
                    r = randint(0,len(atores)-1)
                    ator = atores[r]["id"]
                else:
                    aux = 1
            laux.append(ator)
            elenco = gerarElenco(filme,ator)
            elencos.append(elenco)
    for elenco in elencos:
        insercao(elenco, "elenco")


    
    
    cursor.close() #sem cursor
    connection.close() #fim da conexão com o banco de dados 
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
