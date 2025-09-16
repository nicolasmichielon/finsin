# ============================================================================
# SISTEMA DE SIMULAÇÃO DE INVESTIMENTOS
# Implementação em Python - Entrega 2
# ============================================================================

import json
import csv
import math
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

# ============================================================================
# ENUMS E TIPOS
# ============================================================================

class TipoTaxa(Enum):
    """Enum para tipos de taxa de retorno"""
    FIXA = "fixa"
    VARIAVEL = "variavel"

# ============================================================================
# CLASSES DE DOMÍNIO
# ============================================================================

@dataclass
class ResultadoMensal:
    """
    Representa o resultado de um mês específico da simulação.
    
    Attributes:
        mes: Número do mês (1, 2, 3, ...)
        aporte_mes: Valor do aporte no mês
        total_investido: Total acumulado investido até o mês
        juros_mes: Juros ganhos no mês
        juros_acumulados: Total de juros acumulados
        saldo_final: Saldo total no final do mês
    """
    mes: int
    aporte_mes: float
    total_investido: float
    juros_mes: float
    juros_acumulados: float
    saldo_final: float

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return asdict(self)

@dataclass
class Simulacao:
    """
    Classe principal que representa uma simulação de investimento.
    
    Attributes:
        id: Identificador único da simulação
        nome: Nome/título da simulação
        aporte_inicial: Valor do aporte inicial (deve ser > 0)
        aporte_mensal: Valor do aporte mensal recorrente
        prazo_meses: Prazo da simulação em meses (1-360)
        tipo_taxa: Tipo de taxa (FIXA ou VARIAVEL)
        taxa_fixa: Taxa fixa mensal (se tipo_taxa = FIXA)
        taxas_variaveis: Lista de taxas mensais (se tipo_taxa = VARIAVEL)
        resultados: Lista de resultados mensais calculados
        data_criacao: Data de criação da simulação
        data_modificacao: Data da última modificação
    """
    id: str
    nome: str
    aporte_inicial: float
    aporte_mensal: float
    prazo_meses: int
    tipo_taxa: TipoTaxa
    taxa_fixa: Optional[float] = None
    taxas_variaveis: Optional[List[float]] = None
    resultados: List[ResultadoMensal] = None
    data_criacao: datetime = None
    data_modificacao: datetime = None

    def __post_init__(self):
        """Inicializa campos padrão após criação"""
        if self.resultados is None:
            self.resultados = []
        if self.data_criacao is None:
            self.data_criacao = datetime.now()
        if self.data_modificacao is None:
            self.data_modificacao = datetime.now()

    def calcular(self) -> None:
        """
        Calcula a simulação aplicando juros compostos.
        Implementa UC03 - Calcular Simulação
        """
        self.resultados = CalculadoraInvestimento.calcular_projecao_mensal(self)
        self.data_modificacao = datetime.now()

    def validar(self) -> tuple[bool, List[str]]:
        """
        Valida a simulação conforme regras de negócio.
        
        Returns:
            Tupla (é_válida, lista_de_erros)
        """
        return ValidadorDados.validar_simulacao(self)

    def exportar_csv(self) -> str:
        """
        Exporta resultados para formato CSV.
        Implementa parte do UC06 - Exportar Dados
        
        Returns:
            String com conteúdo CSV
        """
        if not self.resultados:
            raise ValueError("Simulação deve ser calculada antes da exportação")
        
        return ExportadorRelatorio.exportar_csv(self.resultados)

    def to_dict(self) -> Dict[str, Any]:
        """Converte simulação para dicionário para serialização JSON"""
        data = asdict(self)
        data['tipo_taxa'] = self.tipo_taxa.value
        data['data_criacao'] = self.data_criacao.isoformat() if self.data_criacao else None
        data['data_modificacao'] = self.data_modificacao.isoformat() if self.data_modificacao else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Simulacao':
        """Cria simulação a partir de dicionário"""
        # Converte datas
        if data.get('data_criacao'):
            data['data_criacao'] = datetime.fromisoformat(data['data_criacao'])
        if data.get('data_modificacao'):
            data['data_modificacao'] = datetime.fromisoformat(data['data_modificacao'])
        
        # Converte enum
        data['tipo_taxa'] = TipoTaxa(data['tipo_taxa'])
        
        # Converte resultados
        if data.get('resultados'):
            data['resultados'] = [ResultadoMensal(**r) for r in data['resultados']]
        
        return cls(**data)

# ============================================================================
# CLASSES DE NEGÓCIO
# ============================================================================

