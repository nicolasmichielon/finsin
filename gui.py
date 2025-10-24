"""
INTERFACE GRÁFICA DO SINFIN
Trabalho de Análise e Projeto de Sistemas
Curso: Sistemas de Informação - UFSC
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from main import SistemaSimulacaoInvestimentos, TipoTaxa

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_DISPONIVEL = True
except ImportError:
    MATPLOTLIB_DISPONIVEL = False

class InterfaceSimulador:
    """Interface gráfica unificada do sistema"""

    def __init__(self):
        self.sistema = SistemaSimulacaoInvestimentos()
        self.simulacao_atual = None

        # Janela principal
        self.root = tk.Tk()
        self.root.title("Sistema de Simulação de Investimentos - SIN/UFSC")
        self.root.geometry("1000x750")

        # Configurar tema moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Definir cores do tema minimalista
        self.cores = {
            'bg_principal': '#fafafa',
            'bg_secundario': '#ffffff',
            'bg_destaque': '#f8f9fa',
            'texto_principal': '#2c3e50',
            'texto_secundario': '#7f8c8d',
            'accent_principal': '#6c757d',
            'border': '#dee2e6'
        }

        self.root.configure(bg=self.cores['bg_principal'])
        self.configurar_tema()
        self.criar_interface()

    def configurar_tema(self):
        """Configura o tema visual da aplicação"""
        # Configurar estilos ttk
        self.style.configure('Titulo.TLabel',
                            font=('Segoe UI', 14, 'bold'),
                            background=self.cores['bg_secundario'],
                            foreground=self.cores['texto_principal'])

        self.style.configure('Accent.TButton',
                            background=self.cores['accent_principal'],
                            foreground='white',
                            font=('Segoe UI', 10, 'bold'))

        self.style.configure('Outline.TButton',
                            background=self.cores['bg_secundario'],
                            foreground=self.cores['accent_principal'],
                            font=('Segoe UI', 10),
                            relief='solid',
                            borderwidth=1)

    def criar_interface(self):
        """Cria a interface gráfica unificada"""

        # Título principal
        titulo = tk.Label(self.root, text="Sistema de Simulação de Investimentos",
                      font=('Segoe UI', 18, 'bold'),
                      bg=self.cores['bg_principal'],
                      fg=self.cores['texto_principal'])
        titulo.pack(pady=(20, 10))

        # Subtítulo
        subtitulo = tk.Label(self.root, text="Trabalho de Análise e Projeto de Sistemas - SIN/UFSC",
                         font=('Segoe UI', 12),
                         bg=self.cores['bg_principal'],
                         fg=self.cores['texto_secundario'])
        subtitulo.pack(pady=(0, 20))

        # Container principal
        main_container = tk.Frame(self.root, bg=self.cores['bg_principal'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Container esquerdo (lista de simulações)
        left_container = tk.Frame(main_container, bg=self.cores['bg_secundario'],
                                 relief=tk.FLAT, bd=1, highlightbackground=self.cores['border'],
                                 highlightthickness=1)
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))
        left_container.configure(width=300)

        # Container direito (configuração e resultados)
        right_container = tk.Frame(main_container, bg=self.cores['bg_principal'])
        right_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Seção de configuração
        config_section = tk.Frame(right_container, bg=self.cores['bg_secundario'],
                                relief=tk.FLAT, bd=1, highlightbackground=self.cores['border'],
                                highlightthickness=1)
        config_section.pack(fill=tk.X, pady=(0, 20))

        # Seção de resultados
        results_section = tk.Frame(right_container, bg=self.cores['bg_secundario'],
                                 relief=tk.FLAT, bd=1, highlightbackground=self.cores['border'],
                                 highlightthickness=1)
        results_section.pack(fill=tk.BOTH, expand=True)

        self.criar_secao_lista_simulacoes(left_container)
        self.criar_secao_configuracao(config_section)
        self.criar_secao_resultados(results_section)

    def criar_secao_lista_simulacoes(self, parent):
        """Cria seção de lista de simulações"""

        # Título da seção
        ttk.Label(parent, text="Simulações", style='Titulo.TLabel').pack(pady=(20, 15))

        # Botões de ação
        btn_container = tk.Frame(parent, bg=self.cores['bg_secundario'])
        btn_container.pack(padx=15, pady=(0, 15), fill=tk.X)

        btn_nova = ttk.Button(btn_container, text="+ Nova",
                             command=self.nova_simulacao,
                             style='Accent.TButton', cursor='hand2')
        btn_nova.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        btn_excluir = ttk.Button(btn_container, text="Excluir",
                                command=self.excluir_simulacao,
                                style='Outline.TButton', cursor='hand2')
        btn_excluir.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # Botão Comparar
        ttk.Button(parent, text="Comparar Selecionadas", command=self.comparar_simulacoes,
                  style='Accent.TButton', cursor='hand2').pack(padx=15, pady=(0, 15), fill=tk.X)

        # Container para Treeview
        tree_container = tk.Frame(parent, bg=self.cores['bg_secundario'])
        tree_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Treeview para listar simulações
        self.tree_simulacoes = ttk.Treeview(tree_container,
                                           columns=('status',),
                                           show='tree headings',
                                           selectmode='extended',
                                           height=15)

        self.tree_simulacoes.heading('#0', text='Nome')
        self.tree_simulacoes.heading('status', text='Status')
        self.tree_simulacoes.column('#0', width=180)
        self.tree_simulacoes.column('status', width=80, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL,
                                 command=self.tree_simulacoes.yview)
        self.tree_simulacoes.configure(yscrollcommand=scrollbar.set)

        self.tree_simulacoes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind duplo clique para carregar simulação
        self.tree_simulacoes.bind('<Double-1>', self.ao_selecionar_simulacao)

        # Atualizar lista
        self.atualizar_lista_simulacoes()

    def criar_secao_configuracao(self, parent):
        """Cria seção de configuração da simulação"""

        # Título da seção
        ttk.Label(parent, text="Configuração da Simulação", style='Titulo.TLabel').pack(pady=(20, 15))

        # Container para formulário
        form_container = tk.Frame(parent, bg=self.cores['bg_secundario'])
        form_container.pack(fill=tk.X, padx=30, pady=(0, 20))

        # Nome da simulação
        nome_frame = tk.Frame(form_container, bg=self.cores['bg_secundario'])
        nome_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(nome_frame, text="Nome da Simulação:").pack(anchor=tk.W)
        self.entry_nome = ttk.Entry(nome_frame, width=40, font=('Segoe UI', 11))
        self.entry_nome.pack(fill=tk.X, pady=(5, 0))

        # Parâmetros em grid
        params_frame = tk.Frame(form_container, bg=self.cores['bg_secundario'])
        params_frame.pack(fill=tk.X, pady=(0, 20))

        # Primeira linha
        ttk.Label(params_frame, text="Aporte Inicial (R$):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_aporte_inicial = ttk.Entry(params_frame, width=15, font=('Segoe UI', 11))
        self.entry_aporte_inicial.grid(row=0, column=1, padx=(10, 30), pady=5, sticky=tk.W)

        ttk.Label(params_frame, text="Aporte Mensal (R$):").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_aporte_mensal = ttk.Entry(params_frame, width=15, font=('Segoe UI', 11))
        self.entry_aporte_mensal.grid(row=0, column=3, padx=(10, 0), pady=5, sticky=tk.W)

        # Segunda linha
        ttk.Label(params_frame, text="Prazo (meses):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_prazo = ttk.Entry(params_frame, width=15, font=('Segoe UI', 11))
        self.entry_prazo.grid(row=1, column=1, padx=(10, 30), pady=5, sticky=tk.W)

        # Tipo de taxa
        ttk.Label(params_frame, text="Tipo de Taxa:").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.tipo_taxa_var = tk.StringVar(value="FIXA")
        taxa_frame = tk.Frame(params_frame, bg=self.cores['bg_secundario'])
        taxa_frame.grid(row=1, column=3, padx=(10, 0), pady=5, sticky=tk.W)

        ttk.Radiobutton(taxa_frame, text="Fixa", variable=self.tipo_taxa_var,
                       value="FIXA", command=self.ao_mudar_tipo_taxa).pack(side=tk.LEFT)
        ttk.Radiobutton(taxa_frame, text="Variável", variable=self.tipo_taxa_var,
                       value="VARIAVEL", command=self.ao_mudar_tipo_taxa).pack(side=tk.LEFT, padx=(10, 0))

        # Terceira linha - Taxa
        ttk.Label(params_frame, text="Taxa (%):").grid(row=2, column=0, sticky=tk.W, pady=5)
        taxa_input_frame = tk.Frame(params_frame, bg=self.cores['bg_secundario'])
        taxa_input_frame.grid(row=2, column=1, columnspan=3, padx=(10, 0), pady=5, sticky=tk.W)

        self.entry_taxa = ttk.Entry(taxa_input_frame, width=15, font=('Segoe UI', 11))
        self.entry_taxa.pack(side=tk.LEFT)

        self.btn_taxas_variaveis = ttk.Button(taxa_input_frame, text="Definir Taxas Variáveis",
                                             command=self.abrir_dialog_taxas_variaveis,
                                             style='Outline.TButton', cursor='hand2')
        self.btn_taxas_variaveis.pack(side=tk.LEFT, padx=(10, 0))
        self.btn_taxas_variaveis.pack_forget()

        self.taxas_variaveis = None

        # Botões de ação
        actions_frame = tk.Frame(form_container, bg=self.cores['bg_secundario'])
        actions_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(actions_frame, text="Calcular Simulação", command=self.calcular_simulacao,
                  style='Accent.TButton', cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(actions_frame, text="Limpar", command=self.limpar_campos,
                  style='Outline.TButton', cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(actions_frame, text="Ver Histórico", command=self.ver_historico,
                  style='Outline.TButton', cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))

        if MATPLOTLIB_DISPONIVEL:
            ttk.Button(actions_frame, text="Ver Gráficos", command=self.ver_graficos,
                      style='Outline.TButton', cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(actions_frame, text="Exportar CSV", command=self.exportar_csv,
                  style='Outline.TButton', cursor='hand2').pack(side=tk.RIGHT, padx=(0, 10))

        ttk.Button(actions_frame, text="Salvar Arquivo", command=self.salvar_simulacao,
                  style='Outline.TButton', cursor='hand2').pack(side=tk.RIGHT, padx=(0, 10))

        ttk.Button(actions_frame, text="Carregar Arquivo", command=self.carregar_simulacao,
                  style='Outline.TButton', cursor='hand2').pack(side=tk.RIGHT)


    def criar_secao_resultados(self, parent):
        """Cria seção de resultados da simulação"""

        # Título da seção
        ttk.Label(parent, text="Resultados da Simulação", style='Titulo.TLabel').pack(pady=(20, 15))

        # Área de resultados
        result_container = tk.Frame(parent, bg=self.cores['bg_secundario'])
        result_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))

        self.text_resultados = tk.Text(result_container, font=('Courier New', 11),
                                     bg=self.cores['bg_destaque'],
                                     fg=self.cores['texto_principal'],
                                     wrap=tk.WORD,
                                     relief=tk.FLAT,
                                     highlightbackground=self.cores['border'],
                                     highlightthickness=1,
                                     insertbackground=self.cores['texto_principal'],
                                     selectbackground=self.cores['accent_principal'])

        scrollbar_results = ttk.Scrollbar(result_container, orient=tk.VERTICAL, command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar_results.set)

        self.text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_results.pack(side=tk.RIGHT, fill=tk.Y)

        # Mensagem inicial
        self.text_resultados.insert(tk.END, "=== SISTEMA DE SIMULAÇÃO DE INVESTIMENTOS ===\n\n")
        self.text_resultados.insert(tk.END, "Preencha os campos acima e clique em 'Calcular Simulação'\n")
        self.text_resultados.insert(tk.END, "para ver os resultados da análise financeira.\n\n")
        self.text_resultados.insert(tk.END, "Os cálculos e projections aparecerão aqui...")



    # Métodos de controle de taxas
    def ao_mudar_tipo_taxa(self):
        """Alterna entre taxa fixa e variável"""
        if self.tipo_taxa_var.get() == "FIXA":
            self.entry_taxa.config(state='normal')
            self.btn_taxas_variaveis.pack_forget()
            self.taxas_variaveis = None
        else:
            self.entry_taxa.delete(0, tk.END)
            self.entry_taxa.config(state='disabled')
            self.btn_taxas_variaveis.pack(side=tk.LEFT, padx=(10, 0))

    def abrir_dialog_taxas_variaveis(self):
        """Abre diálogo para inserir taxas variáveis"""
        try:
            prazo = int(self.entry_prazo.get())
            if prazo <= 0:
                messagebox.showerror("Erro", "Defina um prazo válido primeiro!")
                return
        except ValueError:
            messagebox.showerror("Erro", "Defina um prazo válido primeiro!")
            return

        # Cria janela de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Definir Taxas Variáveis")
        dialog.geometry("500x600")
        dialog.configure(bg=self.cores['bg_principal'])

        # Título
        ttk.Label(dialog, text=f"Defina as taxas para {prazo} meses",
                 style='Titulo.TLabel').pack(pady=20)

        # Container com scroll
        canvas_frame = tk.Frame(dialog, bg=self.cores['bg_secundario'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        canvas = tk.Canvas(canvas_frame, bg=self.cores['bg_secundario'])
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.cores['bg_secundario'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Entradas para cada mês
        entries = []
        for i in range(prazo):
            frame = tk.Frame(scrollable_frame, bg=self.cores['bg_secundario'])
            frame.pack(fill=tk.X, padx=20, pady=5)

            ttk.Label(frame, text=f"Mês {i+1}:").pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT, padx=10)

            if self.taxas_variaveis and i < len(self.taxas_variaveis):
                entry.insert(0, str(self.taxas_variaveis[i]))

            ttk.Label(frame, text="%").pack(side=tk.LEFT)
            entries.append(entry)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botões
        btn_frame = tk.Frame(dialog, bg=self.cores['bg_principal'])
        btn_frame.pack(pady=10)

        def salvar_taxas():
            try:
                taxas = [float(entry.get()) for entry in entries]
                if any(t < 0 or t > 100 for t in taxas):
                    messagebox.showerror("Erro", "Todas as taxas devem estar entre 0% e 100%!")
                    return
                self.taxas_variaveis = taxas
                messagebox.showinfo("Sucesso", f"{len(taxas)} taxas definidas com sucesso!")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Todas as taxas devem ser números válidos!")

        ttk.Button(btn_frame, text="Salvar", command=salvar_taxas,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy,
                  style='Outline.TButton').pack(side=tk.LEFT, padx=5)

    # Métodos de controle da lista de simulações
    def atualizar_lista_simulacoes(self):
        """Atualiza a lista de simulações no Treeview"""
        # Limpa a lista atual
        for item in self.tree_simulacoes.get_children():
            self.tree_simulacoes.delete(item)

        # Obtém todas as simulações
        simulacoes = self.sistema.listar_simulacoes()

        # Adiciona cada simulação na lista
        for sim in simulacoes:
            status = "✓" if sim['calculada'] else "○"
            nome_display = f"{sim['nome']} ({sim['id']})"
            self.tree_simulacoes.insert('', tk.END, iid=sim['id'],
                                       text=nome_display,
                                       values=(status,))

    def nova_simulacao(self):
        """Cria uma nova simulação"""
        # Limpa campos
        self.limpar_campos()
        self.simulacao_atual = None
        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.insert(tk.END, "Nova simulação criada.\nPreencha os campos e clique em 'Calcular Simulação'.")

    def ao_selecionar_simulacao(self, event):
        """Carrega simulação selecionada ao dar duplo clique"""
        selection = self.tree_simulacoes.selection()
        if selection:
            id_simulacao = selection[0]
            self.simulacao_atual = id_simulacao
            self.carregar_dados_simulacao(id_simulacao)

            # Verifica se já foi calculada e exibe resultados
            simulacao = self.sistema.gerenciador.obter_simulacao(id_simulacao)
            if simulacao and simulacao.resultados:
                resultado = self.sistema.testar_simulacao(id_simulacao)
                if resultado['sucesso']:
                    self.exibir_resultados(resultado)

    def excluir_simulacao(self):
        """Exclui a simulação selecionada"""
        selection = self.tree_simulacoes.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma simulação para excluir!")
            return

        id_simulacao = selection[0]
        simulacao = self.sistema.gerenciador.obter_simulacao(id_simulacao)

        if not simulacao:
            messagebox.showerror("Erro", "Simulação não encontrada!")
            return

        # Confirmação
        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir a simulação '{simulacao.nome}'?\n\nEsta ação não pode ser desfeita."
        )

        if confirmar:
            sucesso, msg = self.sistema.excluir_simulacao(id_simulacao)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)

                # Se for a simulação atual, limpa os campos
                if self.simulacao_atual == id_simulacao:
                    self.nova_simulacao()

                # Atualiza lista
                self.atualizar_lista_simulacoes()
            else:
                messagebox.showerror("Erro", msg)

    # Métodos de controle
    def criar_simulacao_automatica(self):
        """Cria simulação automaticamente quando necessário"""
        nome = self.entry_nome.get().strip()
        if not nome:
            nome = "Simulação " + str(len(self.sistema.gerenciador.simulacoes) + 1)
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome)

        try:
            if not self.simulacao_atual:
                id_simulacao = self.sistema.criar_simulacao(nome)
                self.simulacao_atual = id_simulacao
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar simulação: {str(e)}")
            return False
        return True

    def validar_campos(self):
        """Valida se os campos estão preenchidos corretamente"""
        try:
            if not self.entry_aporte_inicial.get().strip():
                messagebox.showerror("Erro", "Aporte inicial é obrigatório!")
                return False

            aporte_inicial = float(self.entry_aporte_inicial.get())
            if aporte_inicial <= 0:
                messagebox.showerror("Erro", "Aporte inicial deve ser maior que zero!")
                return False

            if not self.entry_prazo.get().strip():
                messagebox.showerror("Erro", "Prazo é obrigatório!")
                return False

            prazo = int(self.entry_prazo.get())
            if prazo <= 0:
                messagebox.showerror("Erro", "Prazo deve ser maior que zero!")
                return False

            if not self.entry_taxa.get().strip():
                messagebox.showerror("Erro", "Taxa mensal é obrigatória!")
                return False

            taxa = float(self.entry_taxa.get())
            if taxa < 0:
                messagebox.showerror("Erro", "Taxa não pode ser negativa!")
                return False

            return True

        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos nos campos!")
            return False

    def aplicar_parametros(self):
        """Aplica parâmetros da interface na simulação"""
        try:
            parametros = {}

            # Nome
            nome = self.entry_nome.get().strip()
            if nome:
                self.sistema.editar_nome_simulacao(self.simulacao_atual, nome)

            # Parâmetros financeiros
            parametros['aporte_inicial'] = float(self.entry_aporte_inicial.get())
            parametros['prazo_meses'] = int(self.entry_prazo.get())

            if self.entry_aporte_mensal.get().strip():
                parametros['aporte_mensal'] = float(self.entry_aporte_mensal.get())
            else:
                parametros['aporte_mensal'] = 0.0

            # Tipo de taxa
            if self.tipo_taxa_var.get() == "FIXA":
                parametros['tipo_taxa'] = TipoTaxa.FIXA
                parametros['taxa_fixa'] = float(self.entry_taxa.get())
                parametros['taxas_variaveis'] = None
            else:
                if not self.taxas_variaveis:
                    raise Exception("Defina as taxas variáveis antes de calcular!")
                parametros['tipo_taxa'] = TipoTaxa.VARIAVEL
                parametros['taxas_variaveis'] = self.taxas_variaveis
                parametros['taxa_fixa'] = None

            # Aplica configurações
            sucesso, erros = self.sistema.configurar_simulacao(self.simulacao_atual, **parametros)
            if not sucesso:
                raise Exception("\n".join(erros))

        except Exception as e:
            raise Exception(f"Erro ao aplicar parâmetros: {str(e)}")

    def carregar_dados_simulacao(self, id_simulacao):
        """Carrega dados da simulação nos campos"""
        simulacao = self.sistema.gerenciador.obter_simulacao(id_simulacao)
        if not simulacao:
            return

        # Limpa campos
        self.limpar_campos()

        # Preenche informações
        self.entry_nome.insert(0, simulacao.nome)
        self.entry_aporte_inicial.insert(0, str(simulacao.aporte_inicial))
        self.entry_aporte_mensal.insert(0, str(simulacao.aporte_mensal or 0))
        self.entry_prazo.insert(0, str(simulacao.prazo_meses))

        if simulacao.tipo_taxa == TipoTaxa.FIXA:
            self.tipo_taxa_var.set("FIXA")
            if simulacao.taxa_fixa is not None:
                self.entry_taxa.insert(0, str(simulacao.taxa_fixa))
            self.ao_mudar_tipo_taxa()
        else:
            self.tipo_taxa_var.set("VARIAVEL")
            self.taxas_variaveis = simulacao.taxas_variaveis
            self.ao_mudar_tipo_taxa()

    def calcular_simulacao(self):
        """Calcula e exibe resultados da simulação"""
        # Validar campos
        if not self.validar_campos():
            return

        # Criar simulação automaticamente se necessário
        if not self.criar_simulacao_automatica():
            return

        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.insert(tk.END, "Calculando simulação...\n\n")
        self.text_resultados.update()

        try:
            # Aplicar parâmetros
            self.aplicar_parametros()

            # Executar cálculo
            resultado = self.sistema.testar_simulacao(self.simulacao_atual)

            if resultado['sucesso']:
                self.exibir_resultados(resultado)
                self.atualizar_lista_simulacoes()
            else:
                self.text_resultados.insert(tk.END, "ERRO NO CÁLCULO:\n")
                for erro in resultado['erros']:
                    self.text_resultados.insert(tk.END, f"- {erro}\n")

        except Exception as e:
            self.text_resultados.insert(tk.END, f"ERRO INESPERADO: {str(e)}\n")

    def exibir_resultados(self, resultado):
        """Exibe resultados na área de texto"""
        self.text_resultados.delete(1.0, tk.END)

        sim_info = resultado['simulacao']
        resultados = resultado['resultados']

        texto = "=" * 60 + "\n"
        texto += f"RESULTADOS - {sim_info['nome'].upper()}\n"
        texto += "=" * 60 + "\n\n"

        texto += "RESUMO FINANCEIRO:\n"
        texto += "-" * 20 + "\n"
        texto += f"Saldo Final:      R$ {resultados['saldo_final']:>15,.2f}\n"
        texto += f"Total Investido:  R$ {resultados['total_investido']:>15,.2f}\n"
        texto += f"Juros Acumulados: R$ {resultados['juros_acumulados']:>15,.2f}\n"
        texto += f"Rentabilidade:       {resultados['rentabilidade_percentual']:>15.2f}%\n"
        texto += f"Prazo:               {resultados['total_meses']:>15} meses\n\n"

        ganho_liquido = resultados['saldo_final'] - resultados['total_investido']
        texto += f"Ganho líquido: R$ {ganho_liquido:,.2f}\n"

        if resultados['total_meses'] > 0:
            ganho_mensal_medio = ganho_liquido / resultados['total_meses']
            texto += f"Ganho médio mensal: R$ {ganho_mensal_medio:,.2f}\n"

        texto += "\n" + "=" * 60 + "\n"

        self.text_resultados.insert(tk.END, texto)

    def salvar_simulacao(self):
        """Salva simulação atual em arquivo"""
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
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def carregar_simulacao(self):
        """Carrega simulação de arquivo"""
        arquivo = filedialog.askopenfilename(
            title="Carregar simulação",
            filetypes=[("Arquivos JSON", "*.json")]
        )

        if arquivo:
            sucesso, resultado = self.sistema.carregar_simulacao(arquivo)
            if sucesso:
                self.simulacao_atual = resultado
                self.carregar_dados_simulacao(resultado)
                self.atualizar_lista_simulacoes()
                messagebox.showinfo("Sucesso", f"Simulação carregada com ID: {resultado}")
            else:
                messagebox.showerror("Erro", resultado)

    def exportar_csv(self):
        """Exporta simulação atual para CSV"""
        if not self.simulacao_atual:
            messagebox.showwarning("Aviso", "Nenhuma simulação selecionada para exportar!")
            return

        arquivo = filedialog.asksaveasfilename(
            title="Exportar para CSV",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")]
        )

        if arquivo:
            sucesso, msg = self.sistema.exportar_csv(self.simulacao_atual, arquivo)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def ver_historico(self):
        """Exibe o histórico de modificações da simulação"""
        if not self.simulacao_atual:
            messagebox.showwarning("Aviso", "Nenhuma simulação selecionada!")
            return

        historico = self.sistema.obter_historico(self.simulacao_atual)
        if not historico:
            messagebox.showinfo("Histórico", "Esta simulação ainda não possui histórico de modificações.")
            return

        # Cria janela de diálogo
        dialog = tk.Toplevel(self.root)
        dialog.title("Histórico de Modificações")
        dialog.geometry("700x500")
        dialog.configure(bg=self.cores['bg_principal'])

        # Título
        simulacao = self.sistema.gerenciador.obter_simulacao(self.simulacao_atual)
        ttk.Label(dialog, text=f"Histórico - {simulacao.nome}",
                 style='Titulo.TLabel').pack(pady=20)

        # Container com scroll
        text_container = tk.Frame(dialog, bg=self.cores['bg_secundario'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        text_historico = tk.Text(text_container, font=('Courier New', 10),
                                bg=self.cores['bg_destaque'],
                                fg=self.cores['texto_principal'],
                                wrap=tk.WORD,
                                relief=tk.FLAT)

        scrollbar = ttk.Scrollbar(text_container, orient=tk.VERTICAL,
                                 command=text_historico.yview)
        text_historico.configure(yscrollcommand=scrollbar.set)

        text_historico.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Preenche histórico
        text_historico.insert(tk.END, "=" * 70 + "\n")
        text_historico.insert(tk.END, f"HISTÓRICO DE MODIFICAÇÕES - {len(historico)} alterações\n")
        text_historico.insert(tk.END, "=" * 70 + "\n\n")

        for i, mod in enumerate(reversed(historico), 1):
            data_hora = mod.timestamp.strftime("%d/%m/%Y %H:%M:%S")
            text_historico.insert(tk.END, f"[{i}] {data_hora}\n")
            text_historico.insert(tk.END, f"    Campo: {mod.campo_alterado}\n")
            text_historico.insert(tk.END, f"    De:    {mod.valor_antigo}\n")
            text_historico.insert(tk.END, f"    Para:  {mod.valor_novo}\n")
            text_historico.insert(tk.END, "\n")

        text_historico.config(state='disabled')

        # Botão fechar
        ttk.Button(dialog, text="Fechar", command=dialog.destroy,
                  style='Accent.TButton').pack(pady=10)

    def ver_graficos(self):
        """Exibe gráficos da simulação"""
        if not MATPLOTLIB_DISPONIVEL:
            messagebox.showerror("Erro", "Matplotlib não está instalado!")
            return

        if not self.simulacao_atual:
            messagebox.showwarning("Aviso", "Nenhuma simulação selecionada!")
            return

        simulacao = self.sistema.gerenciador.obter_simulacao(self.simulacao_atual)
        if not simulacao or not simulacao.resultados:
            messagebox.showwarning("Aviso", "Calcule a simulação antes de visualizar os gráficos!")
            return

        # Cria janela de gráficos
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Gráficos - {simulacao.nome}")
        dialog.geometry("1000x900")
        dialog.configure(bg=self.cores['bg_principal'])

        # Título
        ttk.Label(dialog, text=f"Gráficos da Simulação - {simulacao.nome}",
                 style='Titulo.TLabel').pack(pady=20)

        # Notebook para separar os gráficos
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Aba 1: Gráfico de Evolução
        tab_evolucao = tk.Frame(notebook, bg=self.cores['bg_secundario'])
        notebook.add(tab_evolucao, text="Evolução do Investimento")

        fig_evolucao = self.sistema.criar_grafico_evolucao(self.simulacao_atual)
        if fig_evolucao:
            canvas_evolucao = FigureCanvasTkAgg(fig_evolucao, master=tab_evolucao)
            canvas_evolucao.draw()
            canvas_evolucao.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Aba 2: Gráfico de Composição
        tab_composicao = tk.Frame(notebook, bg=self.cores['bg_secundario'])
        notebook.add(tab_composicao, text="Composição do Saldo")

        fig_composicao = self.sistema.criar_grafico_composicao(self.simulacao_atual)
        if fig_composicao:
            canvas_composicao = FigureCanvasTkAgg(fig_composicao, master=tab_composicao)
            canvas_composicao.draw()
            canvas_composicao.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Botão fechar
        ttk.Button(dialog, text="Fechar", command=dialog.destroy,
                  style='Accent.TButton').pack(pady=10)


    def comparar_simulacoes(self):
        """Compara simulações selecionadas"""
        selection = self.tree_simulacoes.selection()
        if len(selection) < 2:
            messagebox.showwarning("Aviso", "Selecione pelo menos 2 simulações para comparar!\n\nDica: Use Ctrl+Clique para selecionar múltiplas simulações.")
            return

        # Obtém IDs das simulações selecionadas
        ids_selecionados = list(selection)

        # Obtém dados de comparação
        comparacao = self.sistema.comparar_simulacoes(ids_selecionados)
        if not comparacao:
            messagebox.showerror("Erro", "Erro ao comparar simulações!")
            return

        # Cria janela de comparação
        dialog = tk.Toplevel(self.root)
        dialog.title("Comparação de Simulações")
        dialog.geometry("1200x700")
        dialog.configure(bg=self.cores['bg_principal'])

        # Título
        ttk.Label(dialog, text=f"Comparação de {len(ids_selecionados)} Simulações",
                 style='Titulo.TLabel').pack(pady=20)

        # Notebook para separar tabela e gráfico
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Aba 1: Tabela Comparativa
        tab_tabela = tk.Frame(notebook, bg=self.cores['bg_secundario'])
        notebook.add(tab_tabela, text="Tabela Comparativa")

        # Container com scroll para tabela
        text_container = tk.Frame(tab_tabela, bg=self.cores['bg_secundario'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        text_comparacao = tk.Text(text_container, font=('Courier New', 10),
                                 bg=self.cores['bg_destaque'],
                                 fg=self.cores['texto_principal'],
                                 wrap=tk.NONE)

        scrollbar_y = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=text_comparacao.yview)
        scrollbar_x = ttk.Scrollbar(text_container, orient=tk.HORIZONTAL, command=text_comparacao.xview)
        text_comparacao.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        text_comparacao.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        text_container.grid_rowconfigure(0, weight=1)
        text_container.grid_columnconfigure(0, weight=1)

        # Preenche tabela comparativa
        text_comparacao.insert(tk.END, "=" * 140 + "\n")
        text_comparacao.insert(tk.END, "COMPARAÇÃO DE SIMULAÇÕES\n")
        text_comparacao.insert(tk.END, "=" * 140 + "\n\n")

        # Cabeçalho
        header = f"{'Simulação':<30} | {'Aporte Inicial':>15} | {'Aporte Mensal':>15} | {'Prazo':>8} | {'Saldo Final':>18} | {'Rentabilidade':>15}\n"
        text_comparacao.insert(tk.END, header)
        text_comparacao.insert(tk.END, "-" * 140 + "\n")

        # Dados
        for sim in comparacao['simulacoes']:
            if sim['calculada']:
                linha = f"{sim['nome'][:29]:<30} | R$ {sim['aporte_inicial']:>12,.2f} | R$ {sim['aporte_mensal']:>12,.2f} | {sim['prazo_meses']:>6} m | R$ {sim['saldo_final']:>15,.2f} | {sim['rentabilidade']:>13.2f}%\n"
            else:
                linha = f"{sim['nome'][:29]:<30} | R$ {sim['aporte_inicial']:>12,.2f} | R$ {sim['aporte_mensal']:>12,.2f} | {sim['prazo_meses']:>6} m | {'Não calculada':>18} | {'N/A':>15}\n"
            text_comparacao.insert(tk.END, linha)

        text_comparacao.insert(tk.END, "\n" + "=" * 140 + "\n")
        text_comparacao.config(state='disabled')

        # Aba 2: Gráfico Comparativo (se matplotlib disponível)
        if MATPLOTLIB_DISPONIVEL:
            tab_grafico = tk.Frame(notebook, bg=self.cores['bg_secundario'])
            notebook.add(tab_grafico, text="Gráfico Comparativo")

            fig = self.sistema.criar_grafico_comparacao(ids_selecionados)
            if fig:
                canvas = FigureCanvasTkAgg(fig, master=tab_grafico)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            else:
                ttk.Label(tab_grafico, text="Calcule pelo menos 2 simulações para ver o gráfico comparativo",
                         font=('Segoe UI', 12)).pack(pady=50)

        # Botão fechar
        ttk.Button(dialog, text="Fechar", command=dialog.destroy,
                  style='Accent.TButton').pack(pady=10)

    def limpar_campos(self):
        """Limpa campos de configuração"""
        self.entry_nome.delete(0, tk.END)
        self.entry_aporte_inicial.delete(0, tk.END)
        self.entry_aporte_mensal.delete(0, tk.END)
        self.entry_prazo.delete(0, tk.END)
        self.entry_taxa.delete(0, tk.END)
        self.tipo_taxa_var.set("FIXA")
        self.taxas_variaveis = None
        self.ao_mudar_tipo_taxa()


    def executar(self):
        """Executa a aplicação"""
        # Inicialização concluída

        # Inicia interface
        self.root.mainloop()

# Execução da aplicação
if __name__ == '__main__':
    app = InterfaceSimulador()
    app.executar()