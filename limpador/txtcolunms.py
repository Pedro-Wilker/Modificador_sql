import tkinter as tk
from tkinter import filedialog
import re

def limpar_txt(arquivo_txt, arquivo_txt_limpo):
    try:
        with open(arquivo_txt, 'r') as f:
            linhas = f.readlines()

        linhas_filtradas = []
        for linha in linhas:
            linha_strip = linha.strip()
            if not linha_strip.startswith('[') and \
               not linha_strip.startswith('#------------------------------------------------------------') and \
               'identificadores de colunas - FIM' not in linha_strip and \
               'identificador de tabela em' not in linha_strip:
                linhas_filtradas.append(linha)

        with open(arquivo_txt_limpo, 'w') as f:
            f.writelines(linhas_filtradas)

        print(f"Arquivo TXT limpo criado com sucesso: {arquivo_txt_limpo}")

    except FileNotFoundError:
        print(f"O arquivo {arquivo_txt} não foi encontrado.")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

def selecionar_arquivo():
    arquivo_txt = filedialog.askopenfilename(title="Selecione o arquivo TXT", filetypes=[("Arquivos TXT", "*.txt")])
    if arquivo_txt:
        arquivo_txt_limpo = filedialog.asksaveasfilename(title="Salvar arquivo TXT limpo como", defaultextension=".txt", filetypes=[("Arquivos TXT", "*.txt")])
        if arquivo_txt_limpo:
            limpar_txt(arquivo_txt, arquivo_txt_limpo)

# Interface gráfica
janela = tk.Tk()
janela.title("Limpador de TXT")
janela.geometry("300x150")

botao_selecionar = tk.Button(janela, text="Selecionar Arquivo TXT", command=selecionar_arquivo)
botao_selecionar.pack(pady=20)

janela.mainloop()