def leitura(caminho):
    with open(caminho, 'r') as f:
        for i, linha in enumerate(f, start=1):
            linha = linha.strip()
            if not linha or linha.startswith('#') or ':' in linha:
                continue  # Ignora cabeçalho e metadados

            partes = linha.split()
            if len(partes) != 3:
                print(f"[Linha {i}] Ignorada (formato inválido): {linha}")
                continue

            try:
                id_celula = partes[0]
                largura = float(partes[1])
                altura = float(partes[2])
                print(f"ID: {id_celula}, Largura: {largura}, Altura: {altura}")
            except ValueError:
                print(f"[Linha {i}] Erro ao converter largura/altura: {linha}")


# Testando a função com o arquivo de exemplo
arquivo = 'exemplo_bookshelf.nodes'
leitura(arquivo)