class ValidadorDados:
    """
    Classe responsável por validar dados conforme regras de negócio.
    Implementa validações para UC02 - Configurar Parâmetros
    """
    
    @staticmethod
    def validar_aporte_inicial(valor: float) -> tuple[bool, str]:
        """
        Valida aporte inicial conforme RN01.
        
        Args:
            valor: Valor do aporte inicial
            
        Returns:
            Tupla (é_válido, mensagem_erro)
        """
        if valor is None or valor <= 0:
            return False, "Aporte inicial deve ser maior que R$ 0,00 (RN01)"
        return True, ""

    @staticmethod
    def validar_taxa_retorno(taxa: float) -> tuple[bool, str]:
        """
        Valida taxa de retorno conforme RN02.
        
        Args:
            taxa: Taxa de retorno mensal em porcentagem
            
        Returns:
            Tupla (é_válida, mensagem_erro)
        """
        if taxa is None or taxa < 0 or taxa > 100:
            return False, "Taxa de retorno deve estar entre 0% e 100% (RN02)"
        return True, ""

    @staticmethod
    def validar_prazo(meses: int) -> tuple[bool, str]:
        """
        Valida prazo conforme RN03.
        
        Args:
            meses: Prazo em meses
            
        Returns:
            Tupla (é_válido, mensagem_erro)
        """
        if meses is None or meses < 1 or meses > 360:
            return False, "Prazo deve estar entre 1 e 360 meses (RN03)"
        return True, ""

    @staticmethod
    def validar_campos_obrigatorios(simulacao: Simulacao) -> tuple[bool, List[str]]:
        """
        Valida campos obrigatórios conforme RN05.
        
        Args:
            simulacao: Simulação a ser validada
            
        Returns:
            Tupla (são_válidos, lista_erros)
        """
        erros = []
        
        if not simulacao.nome or not simulacao.nome.strip():
            erros.append("Nome da simulação é obrigatório (RN05)")
        
        if simulacao.aporte_inicial is None:
            erros.append("Aporte inicial é obrigatório (RN05)")
        
        if simulacao.prazo_meses is None:
            erros.append("Prazo é obrigatório (RN05)")
        
        if simulacao.tipo_taxa == TipoTaxa.FIXA and simulacao.taxa_fixa is None:
            erros.append("Taxa fixa é obrigatória quando tipo é FIXA (RN05)")
        
        if (simulacao.tipo_taxa == TipoTaxa.VARIAVEL and 
            (not simulacao.taxas_variaveis or len(simulacao.taxas_variaveis) == 0)):
            erros.append("Taxas variáveis são obrigatórias quando tipo é VARIAVEL (RN05)")
        
        return len(erros) == 0, erros

    @staticmethod
    def validar_simulacao(simulacao: Simulacao) -> tuple[bool, List[str]]:
        """
        Valida simulação completa aplicando todas as regras de negócio.
        
        Args:
            simulacao: Simulação a ser validada
            
        Returns:
            Tupla (é_válida, lista_erros)
        """
        erros = []
        
        # RN05 - Campos obrigatórios
        campos_validos, erros_campos = ValidadorDados.validar_campos_obrigatorios(simulacao)
        if not campos_validos:
            erros.extend(erros_campos)
            return False, erros  # Se campos obrigatórios faltam, não continua
        
        # RN01 - Aporte inicial
        aporte_valido, erro_aporte = ValidadorDados.validar_aporte_inicial(simulacao.aporte_inicial)
        if not aporte_valido:
            erros.append(erro_aporte)
        
        # RN03 - Prazo
        prazo_valido, erro_prazo = ValidadorDados.validar_prazo(simulacao.prazo_meses)
        if not prazo_valido:
            erros.append(erro_prazo)
        
        # RN02 - Taxas
        if simulacao.tipo_taxa == TipoTaxa.FIXA:
            taxa_valida, erro_taxa = ValidadorDados.validar_taxa_retorno(simulacao.taxa_fixa)
            if not taxa_valida:
                erros.append(erro_taxa)
        elif simulacao.tipo_taxa == TipoTaxa.VARIAVEL:
            for i, taxa in enumerate(simulacao.taxas_variaveis):
                taxa_valida, erro_taxa = ValidadorDados.validar_taxa_retorno(taxa)
                if not taxa_valida:
                    erros.append(f"Taxa variável {i+1}: {erro_taxa}")
        
        return len(erros) == 0, erros

class CalculadoraInvestimento:
    """
    Classe responsável pelos cálculos financeiros da simulação.
    Implementa UC03 - Calcular Simulação
    """
    
    @staticmethod
    def calcular_juros_compostos(capital: float, taxa_mensal: float, periodo: int) -> float:
        """
        Calcula juros compostos.
        
        Args:
            capital: Capital inicial
            taxa_mensal: Taxa de juros mensal (em decimal, ex: 0.01 para 1%)
            periodo: Período em meses
            
        Returns:
            Valor final com juros compostos
        """
        if taxa_mensal == 0:
            return capital
        return capital * ((1 + taxa_mensal) ** periodo)

    @staticmethod
    def aplicar_aporte_mensal(saldo: float, aporte: float) -> float:
        """
        Aplica aporte mensal ao saldo.
        
        Args:
            saldo: Saldo atual
            aporte: Valor do aporte mensal
            
        Returns:
            Novo saldo com aporte aplicado
        """
        return saldo + aporte

    @staticmethod
    def calcular_projecao_mensal(simulacao: Simulacao) -> List[ResultadoMensal]:
        """
        Calcula projeção mês a mês da simulação.
        
        Args:
            simulacao: Simulação a ser calculada
            
        Returns:
            Lista de resultados mensais
        """
        if not simulacao.validar()[0]:
            raise ValueError("Simulação inválida - não é possível calcular")
        
        resultados = []
        saldo_atual = simulacao.aporte_inicial
        total_investido = simulacao.aporte_inicial
        juros_acumulados = 0.0
        
        for mes in range(1, simulacao.prazo_meses + 1):
            # Determina taxa do mês
            if simulacao.tipo_taxa == TipoTaxa.FIXA:
                taxa_mes = simulacao.taxa_fixa / 100  # Converte % para decimal
            else:
                # Para taxa variável, usa a taxa do índice ou repete a última
                idx_taxa = min(mes - 1, len(simulacao.taxas_variaveis) - 1)
                taxa_mes = simulacao.taxas_variaveis[idx_taxa] / 100
            
            # Aplica juros sobre saldo atual
            juros_mes = saldo_atual * taxa_mes
            saldo_atual += juros_mes
            juros_acumulados += juros_mes
            
            # Aplica aporte mensal (exceto no primeiro mês se não definido diferente)
            aporte_mes = simulacao.aporte_mensal if simulacao.aporte_mensal else 0.0
            saldo_atual += aporte_mes
            total_investido += aporte_mes
            
            # Cria resultado do mês
            resultado = ResultadoMensal(
                mes=mes,
                aporte_mes=aporte_mes,
                total_investido=total_investido,
                juros_mes=juros_mes,
                juros_acumulados=juros_acumulados,
                saldo_final=saldo_atual
            )
            
            resultados.append(resultado)
        
        return resultados

