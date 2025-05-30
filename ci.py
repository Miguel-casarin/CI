# arrumar o codifo, melhorar organização
#usar variaveis globais
#implementar a legalização

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk 

class TabelaHash:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela =[[] for _ in range(tamanho)]
    
    def hash(self, chave):
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

class GerarImagem:
    def __init__(self, largura_total, altura_linha, num_linhas):
        self.largura_total = largura_total
        self.altura_linha = altura_linha
        self.num_linhas = num_linhas

    def desenhar(self, celulas_alocadas):
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, self.largura_total)
        ax.set_ylim(0, self.altura_linha * self.num_linhas)
        ax.set_xlabel('Largura (X)')
        ax.set_ylabel('Altura total')
        ax.set_title('Organização das células no circuito')

        # Desenhar cada célula como um retângulo
        for cel in celulas_alocadas:
            x = cel['x']
            y = cel['linha'] * self.altura_linha
            largura = cel['largura']
            altura = cel['altura']
            rect = patches.Rectangle(
                (x, y), largura, altura,
                linewidth=1, edgecolor='black', facecolor='red', alpha=0.7
            )
            ax.add_patch(rect)
            ax.text(x + largura / 2, y + altura / 2, cel['id'],
                    ha='center', va='center', fontsize=6, color='white')

        # Desenhar as 145 linhas horizontais
        for i in range(self.num_linhas + 1):
            y = i * self.altura_linha
            ax.hlines(y, 0, self.largura_total, colors='gray', linewidth=0.5, linestyles='--', alpha=0.7)

        # Remover linhas de grid verticais
        ax.grid(axis='y', linestyle='--', linewidth=0.5)

        plt.tight_layout()
        plt.show()

def ler_celulas(caminho):
    celulas = []
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
            celulas.append({'id': id_celula, 'largura': largura, 'altura': altura})
    return celulas

def alocar_celulas(organizador, celulas):
    celulas_alocadas = []
    for cel in celulas:
        pos = organizador.alocar_celula(cel['id'], cel['largura'], cel['altura'])
        if pos is not None:
            linha_aloc, x_aloc = pos
            celulas_alocadas.append({'id': cel['id'], 'x': x_aloc, 'linha': linha_aloc, 'largura': cel['largura'], 'altura': cel['altura']})
        else:
            print(f"Não foi possível alocar célula {cel['id']} (largura={cel['largura']})")
    return celulas_alocadas

