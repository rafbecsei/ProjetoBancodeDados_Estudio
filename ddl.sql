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
                 
