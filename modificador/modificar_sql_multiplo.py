import tkinter as tk
from tkinter import filedialog
import re
import json

def selecionar_arquivo():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos SQL", "*.sql")])
    if file_path:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, file_path)

def selecionar_json():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos JSON", "*.json")])
    if file_path:
        entrada_json.delete(0, tk.END)
        entrada_json.insert(0, file_path)
        exibir_dados_json(file_path)

def exibir_dados_json(path):
    try:
        with open(path, 'r') as json_file:
            tabelas = json.load(json_file)
            if isinstance(tabelas, list):  # Verifica se é uma lista
                # Exibir apenas os 20 primeiros itens
                dados_json.set("\n".join([f"{t['oldTable']} -> {t['newTable']}" for t in tabelas[:20]]))
                if len(tabelas) > 20:
                    dados_json.set(dados_json.get() + "\n... (mais itens)")
            else:
                dados_json.set("Erro: O JSON deve ser uma lista de dicionários.")
    except json.JSONDecodeError:
        dados_json.set("Erro: JSON inválido.")
    except KeyError:
        dados_json.set("Erro: Formato JSON incorreto. Verifique os nomes dos campos.")
    except Exception as e:
        dados_json.set(f"Erro ao ler JSON: {str(e)}")

def modificar_arquivo():
    arquivo_sql = entrada_arquivo.get()
    arquivo_json = entrada_json.get()
    
    if not arquivo_sql or not arquivo_json:
        resultado_label.config(text="Por favor, selecione ambos os arquivos.")
        return

    resultado_label.config(text="Carregando...")

    try:
        with open(arquivo_json, 'r') as json_file:
            tabelas = json.load(json_file)
        if not isinstance(tabelas, list):
            raise ValueError("O JSON deve ser uma lista de dicionários.")

        count = 0
        with open(arquivo_sql, 'r', encoding='utf-8') as arquivo_leitura, \
             open(arquivo_sql + '.tmp', 'w', encoding='utf-8') as arquivo_escrita:
            for linha in arquivo_leitura:
                nova_linha = linha
                for tabela in tabelas:
                    if isinstance(tabela, dict):
                        antigo = tabela.get('oldTable', '')
                        novo = tabela.get('newTable', '')
                        if antigo and novo:
                            if re.search(rf"\b{re.escape(antigo)}\b", linha, re.IGNORECASE):
                                nova_linha = re.sub(rf"CREATE TABLE {re.escape(antigo)}", f"CREATE TABLE {novo}", nova_linha, flags=re.IGNORECASE)
                                nova_linha = re.sub(rf"\b{re.escape(antigo)}\b", novo, nova_linha, flags=re.IGNORECASE)
                                count += 1
                arquivo_escrita.write(nova_linha)

        # Renomear o arquivo temporário para o nome original
        import os
        os.replace(arquivo_sql + '.tmp', arquivo_sql)

        resultado_label.config(text=f"Arquivo SQL atualizado com sucesso. {count} tabelas modificadas.")
    except json.JSONDecodeError:
        resultado_label.config(text="Erro: JSON inválido.")
    except KeyError:
        resultado_label.config(text="Erro: Formato JSON incorreto. Verifique os nomes dos campos.")
    except ValueError as ve:
        resultado_label.config(text=f"Erro: {str(ve)}")
    except UnicodeDecodeError:
        resultado_label.config(text="Erro ao ler o arquivo SQL. Tente usar uma codificação diferente.")
    except Exception as e:
        resultado_label.config(text=f"Erro ao atualizar o arquivo: {str(e)}")

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Modificador de Arquivo SQL com JSON")

# Widget para entrada do caminho do arquivo SQL
entrada_arquivo = tk.Entry(janela, width=50)
entrada_arquivo.pack(pady=10)
tk.Button(janela, text="Selecionar Arquivo SQL", command=selecionar_arquivo).pack(pady=5)

# Widget para entrada do caminho do arquivo JSON
entrada_json = tk.Entry(janela, width=50)
entrada_json.pack(pady=10)
tk.Button(janela, text="Selecionar Arquivo JSON", command=selecionar_json).pack(pady=5)

# Label para mostrar dados do JSON
dados_json = tk.StringVar()
tk.Label(janela, text="Dados do JSON:").pack(pady=5)
tk.Label(janela, textvariable=dados_json, wraplength=400, justify=tk.LEFT).pack(pady=5)

# Botão para modificar o arquivo
botao_modificar = tk.Button(janela, text="Modificar Arquivo", command=modificar_arquivo)
botao_modificar.pack(pady=5)

# Label para mostrar resultado
resultado_label = tk.Label(janela, text="")
resultado_label.pack(pady=10)

# Iniciar loop da interface
janela.mainloop()