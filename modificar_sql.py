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
    if not arquivo_selecionado:
        resultado_label.config(text="Por favor, selecione um arquivo.")
        return

    try:
        with open(arquivo_selecionado, 'r', encoding='utf-8') as arquivo_leitura, \
             open(arquivo_selecionado + '.tmp', 'w', encoding='utf-8') as arquivo_escrita:
            for linha in arquivo_leitura:
                # Substituir tanto o nome da tabela quanto quaisquer referências a ele
                nova_linha = re.sub(r"CREATE TABLE tab4226946692", "CREATE TABLE acaofiscal", linha, flags=re.IGNORECASE)
                nova_linha = re.sub(r"\btab4226946692\b", "acaofiscal", nova_linha, flags=re.IGNORECASE)
                arquivo_escrita.write(nova_linha)

        # Renomear o arquivo temporário para o nome original
        import os
        os.replace(arquivo_selecionado + '.tmp', arquivo_selecionado)

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

# Botão para selecionar o arquivo
botao_selecionar = tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo)
botao_selecionar.pack(pady=5)

# Botão para modificar o arquivo
botao_modificar = tk.Button(janela, text="Modificar Arquivo", command=modificar_arquivo)
botao_modificar.pack(pady=5)

# Label para mostrar resultado
resultado_label = tk.Label(janela, text="")
resultado_label.pack(pady=10)

# Iniciar loop da interface
janela.mainloop()