
# Janusgraph - Graph database demo
Author: Prof. Barbosa<br>
Contact: infobarbosa@gmail.com<br>
Github: [infobarbosa](https://github.com/infobarbosa)

## Objetivo
Avaliar de forma rudimentar o comportamento do modelo de armazenamento baseado em **grafos**.<br>
Para isso faremos uso do Janusgraph pela sua simplicidade e praticidade.

## Ambiente 
Este laborarório pode ser executado em qualquer estação de trabalho.<br>
Recomendo, porém, a execução em Linux.<br>
Caso não tenha uma estação de trabalho Linux à sua disposição, recomendo utilizar o AWS Cloud9. Para isso siga essas [instruções](Cloud9/README.md).

---

## 1. Visão Geral

Este laboratório demonstra como utilizar o JanusGraph, um banco de dados de grafos distribuído, em conjunto com Python para efetuar consultas e manipulações de um grafo de exemplo. O grafo criado representa um cenário de relacionamento entre **pessoas** e **empresas**, simulando situações de trabalho, sociedade, vínculos familiares, contratos de prestação de serviços, entre outros.

### 1.1 Pré-Requisitos

- **Docker** e **Docker Compose** instalados na máquina;
- **Python 3.8+** instalado (recomendado criar um ambiente virtual);
- Conhecimentos básicos de:
  - Conceitos de Grafos (vértices e arestas);
  - Noções de Docker (containers, rede interna, etc.);
  - Noções de Python (caso deseje explorar mais a fundo os scripts).

---

## 2. Subindo o Ambiente com Docker

1. **Clone** o repositório:
   ```bash
   git clone https://github.com/infobarbosa/janusgraph-lab.git
   ```

   ```bash
   cd janusgraph-lab
   ```

2. **Execute** o Docker Compose para subir o JanusGraph:
   ```bash
   docker-compose up -d
   ```

   Isso fará o download das imagens necessárias, criará e iniciará containers que incluem o JanusGraph e um servidor de Gremlin (porta padrão: 8182).

3. **Verifique** se o container do JanusGraph está em execução:
   ```bash
   docker ps
   ```

   Você deverá ver algo como `janusgraph-lab_janusgraph_1` em execução na porta `8182`.

---

## 3. Instalando Dependências Python

Dentro do diretório do repositório, existe um arquivo `requirements.txt` contendo as dependências para conexão ao JanusGraph via Python (por exemplo, a biblioteca `gremlinpython`).

1. Crie (opcional) e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux ou Mac
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

---

## 4. Executando o Script de Inicialização do Grafo

Para carregar os dados iniciais (pessoas, empresas e seus relacionamentos), execute:

```bash
python scripts/init_graph.py
```

Este script irá:
- Conectar no Gremlin Server do JanusGraph (no container Docker);
- Criar os vértices referentes a Pessoas e Empresas;
- Criar as arestas que representam os relacionamentos entre esses vértices.

> **Observação**: Caso deseje mudar o host/porta, ajuste no próprio `init_graph.py`, caso esteja executando em outra rede ou com mapeamentos diferentes.

---

## 5. Cenário de Exemplo (com pelo menos 10 níveis)

Abaixo está a descrição do cenário criado pelo `init_graph.py`. Foram usados **nomes reais em português** para as pessoas e empresas:

### 5.1 Pessoas
1. **Mário Santos**  
2. **Júlia Ferreira**  
3. **Carla Vieira**  
4. **Paulo Oliveira**  
5. **Rafaela Andrade**  
6. **Bruno Correia**  
7. **Tânia Silveira**  
8. **Lucas Dias**  
9. **Amanda Nunes**  
10. **Renata Almeida**  *(opcional para expandir ainda mais o cenário)*

### 5.2 Empresas
1. **TechSoluções**  
2. **SuperComércio**  
3. **FinanceiraXYZ**  
4. **AgroVerde**  
5. **ConstrutoraLopes**  *(opcional para expandir ainda mais o cenário)*

### 5.3 Relacionamentos (Exemplo de 14 níveis, atendendo aos “pelo menos 10”)

1. Mário Santos **trabalha para** TechSoluções  
2. Júlia Ferreira **é sócia de** TechSoluções  
3. Carla Vieira **é diretora da** TechSoluções  
4. Paulo Oliveira **é sócio da** SuperComércio  
5. Rafaela Andrade **é diretora da** SuperComércio  
6. Bruno Correia **trabalha para** SuperComércio  
7. Tânia Silveira **trabalha para** SuperComércio  
8. Tânia Silveira **é casada com** Mário Santos  
9. Amanda Nunes **é filha de** Mário Santos  
10. Amanda Nunes **trabalha para** FinanceiraXYZ  
11. Paulo Oliveira **é sócio da** FinanceiraXYZ  
12. SuperComércio **é sócia da** FinanceiraXYZ  
13. AgroVerde **é sócia da** FinanceiraXYZ  
14. TechSoluções **tem contrato de prestação de serviços com** FinanceiraXYZ  

Esses relacionamentos permitem explorar desde consultas mais simples (quem trabalha em qual empresa) até consultas mais avançadas (cadeias de relacionamento que chegam a 2, 3 ou mais “saltos”).

---

## 6. Exercício Básico

O **objetivo** deste primeiro exercício é confirmar que o ambiente está funcionando corretamente e que você sabe executar consultas simples via Gremlin.

### 6.1 Tarefa

1. Abra um terminal e execute o Gremlin Console dentro do container (para ter certeza de que está tudo no ar). Você pode fazer isso de duas formas:
   - Via docker exec:
     ```bash
     docker exec -it janusgraph-lab_janusgraph_1 bash
     ```
     E depois rodar dentro do container:
     ```bash
     /opt/janusgraph/bin/gremlin.sh
     ```
   - Ou então conectar-se de modo remoto com o Gremlin Console instalado localmente (ajuste o host se necessário).

2. Liste **todas as pessoas** que trabalham em “SuperComércio”. Exemplo de consulta Gremlin:
   ```groovy
   g.V().has('empresa', 'nome', 'SuperComércio').
         in('trabalha_para').
         values('nome')
   ```
   > Observe que, dependendo de como o `init_graph.py` criou os labels de aresta e propriedades, o nome exato do label pode variar. Ajuste conforme necessário.

3. Liste **todas as empresas** em que “Mário Santos” trabalha ou é sócio/diretor (neste cenário, Mário Santos só trabalha em TechSoluções, mas fica como exemplo de query).

#### 6.2 Validação

- Se você conseguiu **listar** as pessoas que trabalham em “SuperComércio” e ver **Mário Santos** em “TechSoluções” corretamente, parabéns! Seu ambiente está configurado e funcional.

---

## 7. Exercício Avançado

Agora vamos explorar o potencial do JanusGraph com consultas que envolvem múltiplos relacionamentos em cadeia.

### 7.1 Tarefa

1. Usando queries Gremlin, descubra **todas as empresas** que se relacionam (são sócias, trabalham, têm contratos, etc.) com a empresa “FinanceiraXYZ” em até **dois níveis** de distância. Em outras palavras, queremos encontrar:
   - Empresas **diretamente** ligadas à FinanceiraXYZ (por sociedade, contrato, etc.);
   - Empresas e pessoas **indiretamente** ligadas por até um intermediário.

2. Verifique **quais pessoas** que tenham qualquer tipo de vínculo com “FinanceiraXYZ” podem também ter outro vínculo com “TechSoluções”. Este tipo de query é interessante para detectar, por exemplo, **conflitos de interesse** ou relacionamentos cruzados.

3. Localize **todos os caminhos** que ligam “Mário Santos” a “Paulo Oliveira”. Note que eles podem se cruzar por:
   - Uma empresa em comum,
   - Um vínculo familiar,
   - Ou ambos!

> Dica: Para buscar caminhos e explorar relacionamentos, você pode usar passos como `.repeat()`, `.until()`, `.bothE()`, entre outros.

### 7.2 Possíveis Consultas Exemplo

```groovy
// 1) Quem se relaciona com a FinanceiraXYZ em até dois saltos?
g.V().has('empresa','nome','FinanceiraXYZ').
      bothE().otherV(). // Um salto
      bothE().otherV(). // Dois saltos
      dedup().
      values('nome')

// 2) Relações cruzadas FinanceiraXYZ e TechSoluções
g.V().has('empresa','nome','FinanceiraXYZ').
      bothE().otherV().
      where(
        bothE().otherV().has('empresa','nome','TechSoluções')
      ).
      dedup().
      values('nome')

// 3) Caminhos entre Mário Santos e Paulo Oliveira
g.V().has('pessoa','nome','Mário Santos').
      repeat(both().simplePath()).
      until(has('pessoa','nome','Paulo Oliveira')).
      path()
```

Você pode adaptar os nomes de labels (`pessoa`, `empresa`, `trabalha_para`, `é_sócio_de`, etc.) conforme os criados no `init_graph.py`.

#### 7.3 Validação

- Se você conseguiu **identificar** as empresas e pessoas associadas a **FinanceiraXYZ** em até 2 saltos, listou possíveis relacionamentos cruzados com **TechSoluções** e descobriu **pelo menos um caminho** que liga “Mário Santos” a “Paulo Oliveira”, o exercício avançado está completo.

---

## 8. Conclusão

Com esses dois exercícios (básico e avançado), você:
- Validou que o **ambiente Docker** e o **JanusGraph** estão funcionando;
- Praticou **consultas Gremlin** básicas (ex. listagens diretas) e mais complexas (até 2 saltos, caminhos, etc.);
- Observou como **relacionamentos** de grafos podem facilmente expandir e permitir análises de cadeia de vínculos entre pessoas e empresas, algo muito útil em diversos contextos reais (compliance, fraudes, CRMs avançados, cadastros complexos, etc.).

---

### Próximos Passos

- **Explorar índices** no JanusGraph para melhorar a performance de consultas;
- Integrar a base com **SGBDs distribuídos** como Cassandra ou HBase (possibilidades do JanusGraph);
- Criar **pipelines** de ingestão de dados (ETL) para grafos;
- Estudar **visualização** de grafos (por exemplo, soluções como Gephi, Bloom, KeyLines ou plugins do próprio JanusGraph).

---

## Referências

- [Documentação Oficial do JanusGraph](https://janusgraph.org/)
- [Gremlin Language Reference](https://tinkerpop.apache.org/gremlin.html)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

**Bom aprendizado e boas explorações em Grafos!**