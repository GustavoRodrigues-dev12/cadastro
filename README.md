## 📝 Documentação README.md e Sugestões de Commits

Aqui está uma documentação completa no formato **README.md** para o seu projeto Mini-ERP de Estoque e uma sugestão de **histórico de commits** para formalizar o desenvolvimento.

-----

## 📄 README.md - Mini-ERP Módulo de Estoque

### 📚 Visão Geral do Projeto

Este projeto é uma simulação simplificada do **Módulo de Estoque** de um sistema **ERP (Enterprise Resource Planning)**, desenvolvido em Python. O objetivo é demonstrar conceitos fundamentais de gestão de estoque, incluindo cadastro de produtos, controle de movimentação (entrada/saída) e geração de relatórios gerenciais, como a Curva ABC.

### 🎯 Funcionalidades Implementadas

O sistema oferece um menu interativo com as seguintes opções de gestão de estoque:

  * **Cadastro de Produtos:** Permite incluir novos itens no estoque, registrando **nome, categoria, preço** e **quantidade inicial**.
  * **Exclusão de Produtos:** Remove itens do sistema utilizando seu ID ou nome.
  * **Movimentação de Estoque:** Registra as operações de **Entrada** (compra/reposição) e **Saída** (venda/consumo), atualizando a quantidade em tempo real.
  * **Relatório Básico:** Lista todos os produtos, detalhando seus atributos e destacando produtos com **estoque baixo (quantidade \< 5)**.
  * **Relatório Gerencial (Curva ABC e Custo Total):** Calcula o **Custo Total de Manutenção de Estoque** (valor monetário total) e aplica a **Curva ABC** para classificar os produtos por sua relevância de valor (A, B e C), auxiliando na priorização da gestão.

### 🛠️ Tecnologias Utilizadas

  * **Linguagem de Programação:** Python
  * **Estruturas de Dados:** Listas e Dicionários (simulando um banco de dados).
  * **Bibliotecas:**
      * `pandas` (Opcional, mas **necessário** para o cálculo completo e a exibição formatada da **Curva ABC**).
      * `datetime` (Para registro de data e hora nas movimentações).

### 🚀 Como Executar o Projeto

#### 1\. Pré-requisitos

Certifique-se de ter o Python instalado em seu sistema. Para utilizar a funcionalidade completa da Curva ABC, você deve instalar a biblioteca `pandas`:

```bash
pip install pandas
```

#### 2\. Execução

1.  Salve o código principal em um arquivo chamado `main.py` (ou nome similar).
2.  Abra o terminal na pasta onde o arquivo foi salvo.
3.  Execute o script:

<!-- end list -->

```bash
python main.py
```

O sistema exibirá o menu principal, permitindo que você comece a cadastrar e gerenciar produtos.

### 📂 Estrutura do Código

O código é modularizado em funções para cada operação:

| Função | Descrição |
| :--- | :--- |
| `menu_principal()` | Gerencia o fluxo de navegação. |
| `cadastrar_produto()` | Implementa o requisito de cadastro. |
| `excluir_produto()` | Implementa a remoção de itens. |
| `movimentar_estoque()` | Controla as entradas e saídas e registra o histórico. |
| `mostrar_relatorio_produtos()` | Gera o relatório básico com destaque para estoque baixo. |
| `relatorio_custo_estoque()` | Calcula o valor total do estoque e gera a Curva ABC. |
| `estoque` (Lista Global) | Armazena os produtos como dicionários. |
| `historico_movimentacoes` (Lista Global) | Registra as transações de entrada e saída. |

-----

## 🗃️ Sugestões de Histórico de Commits

Abaixo está um histórico sugerido de commits para formalizar as etapas de desenvolvimento do projeto, seguindo a convenção **Tipo(Escopo): Descrição**.

| Tipo | Escopo | Descrição |
| :--- | :--- | :--- |
| **feat** | `core` | Inicializa projeto e estrutura principal do menu. |
| **feat** | `cadastro` | Implementa a função de cadastrar produto e geração de ID. |
| **feat** | `exclusao` | Adiciona funcionalidade para excluir produto por ID ou nome. |
| **feat** | `relatorio` | Implementa relatório básico de produtos e destaque para estoque baixo. |
| **feat** | `movimentacao` | Adiciona função para movimentar estoque (Entrada/Saída) e registro de histórico. |
| **feat** | `gerencial` | Implementa o relatório de Custo Total de Estoque e lógica da Curva ABC. |
| **fix** | `relatorio` | Trata exceção para importação de pandas na Curva ABC, fornecendo fallback. |
| **style** | `menu` | Ajusta formatação e alinhamento do menu e relatórios para clareza. |
| **docs** | `readme` | Cria documentação inicial README.md. |

Este histórico representa uma progressão lógica do desenvolvimento, desde a estrutura inicial até as funcionalidades mais complexas e a documentação final.
