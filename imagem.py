import matplotlib.pyplot as plt
import matplotlib.patches as patches

class TabelaHash:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela = [[] for _ in range(tamanho)]

    def hash(self, chave):
        # Função hash simples para strings
        return sum(ord(c) for c in chave) % self.tamanho

    def inserir(self, chave, valor):
        indice = self.hash(chave)
        for i, (k, v) in enumerate(self.tabela[indice]):
            if k == chave:
                self.tabela[indice][i] = (chave, valor)
                return
        self.tabela[indice].append((chave, valor))

    def buscar(self, chave):
        indice = self.hash(chave)
        for k, v in self.tabela[indice]:
            if k == chave:
                return v
        return None
    
    def remover(self, chave):
        indice = self.hash(chave)
        for i, (k, v) in enumerate(self.tabela[indice]):
            if k == chave:
                del self.tabela[indice][i]
                return True
        return False

class Organizador:
    def __init__(self, largura_l, altura_l, num_linhas):
        self.largura_l = largura_l
        self.altura_l = altura_l
        self.num_l = num_linhas
        self.linhas = [0.0] * num_linhas  # largura ocupada por linha
        self.tabela = TabelaHash(2000)    # hash por ID da célula

    def alocar_celula(self, id_celula, largura, altura):
        if altura != self.altura_l:
            return None  # ignora células com altura diferente
        for i in range(self.num_l):
            if self.linhas[i] + largura <= self.largura_l:
                x = self.linhas[i]
                self.tabela.inserir(id_celula, (i, x))  # salva (linha, posição x)
                self.linhas[i] += largura
                return (i, x)
        return None  # não coube em nenhuma linha

def leitura_e_alocacao(caminho, organizador):
    celulas_alocadas = []
    with open(caminho, 'r') as f:
        for i, linha in enumerate(f, start=1):
            linha = linha.strip()
            if not linha or linha.startswith('#') or ':' in linha:
                continue
            partes = linha.split()
            if len(partes) != 3:
                print(f"[Linha {i}] Ignorada (formato inválido): {linha}")
                continue
            if not (partes[1].replace('.', '', 1).isdigit() and partes[2].replace('.', '', 1).isdigit()):
                print(f"[Linha {i}] Ignorada (valores não numéricos): {linha}")
                continue
            id_celula = partes[0]
            largura = float(partes[1])
            altura = float(partes[2])
            pos = organizador.alocar_celula(id_celula, largura, altura)
            if pos is not None:
                linha_aloc, x_aloc = pos
                celulas_alocadas.append({'id': id_celula, 'x': x_aloc, 'linha': linha_aloc, 'largura': largura, 'altura': altura})
            else:
                print(f"[Linha {i}] Não foi possível alocar célula {id_celula} (largura={largura})")
    return celulas_alocadas

def gerar_imagem(celulas, largura_total=2500, altura_linha=504, num_linhas=145):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, largura_total)
    ax.set_ylim(0, altura_linha * num_linhas)
    ax.set_xlabel('Largura (X)')
    ax.set_ylabel('Altura total')
    ax.set_title('Organização das células no circuito')

    # Desenha as células
    for cel in celulas:
        x = cel['x']
        y = cel['linha'] * altura_linha
        largura = cel['largura']
        altura = cel['altura']
        rect = patches.Rectangle((x, y), largura, altura, linewidth=1, edgecolor='black', facecolor='red', alpha=0.7)
        ax.add_patch(rect)
        ax.text(x + largura / 2, y + altura / 2, cel['id'], ha='center', va='center', fontsize=6, color='white')

    # Remove grid vertical
    ax.grid(axis='y', linestyle='--', linewidth=0.5)  # só linhas horizontais no grid (opcional)

    # Desenha as 145 linhas horizontais explicitamente
    for i in range(num_linhas + 1):
        y = i * altura_linha
        ax.hlines(y, 0, largura_total, colors='gray', linewidth=0.5, linestyles='--', alpha=0.7)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    arquivo = 'exemplo_bookshelf.nodes'  # seu arquivo nodes
    organizador = Organizador(largura_l=2500, altura_l=504, num_linhas=145)
    celulas = leitura_e_alocacao(arquivo, organizador)
    gerar_imagem(celulas, largura_total=2500, altura_linha=504)