class InterfaceTk:
    def __init__(self, master, organizador, celulas_alocadas, largura_total, altura_linha, num_linhas):
        self.master = master
        self.master.title("EDA Com Hash")
        self.master.geometry("700x500")

        self.organizador = organizador
        self.celulas_alocadas = celulas_alocadas
        self.largura_total = largura_total
        self.altura_linha = altura_linha
        self.num_linhas = num_linhas

        # Botão para gerar imagem
        self.b_imagem = tk.Button(master, text="GERAR IMAGEM", command=self.gerar_imagem)
        self.b_imagem.pack(pady=10)

        # Título para inserção de nova célula
        self.label_nova = tk.Label(master, text="Inserir nova célula:")
        self.label_nova.pack(pady=10)

        self.label_id = tk.Label(master, text="ID:")
        self.label_id.pack()
        self.entrada_id = tk.Entry(master)
        self.entrada_id.pack()

        self.label_largura = tk.Label(master, text="Largura:")
        self.label_largura.pack()
        self.entrada_largura = tk.Entry(master)
        self.entrada_largura.pack()

        self.label_altura = tk.Label(master, text="Altura:")
        self.label_altura.pack()
        self.entrada_altura = tk.Entry(master)
        self.entrada_altura.pack()

        self.botao_inserir = tk.Button(master, text="INSERIR CÉLULA", command=self.inserir_celula)
        self.botao_inserir.pack(pady=10)

        self.msg_insercao = tk.Label(master, text="", fg="blue")
        self.msg_insercao.pack()

        # Entrada para busca
        self.label_busca = tk.Label(master, text="Buscar célula por ID:")
        self.label_busca.pack()

        self.entrada_busca = tk.Entry(master)
        self.entrada_busca.pack(pady=5)

        self.botao_buscar = tk.Button(master, text="BUSCAR", command=self.buscar_celula)
        self.botao_buscar.pack(pady=5)

        self.resultado_busca = tk.Label(master, text="", fg="blue")
        self.resultado_busca.pack()


        # Mensagem para remoção
        self.m_remover = tk.Label(master, text="Escolha a célula que deseja remover")
        self.m_remover.pack(pady=5)
        self.m_remover.pack(padx=(1, 150))

        # Variável para opção selecionada
        self.opcoes = [cel['id'] for cel in celulas_alocadas]
        self.selecionado = tk.StringVar(master)
        if self.opcoes:
            self.selecionado.set(self.opcoes[0])
        else:
            self.selecionado.set('')

        # Menu de seleção
        self.menu = tk.OptionMenu(master, self.selecionado, *self.opcoes)
        self.menu.pack(pady=10)

        # Botão para remover célula selecionada
        self.b_remover = tk.Button(master, text="REMOVER CÉLULA", command=self.remover_celula)
        self.b_remover.pack(pady=10)

    def gerar_imagem(self):
        imagem = GerarImagem(self.largura_total, self.altura_linha, self.num_linhas)
        imagem.desenhar(self.celulas_alocadas)
    
    def inserir_celula(self):
        id_novo = self.entrada_id.get().strip()
        largura_txt = self.entrada_largura.get().strip()
        altura_txt = self.entrada_altura.get().strip()

        if not id_novo or not largura_txt or not altura_txt:
            self.msg_insercao.config(text="Preencha todos os campos!", fg="red")
            return

        try:
            largura = float(largura_txt)
            altura = float(altura_txt)
        except ValueError:
            self.msg_insercao.config(text="Largura e altura devem ser números!", fg="red")
            return

        pos = self.organizador.alocar_celula(id_novo, largura, altura)
        if pos is not None:
            linha_aloc, x_aloc = pos
            nova_celula = {
                'id': id_novo,
                'x': x_aloc,
                'linha': linha_aloc,
                'largura': largura,
                'altura': altura
            }
            self.celulas_alocadas.append(nova_celula)

            # Atualiza menu de remoção
            self.opcoes.append(id_novo)
            self.menu['menu'].add_command(label=id_novo, command=lambda v=id_novo: self.selecionado.set(v))
            self.selecionado.set(id_novo)

            self.msg_insercao.config(text=f"Célula '{id_novo}' inserida na linha {linha_aloc}, X={x_aloc}", fg="green")
        else:
            self.msg_insercao.config(text=f"Não foi possível alocar a célula '{id_novo}'", fg="red")
    
    def buscar_celula(self):
        id_celula = self.entrada_busca.get().strip()
        if not id_celula:
            self.resultado_busca.config(text="Digite um ID válido.", fg="red")
            return

        pos = self.organizador.tabela.buscar(id_celula)
        if pos is not None:
            linha, x = pos
            self.resultado_busca.config(
                text=f"Célula '{id_celula}' está na linha {linha}, posição X={x}", fg="green"
            )
        else:
            self.resultado_busca.config(
                text=f"Célula '{id_celula}' não encontrada.", fg="red"
            )


    def remover_celula(self):
        celula_id = self.selecionado.get()
        if not celula_id:
            return  # Nenhuma célula selecionada

        # Remove da tabela hash
        sucesso = self.organizador.tabela.remover(celula_id)
        if not sucesso:
            print(f"Célula {celula_id} não encontrada para remoção.")
            return

        # Remove da lista de células alocadas
        self.celulas_alocadas = [c for c in self.celulas_alocadas if c['id'] != celula_id]

        # Atualiza a lista das opções do menu
        self.opcoes = [cel['id'] for cel in self.celulas_alocadas]

        # Atualiza o menu
        menu = self.menu['menu']
        menu.delete(0, 'end')  # apaga opções antigas
        for opcao in self.opcoes:
            menu.add_command(label=opcao, command=lambda v=opcao: self.selecionado.set(v))

        # Atualiza valor selecionado
        if self.opcoes:
            self.selecionado.set(self.opcoes[0])
        else:
            self.selecionado.set('')

        print(f"Célula {celula_id} removida com sucesso.")



if __name__ == "__main__":
    arquivo = 'exemplo_bookshelf.nodes'
    largura_total = 2500
    altura_linha = 504
    num_linhas = 145

    organizador = Organizador(largura_total, altura_linha, num_linhas)
    celulas = ler_celulas(arquivo)
    celulas_alocadas = alocar_celulas(organizador, celulas)

    root = tk.Tk()
    app = InterfaceTk(root, organizador, celulas_alocadas, largura_total, altura_linha, num_linhas)
    root.mainloop()
