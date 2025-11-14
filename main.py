import pandas as pd
from datetime import datetime

# --- Estruturas de Dados Globais ---
estoque = []
proximo_id = 1

# Histórico de Movimentações
historico_movimentacoes = []

def gerar_id():
    """Gera um ID único sequencial para o novo produto."""
    global proximo_id
    id_gerado = proximo_id
    proximo_id += 1
    return id_gerado

def buscar_produto(identificador):
    """Auxilia na busca de um produto pelo ID ou Nome."""
    # 1. Tenta encontrar pelo ID
    try:
        id_procurado = int(identificador)
        for produto in estoque:
            if produto['id'] == id_procurado:
                return produto
    except ValueError:
        # 2. Se não for numérico, tenta encontrar pelo Nome
        for produto in estoque:
            if produto['nome'].lower() == identificador.lower():
                return produto
    return None

# --- Funcionalidades do Módulo de Estoque ---

def cadastrar_produto():
    """Permite ao usuário cadastrar um novo produto no estoque."""
    print("\n--- Cadastro de Novo Produto ---")
    nome = input("Nome do produto: ").strip()
    
    for produto in estoque:
        if produto['nome'].lower() == nome.lower():
            print(f"ERRO: O produto '{nome}' já está cadastrado (ID: {produto['id']}).")
            return
            
    categoria = input("Categoria (ex: Eletrônicos, Alimentos, Vestuário): ").strip()
    
    while True:
        try:
            preco = float(input("Preço unitário (ex: 19.99): "))
            if preco <= 0: raise ValueError
            break
        except ValueError:
            print("Entrada inválida. Digite um preço positivo válido.")
            
    while True:
        try:
            quantidade = int(input("Quantidade inicial em estoque: "))
            if quantidade < 0: raise ValueError
            break
        except ValueError:
            print("Entrada inválida. Digite uma quantidade inteira não negativa.")

    novo_produto = {
        'id': gerar_id(),
        'nome': nome,
        'categoria': categoria,
        'preco': preco,
        'quantidade': quantidade
    }
    
    estoque.append(novo_produto)
    print(f"\nProduto '{nome}' cadastrado com sucesso! ID: {novo_produto['id']}")

def excluir_produto():
    """Permite remover um produto pelo ID ou nome."""
    print("\n--- Excluir Produto ---")
    if not estoque:
        print("Estoque vazio. Não há produtos para excluir.")
        return

    identificador = input("Digite o ID do produto ou o nome para excluir: ").strip()
    produto_para_remover = buscar_produto(identificador)

    if produto_para_remover:
        estoque.remove(produto_para_remover)
        print(f"\nProduto '{produto_para_remover['nome']}' (ID: {produto_para_remover['id']}) foi removido com sucesso.")
    else:
        print(f"\nProduto com ID/Nome '{identificador}' não encontrado.")

def movimentar_estoque():
    """Permite registrar entrada ou saída de um produto."""
    print("\n--- Movimentação de Estoque ---")
    if not estoque:
        print("Estoque vazio. Cadastre um produto primeiro.")
        return

    identificador = input("Digite o ID ou Nome do produto a movimentar: ").strip()
    produto = buscar_produto(identificador)

    if not produto:
        print(f"Produto '{identificador}' não encontrado.")
        return

    print(f"\nProduto selecionado: {produto['nome']} (Estoque atual: {produto['quantidade']})")
    
    while True:
        tipo = input("Tipo de movimento (E para Entrada / S para Saída): ").strip().upper()
        if tipo in ['E', 'S']:
            break
        print("Escolha inválida. Digite 'E' ou 'S'.")

    while True:
        try:
            quantidade = int(input("Quantidade a movimentar: "))
            if quantidade <= 0: raise ValueError
            break
        except ValueError:
            print("Entrada inválida. Digite uma quantidade inteira positiva.")

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if tipo == 'E':
        produto['quantidade'] += quantidade
        movimento_tipo = "ENTRADA"
        print(f"\nENTRADA de {quantidade} unidades de '{produto['nome']}' registrada.")
    
    elif tipo == 'S':
        if produto['quantidade'] < quantidade:
            print(f"\nERRO: Não é possível dar saída em {quantidade} unidades. Estoque atual: {produto['quantidade']}.")
            return
        
        produto['quantidade'] -= quantidade
        movimento_tipo = "SAÍDA"
        print(f"\nSAÍDA de {quantidade} unidades de '{produto['nome']}' registrada.")

    historico_movimentacoes.append({
        'produto_id': produto['id'],
        'nome': produto['nome'],
        'tipo': movimento_tipo,
        'quantidade': quantidade,
        'data': data_hora
    })
    print(f"Novo estoque de '{produto['nome']}': {produto['quantidade']}")

# --- Relatórios ---