class GerenciadorSimulacao:
    """
    Classe responsável pelo gerenciamento de simulações.
    Implementa UC01 - Gerenciar Simulação
    """
    
    def __init__(self):
        self.simulacoes: Dict[str, Simulacao] = {}
        self.simulacao_ativa: Optional[Simulacao] = None
        self._proximo_id = 1
    
    def _gerar_id(self) -> str:
        """Gera ID único para nova simulação"""
        id_simulacao = f"SIM{self._proximo_id:04d}"
        self._proximo_id += 1
        return id_simulacao
    
    def criar_simulacao(self, nome: str) -> Simulacao:
        """
        Cria nova simulação.
        
        Args:
            nome: Nome da simulação
            
        Returns:
            Nova simulação criada
        """
        if not nome or not nome.strip():
            raise ValueError("Nome da simulação é obrigatório")
        
        simulacao = Simulacao(
            id=self._gerar_id(),
            nome=nome.strip(),
            aporte_inicial=0.0,
            aporte_mensal=0.0,
            prazo_meses=1,
            tipo_taxa=TipoTaxa.FIXA,
            taxa_fixa=0.0
        )
        
        self.simulacoes[simulacao.id] = simulacao
        self.simulacao_ativa = simulacao
        
        return simulacao
    
    def editar_simulacao(self, id_simulacao: str) -> Simulacao:
        """
        Obtém simulação para edição.
        
        Args:
            id_simulacao: ID da simulação
            
        Returns:
            Simulação para edição
        """
        if id_simulacao not in self.simulacoes:
            raise ValueError(f"Simulação {id_simulacao} não encontrada")
        
        simulacao = self.simulacoes[id_simulacao]
        simulacao.data_modificacao = datetime.now()
        self.simulacao_ativa = simulacao
        
        return simulacao
    
    def excluir_simulacao(self, id_simulacao: str) -> None:
        """
        Exclui simulação.
        
        Args:
            id_simulacao: ID da simulação a ser excluída
        """
        if id_simulacao not in self.simulacoes:
            raise ValueError(f"Simulação {id_simulacao} não encontrada")
        
        # Se é a simulação ativa, limpa referência
        if (self.simulacao_ativa and 
            self.simulacao_ativa.id == id_simulacao):
            self.simulacao_ativa = None
        
        del self.simulacoes[id_simulacao]
    
    def listar_simulacoes(self) -> List[Simulacao]:
        """
        Lista todas as simulações.
        
        Returns:
            Lista de simulações ordenada por data de modificação
        """
        simulacoes = list(self.simulacoes.values())
        simulacoes.sort(key=lambda s: s.data_modificacao, reverse=True)
        return simulacoes
    
    def obter_simulacao(self, id_simulacao: str) -> Optional[Simulacao]:
        """
        Obtém simulação por ID.
        
        Args:
            id_simulacao: ID da simulação
            
        Returns:
            Simulação encontrada ou None
        """
        return self.simulacoes.get(id_simulacao)
    
    def salvar_arquivo(self, simulacao: Simulacao, caminho: str) -> None:
        """
        Salva simulação em arquivo JSON.
        Implementa parte do UC07 - Salvar/Carregar Simulação
        
        Args:
            simulacao: Simulação a ser salva
            caminho: Caminho do arquivo
        """
        try:
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                json.dump(simulacao.to_dict(), arquivo, ensure_ascii=False, indent=2)
        except Exception as e:
            raise IOError(f"Erro ao salvar arquivo: {str(e)}")
    
    def carregar_arquivo(self, caminho: str) -> Simulacao:
        """
        Carrega simulação de arquivo JSON.
        Implementa parte do UC07 - Salvar/Carregar Simulação
        
        Args:
            caminho: Caminho do arquivo
            
        Returns:
            Simulação carregada
        """
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            
            simulacao = Simulacao.from_dict(dados)
            
            # Adiciona ao gerenciador se não existe
            if simulacao.id not in self.simulacoes:
                self.simulacoes[simulacao.id] = simulacao
                # Atualiza contador de IDs
                try:
                    num_id = int(simulacao.id[3:])  # Remove "SIM" do início
                    if num_id >= self._proximo_id:
                        self._proximo_id = num_id + 1
                except:
                    pass
            
            self.simulacao_ativa = simulacao
            return simulacao
            
        except Exception as e:
            raise IOError(f"Erro ao carregar arquivo: {str(e)}")
    
    def pode_comparar(self) -> tuple[bool, str]:
        """
        Verifica se pode fazer comparação conforme RN04.
        
        Returns:
            Tupla (pode_comparar, mensagem)
        """
        if len(self.simulacoes) < 2:
            return False, "É necessário ter pelo menos 2 simulações para comparar (RN04)"
        return True, ""

