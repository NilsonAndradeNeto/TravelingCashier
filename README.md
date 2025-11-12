# Caixeiro Viajante — Solução com Algoritmo Genético

Projeto desenvolvido em Python para resolver o **Problema do Caixeiro Viajante (TSP)** utilizando **Algoritmo Genético (AG)** com interface gráfica em **Tkinter**.  
O sistema busca a rota mais curta possível entre um conjunto de cidades, exibindo o progresso do algoritmo, histórico de gerações e gráfico de evolução da distância.

---

## Como Executar o Projeto

### Pré-requisitos
- Python 3.10+
- Bibliotecas:
  pip install numpy matplotlib

### Execução
  python main.py

---

## Estrutura
- Tkinter: Interface gráfica moderna e responsiva  
- NumPy: Manipulação da matriz de distâncias  
- Matplotlib: Geração de gráficos de convergência  
- Algoritmo Genético: Implementado com elitismo, torneio e mutação adaptativa  

---

## Modelagem do Algoritmo Genético

Cidade Máxima: 20  
População: adaptativa (+25% por cidade após o fatorial)

---

### 1. População

Cada cromossomo representa uma rota completa entre as cidades.  
Exemplo:  
[0, 2, 3, 1, 4] → 0 → 2 → 3 → 1 → 4 → 0

A população é inicializada aleatoriamente, gerando rotas diversas e válidas.  
O objetivo é garantir diversidade inicial e aumentar as chances de encontrar soluções de alta qualidade.

---

### 2. Condição de Parada

O algoritmo é executado até atingir o limite de gerações consecutivas sem melhoria.  
Esse critério de estagnação evita gasto computacional quando o melhor resultado já foi encontrado, encerrando a execução de forma inteligente.

---

### 3. Geração

Cada geração representa um ciclo evolutivo que cria uma nova população a partir da anterior.  
O processo envolve:

- Cálculo do fitness (qualidade de cada rota)  
- Seleção dos melhores indivíduos  
- Cruzamento entre pais selecionados  
- Mutação aleatória controlada  
- Substituição dos indivíduos antigos  

É utilizado elitismo, garantindo que o melhor indivíduo de cada geração nunca seja perdido.

---

### 4. Método de Seleção

Método escolhido: Seleção por Torneio (com Elitismo)  

- Seleciona-se aleatoriamente um grupo de k indivíduos (ex: k=3)  
- O indivíduo com menor distância (melhor fitness) é escolhido como pai  

Esse método equilibra exploração e estabilidade, permitindo que boas rotas tenham mais chance de gerar descendentes.

---

### 5. Método de Cruzamento

Método escolhido: Order Crossover (OX) — Cruzamento de Ordem  

Passos:
1. Escolhem-se dois pontos de corte aleatórios  
2. Copia-se o segmento correspondente do Pai 1 para o filho  
3. Preenche-se o restante com as cidades do Pai 2, respeitando a ordem e sem repetições  

Exemplo:
Pai 1: [0, 1, 2, 3, 4, 5, 6]
Pai 2: [3, 4, 6, 0, 1, 2, 5]
Corte: (2, 5)
Filho: [6, 0, 2, 3, 4, 1, 5]

Esse processo combina boas rotas sem perder a estrutura lógica do problema.

---

### 6. Método de Mutação

Método escolhido: Troca de posição (Swap Mutation)  

- Seleciona duas cidades aleatórias e troca suas posições na rota  
- Mantém a validade do percurso (todas as cidades aparecem uma vez)  

Exemplo:
Antes: [0, 1, 2, 3, 4]
Depois: [0, 3, 2, 1, 4]

A mutação é essencial para evitar mínimos locais e preservar a diversidade genética da população.

---

### 7. Mecanismo de Seleção de Sobreviventes

Método utilizado: Elitismo  

O melhor indivíduo da geração atual é copiado diretamente para a próxima geração.  
Esse mecanismo garante que a melhor solução encontrada nunca se perca, acelerando a convergência do algoritmo.

---

## Conclusão

O projeto apresenta uma implementação prática e visual do algoritmo genético aplicado ao problema do caixeiro viajante, unindo eficiência, clareza e interatividade.  
A solução equilibra exploração e elitismo, demonstrando na prática como técnicas evolutivas podem otimizar problemas complexos de rota.

---

## Créditos

Desenvolvido por **[Nilson Andrade Neto | Kauan Adami]** — Ciência da Computação — UNIVALI  
2025

