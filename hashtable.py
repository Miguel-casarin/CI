# criando a tabela hash do zero

class TabelaHash:
    def __init__(self, tamanho = 100): # o valor do tamanho define o n de fun
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