class ComparacaoResultado:
    """
    Classe que representa resultado de comparação entre simulações.
    Implementa parte do UC05 - Comparar Simulações
    """
    
    def __init__(self, simulacoes: List[Simulacao]):
        self.simulacoes = simulacoes
        self.metricas = self._calcular_metricas()
    
    def _calcular_metricas(self) -> Dict[str, Dict[str, float]]:
        """Calcula métricas de comparação"""
        metricas = {}
        
        for simulacao in self.simulacoes:
            if not simulacao.resultados:
                continue
            
            ultimo_resultado = simulacao.resultados[-1]
            
            metricas[simulacao.nome] = {
                'saldo_final': ultimo_resultado.saldo_final,
                'total_investido': ultimo_resultado.total_investido,
                'rentabilidade_total': ((ultimo_resultado.saldo_final / ultimo_resultado.total_investido - 1) * 100),
                'juros_acumulados': ultimo_resultado.juros_acumulados,
                'prazo_meses': simulacao.prazo_meses
            }
        
        return metricas
    
    def obter_melhor_rentabilidade(self) -> tuple[str, float]:
        """Retorna simulação com melhor rentabilidade"""
        melhor = max(self.metricas.items(), 
                    key=lambda x: x[1]['rentabilidade_total'])
        return melhor[0], melhor[1]['rentabilidade_total']
    
    def obter_maior_saldo(self) -> tuple[str, float]:
        """Retorna simulação com maior saldo final"""
        melhor = max(self.metricas.items(), 
                    key=lambda x: x[1]['saldo_final'])
        return melhor[0], melhor[1]['saldo_final']

class ComparadorSimulacao:
    """
    Classe responsável por comparar simulações.
    Implementa UC05 - Comparar Simulações
    """
    
    @staticmethod
    def comparar_simulacoes(simulacoes: List[Simulacao]) -> ComparacaoResultado:
        """
        Compara múltiplas simulações.
        
        Args:
            simulacoes: Lista de simulações a comparar (máximo 3)
            
        Returns:
            Resultado da comparação
        """
        if len(simulacoes) < 2:
            raise ValueError("É necessário pelo menos 2 simulações para comparar (RN04)")
        
        if len(simulacoes) > 3:
            raise ValueError("Máximo de 3 simulações podem ser comparadas")
        
        # Verifica se todas as simulações foram calculadas
        for simulacao in simulacoes:
            if not simulacao.resultados:
                raise ValueError(f"Simulação '{simulacao.nome}' deve ser calculada antes da comparação")
        
        return ComparacaoResultado(simulacoes)

class ExportadorRelatorio:
    """
    Classe responsável por exportar relatórios.
    Implementa UC06 - Exportar Dados
    """
    
    @staticmethod
    def exportar_csv(resultados: List[ResultadoMensal]) -> str:
        """
        Exporta resultados para CSV.
        
        Args:
            resultados: Lista de resultados mensais
            
        Returns:
            String com conteúdo CSV
        """
        if not resultados:
            raise ValueError("Nenhum resultado para exportar")
        
        # Cabeçalho CSV
        linhas = [
            "Mês,Aporte do Mês,Total Investido,Juros do Mês,Juros Acumulados,Saldo Final"
        ]
        
        # Dados
        for resultado in resultados:
            linha = (
                f"{resultado.mes},"
                f"{resultado.aporte_mes:.2f},"
                f"{resultado.total_investido:.2f},"
                f"{resultado.juros_mes:.2f},"
                f"{resultado.juros_acumulados:.2f},"
                f"{resultado.saldo_final:.2f}"
            )
            linhas.append(linha)
        
        return "\n".join(linhas)
    
    @staticmethod
    def salvar_csv(resultados: List[ResultadoMensal], caminho: str) -> None:
        """
        Salva resultados em arquivo CSV.
        
        Args:
            resultados: Lista de resultados mensais
            caminho: Caminho do arquivo
        """
        conteudo_csv = ExportadorRelatorio.exportar_csv(resultados)
        
        try:
            with open(caminho, 'w', encoding='utf-8', newline='') as arquivo:
                arquivo.write(conteudo_csv)
        except Exception as e:
            raise IOError(f"Erro ao salvar CSV: {str(e)}")
    
    @staticmethod
    def gerar_relatorio_pdf(simulacao: Simulacao) -> str:
        """
        Gera relatório em formato texto (simulação de PDF).
        
        Args:
            simulacao: Simulação para gerar relatório
            
        Returns:
            Conteúdo do relatório em texto
        """
        if not simulacao.resultados:
            raise ValueError("Simulação deve ser calculada antes de gerar relatório")
        
        ultimo_resultado = simulacao.resultados[-1]
        
        relatorio = f"""
RELATÓRIO DE SIMULAÇÃO DE INVESTIMENTOS
========================================

Nome da Simulação: {simulacao.nome}
Data de Criação: {simulacao.data_criacao.strftime('%d/%m/%Y %H:%M')}
Data do Relatório: {datetime.now().strftime('%d/%m/%Y %H:%M')}

PARÂMETROS DA SIMULAÇÃO
-----------------------
Aporte Inicial: R$ {simulacao.aporte_inicial:,.2f}
Aporte Mensal: R$ {simulacao.aporte_mensal:,.2f}
Prazo: {simulacao.prazo_meses} meses
Tipo de Taxa: {simulacao.tipo_taxa.value.upper()}
"""
        
        if simulacao.tipo_taxa == TipoTaxa.FIXA:
            relatorio += f"Taxa Fixa: {simulacao.taxa_fixa:.2f}% ao mês\n"
        else:
            relatorio += f"Taxas Variáveis: {', '.join([f'{t:.2f}%' for t in simulacao.taxas_variaveis])}\n"
        
        relatorio += f"""
RESULTADOS FINAIS
-----------------
Saldo Final: R$ {ultimo_resultado.saldo_final:,.2f}
Total Investido: R$ {ultimo_resultado.total_investido:,.2f}
Juros Acumulados: R$ {ultimo_resultado.juros_acumulados:,.2f}
Rentabilidade Total: {((ultimo_resultado.saldo_final / ultimo_resultado.total_investido - 1) * 100):.2f}%

RESUMO MENSAL (Últimos 12 meses)
--------------------------------
Mês    | Aporte     | Juros      | Saldo Final
-------|------------|------------|-------------
"""
        
        # Mostra últimos 12 meses ou todos se menos de 12
        inicio = max(0, len(simulacao.resultados) - 12)
        for resultado in simulacao.resultados[inicio:]:
            relatorio += f"{resultado.mes:6d} | R$ {resultado.aporte_mes:8,.2f} | R$ {resultado.juros_mes:8,.2f} | R$ {resultado.saldo_final:10,.2f}\n"
        
        return relatorio

