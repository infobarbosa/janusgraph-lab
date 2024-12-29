#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
init_graph.py

Script para inicializar um cenário de exemplo no JanusGraph, envolvendo:
- 10 pessoas (com nomes em português)
- 5 empresas (também em português)
- 14 relacionamentos demonstrando vínculos de trabalho, sociedade, direção, família, etc.

Compatível com TinkerPop 3.6+ / 3.7+, pois:
 - Usa subtraversal anônima (__.V) ao criar edges
 - Força o uso de GraphSONSerializersV3d0() para evitar erros de serialização

Requisitos:
 - JanusGraph em execução (por exemplo, via Docker)
 - "gremlinpython" instalado na versão que corresponda ao TinkerPop do container
 - Ajustar GREMLIN_URL se não estiver em "ws://localhost:8182/gremlin"
"""

from gremlin_python.driver import client, protocol, serializer


GREMLIN_URL = "ws://localhost:8182/gremlin"

def get_gremlin_client():
    """
    Retorna um objeto Client para enviar queries Gremlin ao JanusGraph,
    usando GraphSON 3 ao invés de GraphBinary (para evitar problemas de serialização).
    """
    return client.Client(
        GREMLIN_URL,
        'g',
        message_serializer=serializer.GraphSONSerializersV3d0()
    )


def clear_all_data(gremlin_client):
    """
    Remove todos os vértices e arestas do grafo.
    """
    drop_query = "g.V().drop()"
    print("[INFO] Limpando todos os vértices e arestas do grafo...")
    gremlin_client.submit(drop_query).all().result()


def upsert_vertex(gremlin_client, label: str, key: str, value: str, **properties):
    """
    Cria (ou recupera se já existir) um vértice (label, key=value).
    Adiciona as demais propriedades. Retorna o ID do vértice.
    """
    query = (
        f"g.V().has('{label}', '{key}', '{value}')."
        f"fold()."
        f"coalesce(unfold(), addV('{label}').property('{key}', '{value}'))"
    )
    for prop_key, prop_value in properties.items():
        query += f".property('{prop_key}', '{prop_value}')"
    query += ".id()"

    result = gremlin_client.submit(query).all().result()
    return result[0]


def create_edge(gremlin_client, out_id, edge_label, in_id, **properties):
    """
    Cria uma aresta entre out_id -> in_id com o label edge_label.
    Usa subtraversal anônima (__.V) para compatibilidade com TinkerPop > 3.5.
    """
    query = (
        f"g.V('{out_id}')."
        f"addE('{edge_label}')."
        f"to(__.V('{in_id}'))"
    )
    for prop_key, prop_value in properties.items():
        query += f".property('{prop_key}', '{prop_value}')"

    gremlin_client.submit(query).all().result()


def main():
    # 1) Conecta ao Gremlin Server
    gremlin_client = get_gremlin_client()

    try:
        # 2) Limpa o grafo previamente (opcional, mas recomendável)
        clear_all_data(gremlin_client)

        # 3) Cria vértices de PESSOAS
        # ----------------------------------------------------------------------
        # label="pessoa", propriedade de unicidade = "nome"
        mario_id       = upsert_vertex(gremlin_client, "pessoa", "nome", "Mário Santos")
        juliana_id     = upsert_vertex(gremlin_client, "pessoa", "nome", "Juliana Ferreira")
        carla_id       = upsert_vertex(gremlin_client, "pessoa", "nome", "Carla Vieira")
        paulo_id       = upsert_vertex(gremlin_client, "pessoa", "nome", "Paulo Oliveira")
        rafaela_id     = upsert_vertex(gremlin_client, "pessoa", "nome", "Rafaela Andrade")
        bruno_id       = upsert_vertex(gremlin_client, "pessoa", "nome", "Bruno Correia")
        tania_id       = upsert_vertex(gremlin_client, "pessoa", "nome", "Tânia Silveira")
        lucas_id       = upsert_vertex(gremlin_client, "pessoa", "nome", "Lucas Dias")
        amanda_id      = upsert_vertex(gremlin_client, "pessoa", "nome", "Amanda Nunes")
        renata_id      = upsert_vertex(gremlin_client, "pessoa", "nome", "Renata Almeida")

        # 4) Cria vértices de EMPRESAS
        # ----------------------------------------------------------------------
        # label="empresa", propriedade de unicidade = "nome"
        techsolucoes_id    = upsert_vertex(gremlin_client, "empresa", "nome", "TechSoluções")
        supercomercio_id   = upsert_vertex(gremlin_client, "empresa", "nome", "SuperComércio")
        financeira_id      = upsert_vertex(gremlin_client, "empresa", "nome", "FinanceiraXYZ")
        agroverde_id       = upsert_vertex(gremlin_client, "empresa", "nome", "AgroVerde")
        construtora_id     = upsert_vertex(gremlin_client, "empresa", "nome", "ConstrutoraLopes")

        # 5) Cria relacionamentos (arestas)
        # ----------------------------------------------------------------------
        # Exemplo de 14 níveis (relacionamentos) inspirados no enunciado:

        # 1. Mário Santos trabalha para TechSoluções
        create_edge(gremlin_client, mario_id, "trabalha_para", techsolucoes_id)
        # 2. Juliana Ferreira é sócia da TechSoluções
        create_edge(gremlin_client, juliana_id, "e_socio_de", techsolucoes_id)
        # 3. Carla Vieira é sócia da TechSoluções
        create_edge(gremlin_client, carla_id, "e_socio_de", techsolucoes_id)
        # 4. Paulo Oliveira é sócio da SuperComércio
        create_edge(gremlin_client, paulo_id, "e_socio_de", supercomercio_id)
        # 5. Rafaela Andrade é diretora da SuperComércio
        create_edge(gremlin_client, rafaela_id, "e_diretor_de", supercomercio_id)
        # 6. Bruno Correia trabalha na SuperComércio
        create_edge(gremlin_client, bruno_id, "trabalha_para", supercomercio_id)
        # 7. Tânia Silveira trabalha para SuperComércio
        create_edge(gremlin_client, tania_id, "trabalha_para", supercomercio_id)
        # 8. Tânia Silveira é casada com Mário Santos (bidirecional)
        create_edge(gremlin_client, tania_id, "e_casado_com", mario_id)
        create_edge(gremlin_client, mario_id, "e_casado_com", tania_id)
        # 9. Amanda Nunes é filha de Mário Santos
        create_edge(gremlin_client, amanda_id, "e_filha_de", mario_id)
        # 10. Amanda Nunes trabalha para FinanceiraXYZ
        create_edge(gremlin_client, amanda_id, "trabalha_para", financeira_id)
        # 11. Paulo Oliveira é sócio da FinanceiraXYZ
        create_edge(gremlin_client, paulo_id, "e_socio_de", financeira_id)
        # 12. SuperComércio é sócia da FinanceiraXYZ
        create_edge(gremlin_client, supercomercio_id, "e_socio_de", financeira_id)
        # 13. AgroVerde é sócia da FinanceiraXYZ
        create_edge(gremlin_client, agroverde_id, "e_socio_de", financeira_id)
        # 14. TechSoluções tem contrato de prestação de serviços para a FinanceiraXYZ
        create_edge(gremlin_client, techsolucoes_id, "tem_contrato_com", financeira_id)

        # Exemplo adicional (se quiser expandir níveis de relacionamento):
        # 15. FinanceiraXYZ é sócia da ConstrutoraLopes
        # create_edge(gremlin_client, financeira_id, "e_socio_de", construtora_id)

        print("[INFO] Dados inseridos com sucesso no JanusGraph!")
    
    except protocol.GremlinServerError as e:
        print(f"[ERRO] Ocorreu um problema ao enviar consultas para o Gremlin Server: {e}")
    finally:
        # Fecha a conexão com o Gremlin Server
        gremlin_client.close()


if __name__ == "__main__":
    main()
