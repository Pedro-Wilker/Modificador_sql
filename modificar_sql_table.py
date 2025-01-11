import tkinter as tk
from tkinter import filedialog
import re

def selecionar_arquivo():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos SQL", "*.sql")])
    if file_path:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, file_path)

def modificar_arquivo():
    arquivo_selecionado = entrada_arquivo.get()
    tabela_antiga = entrada_tabela_antiga.get()
    tabela_nova = entrada_tabela_nova.get()

    if not arquivo_selecionado or not tabela_antiga or not tabela_nova:
        resultado_label.config(text="Por favor, preencha todos os campos.")
        return

    try:
        with open(arquivo_selecionado, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()

        # Substituir o nome da tabela
        novo_conteudo = re.sub(r"CREATE TABLE\s+" + re.escape(tabela_antiga), 
                               "CREATE TABLE " + tabela_nova, conteudo, flags=re.IGNORECASE)

        # Gravar o novo conteúdo no arquivo
        with open(arquivo_selecionado, 'w', encoding='utf-8') as arquivo:
            arquivo.write(novo_conteudo)

        resultado_label.config(text="Arquivo SQL atualizado com sucesso.")
    except UnicodeDecodeError:
        resultado_label.config(text="Erro ao ler o arquivo. Tente usar uma codificação diferente.")
    except Exception as e:
        resultado_label.config(text=f"Erro ao atualizar o arquivo: {str(e)}")

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Modificador de Arquivo SQL")

# Widget para entrada do caminho do arquivo
entrada_arquivo = tk.Entry(janela, width=50)
entrada_arquivo.pack(pady=10)

botao_selecionar = tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo)
botao_selecionar.pack(pady=5)

# Entrada para o nome da tabela antiga
tk.Label(janela, text="Nome da tabela antiga:").pack()
entrada_tabela_antiga = tk.Entry(janela)
entrada_tabela_antiga.pack()

# Entrada para o novo nome da tabela
tk.Label(janela, text="Novo nome da tabela:").pack()
entrada_tabela_nova = tk.Entry(janela)
entrada_tabela_nova.pack()

# Botão para modificar o arquivo
botao_modificar = tk.Button(janela, text="Modificar Arquivo", command=modificar_arquivo)
botao_modificar.pack(pady=5)

# Label para mostrar resultado
resultado_label = tk.Label(janela, text="")
resultado_label.pack(pady=10)

# Iniciar loop da interface
janela.mainloop()