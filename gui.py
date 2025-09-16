#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
INTERFACE GRÁFICA DO SISTEMA DE SIMULAÇÃO DE INVESTIMENTOS
Trabalho de Engenharia de Software
Curso: Sistemas de Informação - UFSC

Interface simplificada para demonstrar os 3 casos de uso principais
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from main import SistemaSimulacaoInvestimentos, TipoTaxa

class InterfaceSimulador:
    """Interface gráfica simplificada do sistema"""
    
    def __init__(self):
        self.sistema = SistemaSimulacaoInvestimentos()
        self.simulacao_atual = None

        # Janela principal
        self.root = Tk()
        self.root.title("Sistema de Simulação de Investimentos - SIN/UFSC")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')

        self.criar_interface()

    def criar_interface(self):
        """Cria a interface gráfica"""
        
        # Título principal
        titulo = Label(self.root, text="Sistema de Simulação de Investimentos", 
                      font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        titulo.pack(pady=(20, 10))
        
        # Subtítulo
        subtitulo = Label(self.root, text="Trabalho de Engenharia de Software - SIN/UFSC", 
                         font=('Arial', 12), bg='#f0f0f0', fg='#7f8c8d')
        subtitulo.pack(pady=(0, 30))
        
        # Frame principal com abas para os casos de uso
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # UC01 - Criar e Salvar Simulação
        self.frame_uc01 = self.criar_aba_uc01(notebook)
        notebook.add(self.frame_uc01, text="UC01 - Criar e Salvar")
        
        # UC02 - Editar Simulação  
        self.frame_uc02 = self.criar_aba_uc02(notebook)
        notebook.add(self.frame_uc02, text="UC02 - Editar Simulação")
        
        # UC03 - Testar Simulação
        self.frame_uc03 = self.criar_aba_uc03(notebook)
        notebook.add(self.frame_uc03, text="UC03 - Testar Simulação")
        
        # Frame de status na parte inferior
        self.frame_status = Frame(self.root, bg='#ecf0f1', height=50)
        self.frame_status.pack(fill=X, side=BOTTOM)
        
        self.label_status = Label(self.frame_status, text="Sistema iniciado - Selecione um caso de uso", 
                                 bg='#ecf0f1', fg='#2c3e50', font=('Arial', 10))
        self.label_status.pack(pady=15)

    def criar_aba_uc01(self, parent):
        """Cria aba do UC01 - Criar e Salvar Simulação"""
        frame = Frame(parent, bg='white', padx=30, pady=20)
        
        # Título da aba
        Label(frame, text="UC01 - Criar e Salvar Simulação", 
              font=('Arial', 14, 'bold'), bg='white', fg='#27ae60').pack(pady=(0, 20))
        
        Label(frame, text="Implementado por: Nick D", 
              font=('Arial', 10, 'italic'), bg='white', fg='#7f8c8d').pack(pady=(0, 20))
        
        # Seção Criar Nova Simulação
        grupo_criar = LabelFrame(frame, text="Criar Nova Simulação", font=('Arial', 12, 'bold'))
        grupo_criar.pack(fill=X, pady=(0, 20))
        
        Label(grupo_criar, text="Nome da Simulação:").grid(row=0, column=0, sticky=W, padx=10, pady=10)
        self.entry_nome_uc01 = Entry(grupo_criar, width=40, font=('Arial', 11))
        self.entry_nome_uc01.grid(row=0, column=1, padx=10, pady=10)
        
        Button(grupo_criar, text="CRIAR SIMULAÇÃO", command=self.criar_simulacao_uc01,
               bg='#27ae60', fg='white', font=('Arial', 11, 'bold'), padx=20).grid(row=0, column=2, padx=10, pady=10)
        
        # Seção Salvar/Carregar
        grupo_arquivo = LabelFrame(frame, text="Gerenciar Arquivos", font=('Arial', 12, 'bold'))
        grupo_arquivo.pack(fill=X, pady=(0, 20))
        
        Button(grupo_arquivo, text="SALVAR SIMULAÇÃO", command=self.salvar_simulacao_uc01,
               bg='#3498db', fg='white', font=('Arial', 11, 'bold'), padx=20).pack(side=LEFT, padx=10, pady=10)
        
        Button(grupo_arquivo, text="CARREGAR SIMULAÇÃO", command=self.carregar_simulacao_uc01,
               bg='#9b59b6', fg='white', font=('Arial', 11, 'bold'), padx=20).pack(side=LEFT, padx=10, pady=10)
        
        # Lista de simulações
        grupo_lista = LabelFrame(frame, text="Simulações Criadas", font=('Arial', 12, 'bold'))
        grupo_lista.pack(fill=BOTH, expand=True)
        
        self.lista_simulacoes = Listbox(grupo_lista, height=8, font=('Arial', 10))
        scrollbar = Scrollbar(grupo_lista, orient=VERTICAL, command=self.lista_simulacoes.yview)
        self.lista_simulacoes.configure(yscrollcommand=scrollbar.set)
        
        self.lista_simulacoes.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=RIGHT, fill=Y, pady=10)
        
        Button(grupo_lista, text="ATUALIZAR LISTA", command=self.atualizar_lista_simulacoes,
               bg='#95a5a6', fg='white', font=('Arial', 10)).pack(pady=5)
        
        return frame

    def criar_aba_uc02(self, parent):
        """Cria aba do UC02 - Editar Simulação"""
        frame = Frame(parent, bg='white', padx=30, pady=20)
        
        # Título da aba
        Label(frame, text="UC02 - Editar Simulação", 
              font=('Arial', 14, 'bold'), bg='white', fg='#e67e22').pack(pady=(0, 20))
        
        Label(frame, text="Implementado por: Nick C", 
              font=('Arial', 10, 'italic'), bg='white', fg='#7f8c8d').pack(pady=(0, 20))
        
        # Seleção de simulação
        grupo_selecao = LabelFrame(frame, text="Selecionar Simulação para Editar", font=('Arial', 12, 'bold'))
        grupo_selecao.pack(fill=X, pady=(0, 20))
        
        self.combo_simulacoes = ttk.Combobox(grupo_selecao, width=50, state="readonly")
        self.combo_simulacoes.pack(side=LEFT, padx=10, pady=10)
        
        Button(grupo_selecao, text="SELECIONAR", command=self.selecionar_simulacao_uc02,
               bg='#e67e22', fg='white', font=('Arial', 11, 'bold')).pack(side=LEFT, padx=10, pady=10)
        
        # Edição de parâmetros
        grupo_edicao = LabelFrame(frame, text="Editar Parâmetros", font=('Arial', 12, 'bold'))
        grupo_edicao.pack(fill=X, pady=(0, 20))
        
        # Grid de campos editáveis
        Label(grupo_edicao, text="Nome:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        self.entry_nome_uc02 = Entry(grupo_edicao, width=30)
        self.entry_nome_uc02.grid(row=0, column=1, padx=10, pady=5)
        
        Label(grupo_edicao, text="Aporte Inicial (R$):").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        self.entry_aporte_inicial = Entry(grupo_edicao, width=20)
        self.entry_aporte_inicial.grid(row=1, column=1, padx=10, pady=5, sticky=W)
        
        Label(grupo_edicao, text="Aporte Mensal (R$):").grid(row=2, column=0, sticky=W, padx=10, pady=5)
        self.entry_aporte_mensal = Entry(grupo_edicao, width=20)
        self.entry_aporte_mensal.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        
        Label(grupo_edicao, text="Prazo (meses):").grid(row=3, column=0, sticky=W, padx=10, pady=5)
        self.entry_prazo = Entry(grupo_edicao, width=15)
        self.entry_prazo.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        
        Label(grupo_edicao, text="Taxa Mensal (%):").grid(row=4, column=0, sticky=W, padx=10, pady=5)
        self.entry_taxa = Entry(grupo_edicao, width=15)
        self.entry_taxa.grid(row=4, column=1, padx=10, pady=5, sticky=W)
        
        # Botões de ação
        frame_botoes = Frame(grupo_edicao)
        frame_botoes.grid(row=5, column=0, columnspan=2, pady=20)
        
        Button(frame_botoes, text="SALVAR ALTERAÇÕES", command=self.salvar_alteracoes_uc02,
               bg='#e67e22', fg='white', font=('Arial', 11, 'bold'), padx=20).pack(side=LEFT, padx=10)
        
        Button(frame_botoes, text="LIMPAR CAMPOS", command=self.limpar_campos_uc02,
               bg='#95a5a6', fg='white', font=('Arial', 11, 'bold'), padx=20).pack(side=LEFT, padx=10)
        
        return frame

    def criar_aba_uc03(self, parent):
        """Cria aba do UC03 - Testar/Calcular Simulação"""
        frame = Frame(parent, bg='white', padx=30, pady=20)
        
        # Título da aba
        Label(frame, text="UC03 - Testar/Calcular Simulação", 
              font=('Arial', 14, 'bold'), bg='white', fg='#8e44ad').pack(pady=(0, 20))
        
        Label(frame, text="Implementado por: Nick J", 
              font=('Arial', 10, 'italic'), bg='white', fg='#7f8c8d').pack(pady=(0, 20))
        
        # Seleção e teste
        grupo_teste = LabelFrame(frame, text="Testar Simulação", font=('Arial', 12, 'bold'))
        grupo_teste.pack(fill=X, pady=(0, 20))
        
        self.combo_teste = ttk.Combobox(grupo_teste, width=40, state="readonly")
        self.combo_teste.pack(side=LEFT, padx=10, pady=10)
        
        Button(grupo_teste, text="CALCULAR E TESTAR", command=self.testar_simulacao_uc03,
               bg='#8e44ad', fg='white', font=('Arial', 11, 'bold'), padx=20).pack(side=LEFT, padx=10, pady=10)
        
        # Área de resultados
        grupo_resultados = LabelFrame(frame, text="Resultados do Teste", font=('Arial', 12, 'bold'))
        grupo_resultados.pack(fill=BOTH, expand=True)
        
        self.text_resultados = Text(grupo_resultados, height=15, font=('Courier New', 10),
                                  bg='#2c3e50', fg='#ecf0f1', wrap=WORD)
        scrollbar_texto = Scrollbar(grupo_resultados, orient=VERTICAL, command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar_texto.set)
        
        self.text_resultados.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
        scrollbar_texto.pack(side=RIGHT, fill=Y, pady=10)
        
        # Mensagem inicial
        self.text_resultados.insert(END, "=== SISTEMA DE TESTE DE SIMULAÇÕES ===\n\n")
        self.text_resultados.insert(END, "Instruções:\n")
        self.text_resultados.insert(END, "1. Selecione uma simulação na lista acima\n")
        self.text_resultados.insert(END, "2. Clique em 'CALCULAR E TESTAR'\n")
        self.text_resultados.insert(END, "3. Analise os resultados aqui exibidos\n\n")
        self.text_resultados.insert(END, "Aguardando seleção de simulação para teste...\n")
        
        return frame

    # Métodos do UC01
    def criar_simulacao_uc01(self):
        """UC01 - Cria nova simulação"""
        nome = self.entry_nome_uc01.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Nome da simulação é obrigatório!")
            return
        
        try:
            id_simulacao = self.sistema.criar_simulacao(nome)
            self.simulacao_atual = id_simulacao
            
            self.entry_nome_uc01.delete(0, END)
            self.atualizar_lista_simulacoes()
            self.atualizar_combos()
            self.atualizar_status(f"Simulação '{nome}' criada com ID: {id_simulacao}")
            
            messagebox.showinfo("Sucesso", f"Simulação '{nome}' criada com sucesso!\nID: {id_simulacao}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar simulação: {str(e)}")

    def salvar_simulacao_uc01(self):
        """UC01 - Salva simulação atual"""
        if not self.simulacao_atual:
            messagebox.showwarning("Aviso", "Nenhuma simulação selecionada para salvar!")
            return
        
        arquivo = filedialog.asksaveasfilename(
            title="Salvar simulação",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        
        if arquivo:
            sucesso, msg = self.sistema.salvar_simulacao(self.simulacao_atual, arquivo)
            if sucesso:
                self.atualizar_status(f"Simulação salva: {arquivo}")
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def carregar_simulacao_uc01(self):
        """UC01 - Carrega simulação de arquivo"""
        arquivo = filedialog.askopenfilename(
            title="Carregar simulação",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        
        if arquivo:
            sucesso, resultado = self.sistema.carregar_simulacao(arquivo)
            if sucesso:
                self.simulacao_atual = resultado
                self.atualizar_lista_simulacoes()
                self.atualizar_combos()
                self.atualizar_status(f"Simulação carregada: {resultado}")
                messagebox.showinfo("Sucesso", f"Simulação carregada com ID: {resultado}")
            else:
                messagebox.showerror("Erro", resultado)

    def atualizar_lista_simulacoes(self):
        """Atualiza lista de simulações"""
        self.lista_simulacoes.delete(0, END)
        simulacoes = self.sistema.listar_simulacoes()
        
        for sim in simulacoes:
            status = "✓" if sim['calculada'] else "○"
            texto = f"{status} {sim['id']} - {sim['nome']} ({sim['prazo_meses']} meses)"
            self.lista_simulacoes.insert(END, texto)

    # Métodos do UC02
    def selecionar_simulacao_uc02(self):
        """UC02 - Seleciona simulação para edição"""
        selecao = self.combo_simulacoes.get()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma simulação!")
            return
        
        # Extrai ID da seleção
        id_simulacao = selecao.split(" - ")[0]
        self.simulacao_atual = id_simulacao
        
        # Carrega dados nos campos
        self.carregar_dados_edicao(id_simulacao)
        self.atualizar_status(f"Simulação {id_simulacao} selecionada para edição")

    def carregar_dados_edicao(self, id_simulacao):
        """Carrega dados da simulação nos campos de edição"""
        simulacoes = self.sistema.listar_simulacoes()
        sim_info = next((s for s in simulacoes if s['id'] == id_simulacao), None)
        
        if sim_info:
            # Limpa campos
            self.limpar_campos_uc02()
            
            # Preenche nome
            self.entry_nome_uc02.insert(0, sim_info['nome'])
            
            # Para outros campos, precisaríamos acessar a simulação completa
            # Por simplicidade, deixamos campos vazios para o usuário preencher

    def salvar_alteracoes_uc02(self):
        """UC02 - Salva alterações na simulação"""
        if not self.simulacao_atual:
            messagebox.showwarning("Aviso", "Nenhuma simulação selecionada!")
            return
        
        try:
            # Coleta dados dos campos
            parametros = {}
            
            # Nome
            novo_nome = self.entry_nome_uc02.get().strip()
            if novo_nome:
                sucesso, msg = self.sistema.editar_nome_simulacao(self.simulacao_atual, novo_nome)
                if not sucesso:
                    messagebox.showerror("Erro", msg)
                    return
            
            # Outros parâmetros
            if self.entry_aporte_inicial.get():
                parametros['aporte_inicial'] = float(self.entry_aporte_inicial.get())
            
            if self.entry_aporte_mensal.get():
                parametros['aporte_mensal'] = float(self.entry_aporte_mensal.get())
            
            if self.entry_prazo.get():
                parametros['prazo_meses'] = int(self.entry_prazo.get())
            
            if self.entry_taxa.get():
                parametros['tipo_taxa'] = TipoTaxa.FIXA
                parametros['taxa_fixa'] = float(self.entry_taxa.get())
            
            # Aplica alterações
            if parametros:
                sucesso, erros = self.sistema.configurar_simulacao(self.simulacao_atual, **parametros)
                if sucesso:
                    self.atualizar_lista_simulacoes()
                    self.atualizar_combos()
                    self.atualizar_status("Alterações salvas com sucesso")
                    messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
                else:
                    messagebox.showerror("Erro", "\n".join(erros))
            else:
                messagebox.showinfo("Info", "Nome atualizado com sucesso!")
                
        except ValueError as e:
            messagebox.showerror("Erro", f"Valores inválidos nos campos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def limpar_campos_uc02(self):
        """Limpa campos de edição"""
        self.entry_nome_uc02.delete(0, END)
        self.entry_aporte_inicial.delete(0, END)
        self.entry_aporte_mensal.delete(0, END)
        self.entry_prazo.delete(0, END)
        self.entry_taxa.delete(0, END)

    # Métodos do UC03
    def testar_simulacao_uc03(self):
        """UC03 - Testa e calcula simulação"""
        selecao = self.combo_teste.get()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma simulação para testar!")
            return
        
        # Extrai ID da seleção
        id_simulacao = selecao.split(" - ")[0]
        
        self.text_resultados.delete(1.0, END)
        self.text_resultados.insert(END, f"Testando simulação {id_simulacao}...\n\n")
        self.text_resultados.update()
        
        try:
            # Executa o teste
            resultado = self.sistema.testar_simulacao(id_simulacao)
            
            if resultado['sucesso']:
                self.exibir_resultados_teste(resultado)
                self.atualizar_status(f"Teste da simulação {id_simulacao} concluído")
            else:
                self.text_resultados.insert(END, "ERRO NO TESTE:\n")
                for erro in resultado['erros']:
                    self.text_resultados.insert(END, f"- {erro}\n")
                
        except Exception as e:
            self.text_resultados.insert(END, f"ERRO INESPERADO: {str(e)}\n")

    def exibir_resultados_teste(self, resultado):
        """Exibe resultados do teste na área de texto"""
        self.text_resultados.delete(1.0, END)
        
        sim_info = resultado['simulacao']
        resultados = resultado['resultados']
        
        texto = "=" * 60 + "\n"
        texto += f"RESULTADO DO TESTE - {sim_info['nome'].upper()}\n"
        texto += "=" * 60 + "\n\n"
        
        texto += "MÉTRICAS FINAIS:\n"
        texto += "-" * 20 + "\n"
        texto += f"Saldo Final:      R$ {resultados['saldo_final']:>15,.2f}\n"
        texto += f"Total Investido:  R$ {resultados['total_investido']:>15,.2f}\n"
        texto += f"Juros Acumulados: R$ {resultados['juros_acumulados']:>15,.2f}\n"
        texto += f"Rentabilidade:       {resultados['rentabilidade_percentual']:>15.2f}%\n"
        texto += f"Prazo Simulado:      {resultados['total_meses']:>15} meses\n\n"
        
        texto += "ANÁLISE DO INVESTIMENTO:\n"
        texto += "-" * 25 + "\n"
        
        if resultados['rentabilidade_percentual'] > 50:
            texto += "✓ EXCELENTE rentabilidade obtida!\n"
        elif resultados['rentabilidade_percentual'] > 20:
            texto += "✓ BOA rentabilidade obtida!\n"
        else:
            texto += "○ Rentabilidade MODERADA\n"
        
        ganho_liquido = resultados['saldo_final'] - resultados['total_investido']
        texto += f"\nGanho líquido: R$ {ganho_liquido:,.2f}\n"
        
        if resultados['total_meses'] > 0:
            ganho_mensal_medio = ganho_liquido / resultados['total_meses']
            texto += f"Ganho médio mensal: R$ {ganho_mensal_medio:,.2f}\n"
        
        texto += "\n" + "=" * 60 + "\n"
        texto += "TESTE CONCLUÍDO COM SUCESSO!\n"
        texto += "=" * 60 + "\n"
        
        self.text_resultados.insert(END, texto)

    # Métodos auxiliares
    def atualizar_combos(self):
        """Atualiza comboboxes com lista de simulações"""
        simulacoes = self.sistema.listar_simulacoes()
        valores = [f"{s['id']} - {s['nome']}" for s in simulacoes]
        
        self.combo_simulacoes['values'] = valores
        self.combo_teste['values'] = valores

    def atualizar_status(self, mensagem):
        """Atualiza barra de status"""
        self.label_status.config(text=mensagem)

    def executar(self):
        """Executa a aplicação"""
        # Atualiza listas iniciais
        self.atualizar_lista_simulacoes()
        self.atualizar_combos()
        
        # Inicia interface
        self.root.mainloop()

# Execução da aplicação
if __name__ == '__main__':
    app = InterfaceSimulador()
    app.executar()