# ============================================================================
# CLASSE PRINCIPAL DO SISTEMA
# ============================================================================

class SistemaSimulacaoInvestimentos:
    """
    Classe principal que integra todos os componentes do sistema.
    Serve como facade para as operações do sistema.
    """
    
    def __init__(self):
        self.gerenciador = GerenciadorSimulacao()
        self.versao = "1.0.0"
    
    # UC01 - Gerenciar Simulação
    def criar_simulacao(self, nome: str) -> str:
        """Cria nova simulação e retorna ID"""
        simulacao = self.gerenciador.criar_simulacao(nome)
        return simulacao.id
    
    def editar_simulacao(self, id_simulacao: str) -> bool:
        """Seleciona simulação para edição"""
        try:
            self.gerenciador.editar_simulacao(id_simulacao)
            return True
        except ValueError:
            return False
    
    def excluir_simulacao(self, id_simulacao: str) -> bool:
        """Exclui simulação"""
        try:
            self.gerenciador.excluir_simulacao(id_simulacao)
            return True
        except ValueError:
            return False
    
    def listar_simulacoes(self) -> List[Dict[str, Any]]:
        """Lista simulações com informações básicas"""
        simulacoes = self.gerenciador.listar_simulacoes()
        return [
            {
                'id': s.id,
                'nome': s.nome,
                'prazo_meses': s.prazo_meses,
                'data_criacao': s.data_criacao.strftime('%d/%m/%Y'),
                'calculada': len(s.resultados) > 0
            }
            for s in simulacoes
        ]
    
    # UC02 - Configurar Parâmetros
    def configurar_simulacao(self, id_simulacao: str, **kwargs) -> tuple[bool, List[str]]:
        """
        Configura parâmetros da simulação.
        
        Args:
            id_simulacao: ID da simulação
            **kwargs: Parâmetros a configurar (aporte_inicial, aporte_mensal, etc.)
            
        Returns:
            Tupla (sucesso, lista_erros)
        """
        simulacao = self.gerenciador.obter_simulacao(id_simulacao)
        if not simulacao:
            return False, [f"Simulação {id_simulacao} não encontrada"]
        
        # Atualiza parâmetros
        for campo, valor in kwargs.items():
            if hasattr(simulacao, campo):
                setattr(simulacao, campo, valor)
        
        # Valida simulação
        valida, erros = simulacao.validar()
        
        if valida:
            simulacao.data_modificacao = datetime.now()
            # Limpa resultados pois parâmetros mudaram
            simulacao.resultados = []
        
        return valida, erros
    
    # UC03 - Calcular Simulação
    def calcular_simulacao(self, id_simulacao: str) -> tuple[bool, List[str]]:
        """
        Calcula simulação aplicando juros compostos.
        
        Args:
            id_simulacao: ID da simulação a calcular
            
        Returns:
            Tupla (sucesso, lista_erros)
        """
        simulacao = self.gerenciador.obter_simulacao(id_simulacao)
        if not simulacao:
            return False, [f"Simulação {id_simulacao} não encontrada"]
        
        # Valida antes de calcular
        valida, erros = simulacao.validar()
        if not valida:
            return False, erros
        
        try:
            simulacao.calcular()
            return True, []
        except Exception as e:
            return False, [f"Erro ao calcular: {str(e)}"]
    
    # UC04 - Visualizar Resultados
    def obter_resultados(self, id_simulacao: str) -> Optional[Dict[str, Any]]:
        """
        Obtém resultados da simulação para visualização.
        
        Args:
            id_simulacao: ID da simulação
            
        Returns:
            Dicionário com resultados ou None se não encontrada
        """
        simulacao = self.gerenciador.obter_simulacao(id_simulacao)
        if not simulacao or not simulacao.resultados:
            return None
        
        ultimo_resultado = simulacao.resultados[-1]
        
        return {
            'simulacao': {
                'id': simulacao.id,
                'nome': simulacao.nome,
                'prazo_meses': simulacao.prazo_meses
            },
            'resultados_mensais': [r.to_dict() for r in simulacao.resultados],
            'metricas_finais': {
                'saldo_final': ultimo_resultado.saldo_final,
                'total_investido': ultimo_resultado.total_investido,
                'juros_acumulados': ultimo_resultado.juros_acumulados,
                'rentabilidade_total': ((ultimo_resultado.saldo_final / ultimo_resultado.total_investido - 1) * 100)
            }
        }
    
    def obter_dados_grafico(self, id_simulacao: str) -> Optional[Dict[str, List[Any]]]:
        """
        Obtém dados formatados para geração de gráfico.
        
        Args:
            id_simulacao: ID da simulação
            
        Returns:
            Dicionário com dados para gráfico ou None
        """
        simulacao = self.gerenciador.obter_simulacao(id_simulacao)
        if not simulacao or not simulacao.resultados:
            return None
        
        meses = []
        saldos = []
        aportes_acumulados = []
        
        for resultado in simulacao.resultados:
            meses.append(resultado.mes)
            saldos.append(resultado.saldo_final)
            aportes_acumulados.append(resultado.total_investido)
        
        return {
            'meses': meses,
            'saldo_final': saldos,
            'total_investido': aportes_acumulados
        }
    
    # UC05 - Comparar Simulações
    def pode_comparar_simulacoes(self) -> tuple[bool, str]:
        """Verifica se pode fazer comparação"""
        return self.gerenciador.pode_comparar()
    
    def comparar_simulacoes(self, ids_simulacao: List[str]) -> Optional[Dict[str, Any]]:
        """
        Compara múltiplas simulações.
        
        Args:
            ids_simulacao: Lista de IDs das simulações a comparar
            
        Returns:
            Resultado da comparação ou None se erro
        """
        if len(ids_simulacao) < 2:
            return None
        
        simulacoes = []
        for id_sim in ids_simulacao:
            simulacao = self.gerenciador.obter_simulacao(id_sim)
            if simulacao and simulacao.resultados:
                simulacoes.append(simulacao)
        
        if len(simulacoes) < 2:
            return None
        
        try:
            comparacao = ComparadorSimulacao.comparar_simulacoes(simulacoes)
            
            # Formata resultado para interface
            resultado = {
                'simulacoes': [s.nome for s in comparacao.simulacoes],
                'metricas': comparacao.metricas,
                'melhor_rentabilidade': comparacao.obter_melhor_rentabilidade(),
                'maior_saldo': comparacao.obter_maior_saldo()
            }
            
            return resultado
            
        except Exception:
            return None
    
    # UC06 - Exportar Dados
    def exportar_csv(self, id_simulacao: str, caminho: str) -> tuple[bool, str]:
        """
        Exporta simulação para CSV.
        
        Args:
            id_simulacao: ID da simulação
            caminho: Caminho do arquivo
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        simulacao = self.gerenciador.obter_simulacao(id_simulacao)
        if not simulacao:
            return False, "Simulação não encontrada"
        
        if not simulacao.resultados:
            return False, "Simulação deve ser calculada antes da exportação"
        
        try:
            ExportadorRelatorio.salvar_csv(simulacao.resultados, caminho)
            return True, f"CSV exportado para {caminho}"
        except Exception as e:
            return False, f"Erro ao exportar CSV: {str(e)}"
    
    def gerar_relatorio_pdf(self, id_simulacao: str) -> tuple[bool, str]:
        """
        Gera relatório da simulação.
        
        Args:
            id_simulacao: ID da simulação
            
        Returns:
            Tupla (sucesso, conteudo_ou_erro)
        """
        simulacao = self.gerenciador.obter_simulacao(id_simulacao)
        if not simulacao:
            return False, "Simulação não encontrada"
        
        if not simulacao.resultados:
            return False, "Simulação deve ser calculada antes de gerar relatório"
        
        try:
            relatorio = ExportadorRelatorio.gerar_relatorio_pdf(simulacao)
            return True, relatorio
        except Exception as e:
            return False, f"Erro ao gerar relatório: {str(e)}"
    
    # UC07 - Salvar/Carregar Simulação
    def salvar_simulacao(self, id_simulacao: str, caminho: str) -> tuple[bool, str]:
        """
        Salva simulação em arquivo JSON.
        
        Args:
            id_simulacao: ID da simulação
            caminho: Caminho do arquivo
            
        Returns:
            Tupla (sucesso, mensagem)
        """
        simulacao = self.gerenciador.obter_simulacao(id_simulacao)
        if not simulacao:
            return False, "Simulação não encontrada"
        
        try:
            self.gerenciador.salvar_arquivo(simulacao, caminho)
            return True, f"Simulação salva em {caminho}"
        except Exception as e:
            return False, f"Erro ao salvar: {str(e)}"
    
    def carregar_simulacao(self, caminho: str) -> tuple[bool, str]:
        """
        Carrega simulação de arquivo JSON.
        
        Args:
            caminho: Caminho do arquivo
            
        Returns:
            Tupla (sucesso, id_simulacao_ou_erro)
        """
        try:
            simulacao = self.gerenciador.carregar_arquivo(caminho)
            return True, simulacao.id
        except Exception as e:
            return False, f"Erro ao carregar: {str(e)}"
    
    def obter_informacoes_sistema(self) -> Dict[str, Any]:
        """Retorna informações do sistema"""
        return {
            'versao': self.versao,
            'total_simulacoes': len(self.gerenciador.simulacoes),
            'simulacao_ativa': self.gerenciador.simulacao_ativa.id if self.gerenciador.simulacao_ativa else None
        }

# ============================================================================
# EXEMPLOS DE USO E TESTES
# ============================================================================

def exemplo_uso_completo():
    """
    Exemplo demonstrando uso completo do sistema.
    Pode ser usado como teste manual.
    """
    print("=== SISTEMA DE SIMULAÇÃO DE INVESTIMENTOS ===")
    print("Exemplo de uso completo do sistema\n")
    
    # Inicializa sistema
    sistema = SistemaSimulacaoInvestimentos()
    
    # UC01 - Criar simulação
    print("1. Criando simulação...")
    id_sim = sistema.criar_simulacao("Minha Aposentadoria")
    print(f"   Simulação criada com ID: {id_sim}")
    
    # UC02 - Configurar parâmetros
    print("\n2. Configurando parâmetros...")
    sucesso, erros = sistema.configurar_simulacao(
        id_sim,
        aporte_inicial=10000.0,
        aporte_mensal=1000.0,
        prazo_meses=120,
        tipo_taxa=TipoTaxa.FIXA,
        taxa_fixa=0.8
    )
    
    if sucesso:
        print("   Parâmetros configurados com sucesso!")
    else:
        print(f"   Erros na configuração: {erros}")
        return
    
    # UC03 - Calcular simulação
    print("\n3. Calculando simulação...")
    sucesso, erros = sistema.calcular_simulacao(id_sim)
    
    if sucesso:
        print("   Simulação calculada com sucesso!")
    else:
        print(f"   Erros no cálculo: {erros}")
        return
    
    # UC04 - Visualizar resultados
    print("\n4. Visualizando resultados...")
    resultados = sistema.obter_resultados(id_sim)
    
    if resultados:
        metricas = resultados['metricas_finais']
        print(f"   Saldo Final: R$ {metricas['saldo_final']:,.2f}")
        print(f"   Total Investido: R$ {metricas['total_investido']:,.2f}")
        print(f"   Rentabilidade: {metricas['rentabilidade_total']:.2f}%")
        
        # Mostra últimos 5 meses
        print("\n   Últimos 5 meses:")
        print("   Mês | Saldo Final")
        print("   ----|------------")
        for resultado in resultados['resultados_mensais'][-5:]:
            print(f"   {resultado['mes']:3d} | R$ {resultado['saldo_final']:9,.2f}")
    
    # Criar segunda simulação para demonstrar comparação
    print("\n5. Criando segunda simulação para comparação...")
    id_sim2 = sistema.criar_simulacao("Investimento Agressivo")
    
    sistema.configurar_simulacao(
        id_sim2,
        aporte_inicial=10000.0,
        aporte_mensal=1000.0,
        prazo_meses=120,
        tipo_taxa=TipoTaxa.FIXA,
        taxa_fixa=1.2  # Taxa maior
    )
    
    sistema.calcular_simulacao(id_sim2)
    print("   Segunda simulação criada e calculada!")
    
    # UC05 - Comparar simulações
    print("\n6. Comparando simulações...")
    pode_comparar, msg = sistema.pode_comparar_simulacoes()
    
    if pode_comparar:
        comparacao = sistema.comparar_simulacoes([id_sim, id_sim2])
        
        if comparacao:
            print("   Comparação realizada:")
            print(f"   Melhor rentabilidade: {comparacao['melhor_rentabilidade'][0]} ({comparacao['melhor_rentabilidade'][1]:.2f}%)")
            print(f"   Maior saldo final: {comparacao['maior_saldo'][0]} (R$ {comparacao['maior_saldo'][1]:,.2f})")
    else:
        print(f"   Não é possível comparar: {msg}")
    
    # UC06 - Exportar dados
    print("\n7. Exportando dados...")
    sucesso, msg = sistema.exportar_csv(id_sim, "simulacao_exemplo.csv")
    print(f"   CSV: {msg}")
    
    sucesso, relatorio = sistema.gerar_relatorio_pdf(id_sim)
    if sucesso:
        print("   Relatório PDF gerado com sucesso!")
        print("   Primeiras linhas do relatório:")
        linhas = relatorio.split('\n')[:10]
        for linha in linhas:
            print(f"   {linha}")
        print("   ...")
    else:
        print(f"   Erro no relatório: {relatorio}")
    
    # UC07 - Salvar simulação
    print("\n8. Salvando simulação...")
    sucesso, msg = sistema.salvar_simulacao(id_sim, "minha_simulacao.json")
    print(f"   {msg}")
    
    print("\n=== EXEMPLO CONCLUÍDO ===")
    
    return sistema

def testes_validacao():
    """
    Testes das validações e regras de negócio.
    """
    print("\n=== TESTES DE VALIDAÇÃO ===")
    
    sistema = SistemaSimulacaoInvestimentos()
    
    # Teste RN01 - Aporte inicial obrigatório
    print("\n1. Testando RN01 - Aporte inicial obrigatório")
    id_sim = sistema.criar_simulacao("Teste RN01")
    
    sucesso, erros = sistema.configurar_simulacao(
        id_sim,
        aporte_inicial=0.0,  # Valor inválido
        prazo_meses=12,
        tipo_taxa=TipoTaxa.FIXA,
        taxa_fixa=1.0
    )
    
    print(f"   Configuração com aporte 0: {'FALHOU' if not sucesso else 'PASSOU'}")
    if not sucesso:
        print(f"   Erros: {erros}")
    
    # Teste RN02 - Taxa entre 0% e 100%
    print("\n2. Testando RN02 - Taxa entre 0% e 100%")
    sucesso, erros = sistema.configurar_simulacao(
        id_sim,
        aporte_inicial=1000.0,
        taxa_fixa=150.0  # Taxa inválida
    )
    
    print(f"   Taxa 150%: {'FALHOU' if not sucesso else 'PASSOU'}")
    if not sucesso:
        print(f"   Erros: {erros}")
    
    # Teste RN03 - Prazo entre 1 e 360 meses
    print("\n3. Testando RN03 - Prazo entre 1 e 360 meses")
    sucesso, erros = sistema.configurar_simulacao(
        id_sim,
        taxa_fixa=1.0,
        prazo_meses=500  # Prazo inválido
    )
    
    print(f"   Prazo 500 meses: {'FALHOU' if not sucesso else 'PASSOU'}")
    if not sucesso:
        print(f"   Erros: {erros}")
    
    # Teste RN04 - Comparação com mínimo 2 simulações
    print("\n4. Testando RN04 - Comparação com mínimo 2 simulações")
    # Sistema tem apenas 1 simulação
    pode_comparar, msg = sistema.pode_comparar_simulacoes()
    print(f"   Comparação com 1 simulação: {'FALHOU' if not pode_comparar else 'PASSOU'}")
    print(f"   Mensagem: {msg}")
    
    # Teste RN05 - Campos obrigatórios
    print("\n5. Testando RN05 - Campos obrigatórios")
    id_sim2 = sistema.criar_simulacao("")  # Nome vazio - deveria falhar
    
    print("=== TESTES DE VALIDAÇÃO CONCLUÍDOS ===")

def demonstracao_casos_uso():
    """
    Demonstração específica de cada caso de uso.
    """
    print("\n=== DEMONSTRAÇÃO DOS CASOS DE USO ===")
    
    sistema = SistemaSimulacaoInvestimentos()
    
    print("\nUC01 - Gerenciar Simulação")
    print("-" * 30)
    
    # Criar
    id1 = sistema.criar_simulacao("Simulação Teste 1")
    id2 = sistema.criar_simulacao("Simulação Teste 2")
    print(f"Criadas simulações: {id1}, {id2}")
    
    # Listar
    simulacoes = sistema.listar_simulacoes()
    print(f"Total de simulações: {len(simulacoes)}")
    
    # Editar
    sucesso = sistema.editar_simulacao(id1)
    print(f"Edição de {id1}: {'Sucesso' if sucesso else 'Falha'}")
    
    # Excluir
    sucesso = sistema.excluir_simulacao(id2)
    print(f"Exclusão de {id2}: {'Sucesso' if sucesso else 'Falha'}")
    
    print("\nUC02 - Configurar Parâmetros")
    print("-" * 30)
    
    # Configuração válida
    sucesso, erros = sistema.configurar_simulacao(
        id1,
        aporte_inicial=5000.0,
        aporte_mensal=500.0,
        prazo_meses=60,
        tipo_taxa=TipoTaxa.FIXA,
        taxa_fixa=0.7
    )
    print(f"Configuração: {'Sucesso' if sucesso else 'Falha'}")
    if not sucesso:
        print(f"Erros: {erros}")
    
    print("\nUC03 - Calcular Simulação")
    print("-" * 30)
    
    sucesso, erros = sistema.calcular_simulacao(id1)
    print(f"Cálculo: {'Sucesso' if sucesso else 'Falha'}")
    if not sucesso:
        print(f"Erros: {erros}")
    
    print("\nUC04 - Visualizar Resultados")
    print("-" * 30)
    
    resultados = sistema.obter_resultados(id1)
    if resultados:
        print("Resultados obtidos com sucesso!")
        print(f"Saldo final: R$ {resultados['metricas_finais']['saldo_final']:,.2f}")
    else:
        print("Falha ao obter resultados")
    
    dados_grafico = sistema.obter_dados_grafico(id1)
    if dados_grafico:
        print(f"Dados para gráfico: {len(dados_grafico['meses'])} pontos")
    
    print("\nUC05 - Comparar Simulações")
    print("-" * 30)
    
    # Criar segunda simulação para comparar
    id3 = sistema.criar_simulacao("Simulação Comparação")
    sistema.configurar_simulacao(
        id3,
        aporte_inicial=5000.0,
        aporte_mensal=500.0,
        prazo_meses=60,
        tipo_taxa=TipoTaxa.FIXA,
        taxa_fixa=1.0  # Taxa diferente
    )
    sistema.calcular_simulacao(id3)
    
    comparacao = sistema.comparar_simulacoes([id1, id3])
    if comparacao:
        print("Comparação realizada com sucesso!")
        print(f"Simulações: {comparacao['simulacoes']}")
    else:
        print("Falha na comparação")
    
    print("\nUC06 - Exportar Dados")
    print("-" * 30)
    
    sucesso, msg = sistema.exportar_csv(id1, "teste.csv")
    print(f"Exportação CSV: {msg}")
    
    sucesso, relatorio = sistema.gerar_relatorio_pdf(id1)
    print(f"Relatório PDF: {'Gerado' if sucesso else 'Falha'}")
    
    print("\nUC07 - Salvar/Carregar Simulação")
    print("-" * 30)
    
    sucesso, msg = sistema.salvar_simulacao(id1, "teste_simulacao.json")
    print(f"Salvamento: {msg}")
    
    sucesso, resultado = sistema.carregar_simulacao("teste_simulacao.json")
    print(f"Carregamento: {'Sucesso - ID: ' + resultado if sucesso else 'Falha: ' + resultado}")
    
    print("\n=== DEMONSTRAÇÃO CONCLUÍDA ===")

# ============================================================================
# EXECUÇÃO DE EXEMPLO (SE EXECUTADO DIRETAMENTE)
# ============================================================================

if __name__ == "__main__":
    print("Sistema de Simulação de Investimentos - Versão 1.0.0")
    print("=" * 60)
    
    # Executa exemplo completo
    sistema = exemplo_uso_completo()

    # Demonstra casos de uso
    demonstracao_casos_uso()
    
    print(f"\nInformações do sistema: {sistema.obter_informacoes_sistema()}")
    print("\nExecução concluída com sucesso!")