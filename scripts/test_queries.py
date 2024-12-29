#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_queries.py

Script para executar consultas de teste e verificar se os dados
inseridos pelo init_graph.py foram carregados conforme esperado.

Utiliza o mesmo padrão de conexão (GraphSONSerializersV3d0).
"""

from gremlin_python.driver import client, protocol, serializer

GREMLIN_URL = "ws://localhost:8182/gremlin"

def get_gremlin_client():
    """
    Retorna um objeto Client para enviar queries Gremlin ao JanusGraph,
    usando GraphSON v3 para maior compatibilidade.
    """
    return client.Client(
        GREMLIN_URL,
        'g',
        message_serializer=serializer.GraphSONSerializersV3d0()
    )


def run_query(gremlin_client, query):
    """
    Função auxiliar para executar uma string Gremlin e retornar a lista de resultados.
    """
    try:
        result_set = gremlin_client.submit(query)
        results = result_set.all().result()
        return results
    except protocol.GremlinServerError as e:
        print(f"[ERRO] Ocorreu um problema ao enviar a consulta para o Gremlin Server: {e}")
        return []


def test_queries(gremlin_client):
    """
    Executa algumas consultas para verificar:
     1. Quantidade total de vértices.
     2. Quantidade total de arestas.
     3. Todas as pessoas cadastradas.
     4. Todas as empresas cadastradas.
     5. Pessoas que trabalham em 'SuperComércio'.
     6. Sociedades da 'FinanceiraXYZ' (quem é sócio? quais empresas?).
     7. Relações familiares de 'Mário Santos' (filhos, cônjuges).
     8. Exemplo de caminho entre duas pessoas.
    """

    print("=== 1) Contagem de Vértices ===")
    query_1 = "g.V().count()"
    vertices_count = run_query(gremlin_client, query_1)
    print(f"Total de vértices: {vertices_count[0] if vertices_count else 'Erro ou vazio'}")
    print("")

    print("=== 2) Contagem de Arestas ===")
    query_2 = "g.E().count()"
    edges_count = run_query(gremlin_client, query_2)
    print(f"Total de arestas: {edges_count[0] if edges_count else 'Erro ou vazio'}")
    print("")

    print("=== 3) Todas as Pessoas (label='pessoa') ===")
    query_3 = "g.V().hasLabel('pessoa').values('nome')"
    people = run_query(gremlin_client, query_3)
    print("Pessoas encontradas:")
    for p in people:
        print(f" - {p}")
    print("")

    print("=== 4) Todas as Empresas (label='empresa') ===")
    query_4 = "g.V().hasLabel('empresa').values('nome')"
    companies = run_query(gremlin_client, query_4)
    print("Empresas encontradas:")
    for c in companies:
        print(f" - {c}")
    print("")

    print("=== 5) Pessoas que trabalham em 'SuperComércio' ===")
    query_5 = (
        "g.V().has('empresa','nome','SuperComércio')"
        ".in('trabalha_para')"
        ".values('nome')"
    )
    workers_supercomercio = run_query(gremlin_client, query_5)
    print("Quem trabalha para SuperComércio:")
    for w in workers_supercomercio:
        print(f" - {w}")
    print("")

    print("=== 6) Sociedades da 'FinanceiraXYZ' ===")
    query_6 = (
        "g.V().has('empresa','nome','FinanceiraXYZ')"
        ".in('e_socio_de')"
        ".values('nome')"
    )
    socios_financeira = run_query(gremlin_client, query_6)
    print("Pessoas/Empresas sócias da FinanceiraXYZ:")
    for s in socios_financeira:
        print(f" - {s}")
    print("")

    print("=== 7) Relações familiares de 'Mário Santos' ===")
    # Pegando todo mundo que tem aresta do tipo "e_filha_de" ou "e_casado_com"
    # onde Mário Santos é o target (in)
    query_7 = (
        "g.V().has('pessoa','nome','Mário Santos')"
        ".inE('e_filha_de','e_casado_com')"
        ".outV().values('nome')"
    )
    family_of_mario = run_query(gremlin_client, query_7)
    print("Familiares de Mário Santos:")
    for f in family_of_mario:
        print(f" - {f}")
    print("")

    print("=== 8) Exemplo de caminho entre duas pessoas (Carla Vieira e Bruno Correia) ===")
    # Vamos buscar caminhos até 4 saltos (apenas como teste)
    query_8 = (
        "g.V().has('pessoa','nome','Carla Vieira')"
        ".repeat(both().simplePath()).times(4)"
        ".has('pessoa','nome','Bruno Correia')"
        ".path()"
    )
    paths_carla_bruno = run_query(gremlin_client, query_8)
    if paths_carla_bruno:
        print("Caminhos encontrados (Carla Vieira -> Bruno Correia):")
        for path in paths_carla_bruno:
            # path é do tipo org.apache.tinkerpop.gremlin.structure.util.Path
            print(path)
    else:
        print("Nenhum caminho encontrado entre Carla Vieira e Bruno Correia (dentro de 4 saltos).")

    print("\n*** Testes finalizados ***")


def main():
    gremlin_client = get_gremlin_client()
    try:
        test_queries(gremlin_client)
    finally:
        gremlin_client.close()


if __name__ == "__main__":
    main()