def mostrar_relatorio_produtos():
    """Lista todos os produtos e destaca aqueles com estoque baixo."""
    print("\n--- Relatório Básico de Estoque ---")
    if not estoque:
        print("Estoque vazio. Nenhum produto cadastrado.")
        return

    print(f"{'ID':<4} | {'Nome':<30} | {'Categoria':<15} | {'Preço':>10} | {'Qtde':>6} | {'Status'}")
    print("-" * 75)
    
    produtos_com_estoque_baixo = 0
    LIMITE_ESTOQUE_BAIXO = 5
    
    for produto in estoque:
        id_prod = produto['id']
        nome_prod = produto['nome']
        cat_prod = produto['categoria']
        preco_prod = f"R$ {produto['preco']:.2f}"
        qtde_prod = produto['quantidade']
        
        status = ""
        if qtde_prod < LIMITE_ESTOQUE_BAIXO:
            status = "**ESTOQUE BAIXO**"
            produtos_com_estoque_baixo += 1
            # Código ANSI para cor vermelha (destaque)
            linha = f"{id_prod:<4} | {nome_prod:<30} | {cat_prod:<15} | {preco_prod:>10} | {qtde_prod:>6} | {status}"
            print(f"\033[91m{linha}\033[0m") 
        else:
            linha = f"{id_prod:<4} | {nome_prod:<30} | {cat_prod:<15} | {preco_prod:>10} | {qtde_prod:>6} | {status}"
            print(linha)

    print("-" * 75)
    print(f"Total de produtos cadastrados: {len(estoque)}")
    print(f"Produtos com estoque baixo (<{LIMITE_ESTOQUE_BAIXO}): {produtos_com_estoque_baixo}")

def relatorio_custo_estoque():
    """
    Calcula o Custo Total de Estoque (valor monetário) 
    e realiza a Curva ABC.
    """
    print("\n--- Relatório Gerencial: Custo de Estoque e Curva ABC ---")
    if not estoque:
        print("Estoque vazio.")
        return

    # 1. Cálculo e preparo para Curva ABC
    dados_abc = []
    custo_total_geral = 0.0

    for produto in estoque:
        valor_total = produto['preco'] * produto['quantidade']
        custo_total_geral += valor_total
        dados_abc.append({
            'ID': produto['id'],
            'Produto': produto['nome'],
            'Quantidade': produto['quantidade'],
            'Preco': produto['preco'],
            'Valor_Total': valor_total
        })

    print(f"Custo Total de Estoque (Valor Monetário): R$ {custo_total_geral:.2f}")
    print("-" * 65)

    if custo_total_geral == 0:
        print("Não há valor monetário no estoque para calcular a Curva ABC.")
        return
        
    # 2. Implementação da Curva ABC
    try:
        df = pd.DataFrame(dados_abc)
        df = df.sort_values(by='Valor_Total', ascending=False).reset_index(drop=True)
        
        # Cálculo da participação percentual
        df['Participacao'] = (df['Valor_Total'] / custo_total_geral) * 100
        df['Acumulada'] = df['Participacao'].cumsum()

        # Classificação ABC (A=80%, B=15%, C=5%)
        def classificar_abc(acumulada):
            if acumulada <= 80:
                return 'A'
            elif acumulada <= 95: # 80 + 15 = 95
                return 'B'
            else:
                return 'C'

        df['Curva_ABC'] = df['Acumulada'].apply(classificar_abc)
        
        # 3. Exibição da Curva ABC
        print("### Curva ABC (Por Valor Total no Estoque) ###")
        
        # Formatação para exibição
        df['Valor_Total_Fmt'] = df['Valor_Total'].map('R$ {:,.2f}'.format)
        df['Participacao_Fmt'] = df['Participacao'].map('{:.2f}%'.format)
        df['Acumulada_Fmt'] = df['Acumulada'].map('{:.2f}%'.format)
        
        # Exibe as colunas principais
        print(df[['Curva_ABC', 'Produto', 'Valor_Total_Fmt', 'Participacao_Fmt', 'Acumulada_Fmt']].to_markdown(index=False))
        
        print("\n* A = Produtos que representam 80% do valor total (Maior prioridade de gestão).")
        print("* B = Próximos 15% do valor total.")
        print("* C = Restante 5% do valor total.")

    except ImportError:
        print("\nATENÇÃO: A biblioteca 'pandas' não está instalada.")
        print("Para o relatório completo da Curva ABC, instale com 'pip install pandas'.")
        
        # Relatório simplificado sem pandas
        dados_abc_simples = sorted(dados_abc, key=lambda x: x['Valor_Total'], reverse=True)
        print("ID | Produto | Valor Total")
        print("-" * 30)
        for item in dados_abc_simples:
             print(f"{item['ID']:<2} | {item['Produto']:<10} | R$ {item['Valor_Total']:.2f}")

# --- Menu Principal ---
def menu_principal():
    """Exibe o menu interativo e gerencia a navegação."""
    while True:
        print("\n" + "=" * 50)
        print("    Mini-ERP - Módulo de Estoque")
        print("=" * 50)
        print("1. Cadastrar produto")
        print("2. Excluir produto")
        print("3. Movimentar estoque (Entrada/Saída)")
        print("4. Relatório Básico de Produtos (Estoque Baixo)")
        print("5. Relatório Gerencial (Custo Total e Curva ABC)")
        print("6. Sair do programa")
        print("-" * 50)
        
        opcao = input("Escolha uma opção (1-6): ").strip()
        
        if opcao == '1':
            cadastrar_produto()
        elif opcao == '2':
            excluir_produto()
        elif opcao == '3':
            movimentar_estoque()
        elif opcao == '4':
            mostrar_relatorio_produtos()
        elif opcao == '5':
            relatorio_custo_estoque()
        elif opcao == '6':
            print("\nEncerrando o programa Mini-ERP. Até mais!")
            break
        else:
            print("\nOpção inválida. Por favor, digite um número de 1 a 6.")

# Inicia o programa
if __name__ == "__main__":
    menu_principal()
