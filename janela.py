import tkinter as tk

janela = tk .Tk()
janela.title("EDA Com Hash")
janela.geometry("400x200")

#mensagem = tk.Label(janela, text="Bem-vindo ao programa!", #font=("Arial", 14), fg="green")
#mensagem.pack(pady=20)
#mensagem.pack(padx=(1, 40))

b_imagem = tk.Button(janela, text="GERAR IMAGEM")
b_imagem.pack(pady=20)

m_remover =  tk.Label(janela, text="Escola a celula que deseja remover")
m_remover.pack(pady=20)
m_remover.pack(padx=(1, 150))

opcoes = ["Opção 1", "Opção 2", "Opção 3"]
menu = tk.OptionMenu(janela, *opcoes, )
menu.pack(pady=10)

# Inicia o loop da interface
janela.mainloop()