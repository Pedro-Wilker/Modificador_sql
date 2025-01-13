import json
import tkinter as tk
from tkinter import filedialog

def transformar_txt_em_json(arquivo_txt, arquivo_json):
    try:
        with open(arquivo_txt, 'r') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]

        tabelas = []
        for i in range(0, len(linhas), 2):
            if i + 1 < len(linhas):  
                antiga = linhas[i].split('|')[-1].strip()
                nova = linhas[i + 1].split('|')[-1].strip()
                tabela = {
                    "oldColumn": antiga,
                    "newColumn": nova
                }
                tabelas.append(tabela)
            else:
                print(f"Aviso: Linha {i} não tem par correspondente e será ignorada.")

        with open(arquivo_json, 'w') as f:
            json.dump(tabelas, f, indent=4, ensure_ascii=False)

        print(f"Arquivo JSON criado com sucesso: {arquivo_json}")

    except FileNotFoundError:
        print(f"O arquivo {arquivo_txt} não foi encontrado.")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

def selecionar_arquivo():
    arquivo_txt = filedialog.askopenfilename(title="Selecione o arquivo TXT", filetypes=[("Arquivos TXT", "*.txt")])
    if arquivo_txt:
        arquivo_json = filedialog.asksaveasfilename(title="Salvar arquivo JSON como", defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
        if arquivo_json:
            transformar_txt_em_json(arquivo_txt, arquivo_json)

# Interface gráfica
janela = tk.Tk()
janela.title("Conversor TXT para JSON")
janela.geometry("300x150")

botao_selecionar = tk.Button(janela, text="Selecionar Arquivo TXT", command=selecionar_arquivo)
botao_selecionar.pack(pady=20)

janela.mainloop()