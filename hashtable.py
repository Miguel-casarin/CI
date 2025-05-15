# criando a tabela hash do zero

class TabelaHash:
    def __init__(self, tamanho): # o valor do tamanho define o n de fun
        self.tamanho = tamanho
        self.tabela = [[] for _ in range(tamanho)] # lista de buckets

    def hash(self, chave): # vou definir a minha função hash aqui
        pass

    def inserir(self, chave, valor):
        indice = self.hash(chave)

         # Verifica se a chave já existe, e atualiza
        for i, (k, v) in enumerate(self.tabela[indice]):
            if k == chave:
                self.tabela[indice][i] = (chave, valor)
                return
        # Senão, adiciona nova tupla
        self.tabela[indice].append((chave, valor))

    def buscar(self, chave):
        indice = self.hash(chave)
        for k, v in self.tabela[indice]:
            if k == chave:
                return v
        
        return None # caso nao for encontrada
    
    def remover(self, chave):
        indice = self.hash(chave)
        for i, (k, v) in enumerate(self.tabela[indice]):
            if k == chave:
                del self.tabela[indice][i]
                return True
        return False  # Não encontrada

class Organizador:
    def __init__(self, largura_l = 0, altura_l = 0, num_linhas = 0):
        self.largura_l = largura_l
        self.altura_l = altura_l
        self.num_l = num_linhas
        self.linhas = [0.0] * num_linhas  # largura ocupada por linha
        self.tabela = TabelaHash(2000)    # hash por ID da célula

    def alocar_célula(self, id_célula, largura, altura):
        for i in range(self.num_l):
            if altura == self.altura_l:
                if self.linhas[i] + largura <= self.largura_l:
                    x = self.linhas[i]
                    self.tabela.inserir(id_célula, (i, x))  # salva (linha, posição x)
                    self.linhas[i] += largura
                    return (i, x)   

def leitura(caminho):
    with open(caminho, 'r') as f:
        for i, linha in enumerate(f, start=1):
            linha = linha.strip()

            if not linha or linha.startswith('#') or ':' in linha:
                continue  # Ignora comentários e cabeçalho

            partes = linha.split()
            if len(partes) != 3:
                print(f"[Linha {i}] Ignorada (formato inválido): {linha}")
                continue

            # Verifica se as partes 1 e 2 são números válidos
            if not (partes[1].replace('.', '', 1).isdigit() and partes[2].replace('.', '', 1).isdigit()):
                print(f"[Linha {i}] Ignorada (valores não numéricos): {linha}")
                continue

            id_celula = partes[0]
            largura = float(partes[1])
            altura = float(partes[2])
            


# vou ter uma hash armazenando as posições livres e outra as ocupada
Celulas_fixas = TabelaHash(tamanho=0)
celulas_variaveis = TabelaHash(tamanho=0)

arquivo = 'exemplo_bookshelf.nodes'

