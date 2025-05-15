import tkinter as tk

# Função chamada quando o botão for clicado
def ao_clicar():
    print("Botão clicado!")

# Função chamada quando uma opção é selecionada no menu
def ao_selecionar(valor):
    print("Selecionado:", valor)

# Função chamada ao enviar texto do campo de entrada
def enviar_texto():
    texto = campo_entrada.get()
    print("Texto digitado:", texto)

# Cria a janela principal
janela = tk.Tk()
janela.title("Minha Janela Tkinter")
janela.geometry("720x560")

# Lista de opções
opcoes = ["Opção 1", "Opção 2", "Opção 3"]
selecionado = tk.StringVar(janela)
selecionado.set(opcoes[0])

# Menu de seleção
menu = tk.OptionMenu(janela, selecionado, *opcoes, command=ao_selecionar)
menu.pack(pady=10)

# Campo de digitação
campo_entrada = tk.Entry(janela, width=40)
campo_entrada.pack(pady=10)

# Botão para enviar texto digitado
botao_enviar = tk.Button(janela, text="Enviar Texto", command=enviar_texto)
botao_enviar.pack(pady=5)

# Botões adicionais
botao = tk.Button(janela, text="Clique aqui", command=ao_clicar)
botao.pack(pady=10)

b_gerar_imagem = tk.Button(janela, text="GERAR IMAGEM")
b_gerar_imagem.pack(pady=10)

# Loop da interface
janela.mainloop()
