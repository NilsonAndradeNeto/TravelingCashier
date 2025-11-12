import tkinter as tk
from tkinter import ttk, messagebox
import random
import numpy as np
import time
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def definir_populacao(num_cidades):
    if num_cidades <= 5:
        return math.factorial(num_cidades)
    else:
        pop = 120
        for _ in range(6, num_cidades + 1):
            pop *= 1.25
        return int(pop)


def calcular_distancia(rota, matriz):
    total = 0
    for i in range(len(rota) - 1):
        total += matriz[rota[i], rota[i + 1]]
    total += matriz[rota[-1], rota[0]]
    return total


def gerar_rota(num_cidades):
    rota = list(range(num_cidades))
    random.shuffle(rota)
    return rota


def selecao_torneio(pop, matriz, k=3):
    competidores = random.sample(pop, min(k, len(pop)))
    competidores.sort(key=lambda x: calcular_distancia(x, matriz))
    return competidores[0]


def crossover(pai1, pai2):
    tamanho = len(pai1)
    i, j = sorted(random.sample(range(tamanho), 2))
    filho = [None] * tamanho
    filho[i:j] = pai1[i:j]
    pos = j
    for cidade in pai2:
        if cidade not in filho:
            if pos >= tamanho:
                pos = 0
            filho[pos] = cidade
            pos += 1
    return filho


def mutacao(rota, taxa):
    for i in range(len(rota)):
        if random.random() < taxa:
            j = random.randint(0, len(rota) - 1)
            rota[i], rota[j] = rota[j], rota[i]
    return rota


def algoritmo_genetico(matriz, taxa_mutacao=0.05, max_estagnacao=100, callback=None):
    n = len(matriz)
    tamanho_pop = definir_populacao(n)
    populacao = [gerar_rota(n) for _ in range(tamanho_pop)]

    melhor_rota = None
    melhor_dist = float("inf")
    historico = []
    inicio = time.time()
    
    geracoes_sem_melhoria = 0
    geracao = 0

    while geracoes_sem_melhoria < max_estagnacao:
        geracao += 1
        populacao.sort(key=lambda x: calcular_distancia(x, matriz))
        atual = populacao[0]
        dist = calcular_distancia(atual, matriz)
        historico.append((geracao, dist))

        if dist < melhor_dist:
            melhor_dist = dist
            melhor_rota = atual.copy()
            geracoes_sem_melhoria = 0  # Reset contador
        else:
            geracoes_sem_melhoria += 1

        if callback:
            callback(geracao, geracoes_sem_melhoria, max_estagnacao, melhor_dist)

        nova = [atual]
        while len(nova) < tamanho_pop:
            p1 = selecao_torneio(populacao, matriz)
            p2 = selecao_torneio(populacao, matriz)
            filho = crossover(p1, p2)
            filho = mutacao(filho, taxa_mutacao)
            nova.append(filho)
        populacao = nova

    tempo = time.time() - inicio
    return melhor_rota, melhor_dist, historico, tempo, geracao


# ==============================================
#  INTERFACE GRÁFICA
# ==============================================

class CaixeiroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caixeiro Viajante - Algoritmo Genético")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0e27")

        # Estilo personalizado
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar", 
                       troughcolor='#1a1f3a', 
                       background='#10b981',
                       bordercolor='#1a1f3a',
                       lightcolor='#10b981',
                       darkcolor='#10b981')

        # Container principal com padding
        self.container = tk.Frame(root, bg="#0a0e27")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # CABEÇALHO
        header = tk.Frame(self.container, bg="#0f172a", relief="flat", bd=0)
        header.pack(fill="x", pady=(0, 20))
        
        title_frame = tk.Frame(header, bg="#0f172a")
        title_frame.pack(pady=15)
        
        tk.Label(title_frame, text="Caixeiro Viajante", 
                font=("Segoe UI", 20, "bold"), fg="#e0e7ff", bg="#0f172a").pack(side="left", padx=(20, 10))
        tk.Label(title_frame, text="Algoritmo Genético", 
                font=("Segoe UI", 12), fg="#94a3b8", bg="#0f172a").pack(side="left")

        # ÁREA COM SCROLL
        canvas_container = tk.Frame(self.container, bg="#0a0e27")
        canvas_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_container, bg="#0a0e27", highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="#0a0e27")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind para centralizar conteúdo
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Scroll com mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.num_cidades = 0
        self.entries = []

        # ----- PARÂMETROS -----
        params_frame = tk.Frame(self.scrollable_frame, bg="#1e293b", relief="flat", bd=0)
        params_frame.pack(fill="x", padx=10, pady=10)
        
        inner_params = tk.Frame(params_frame, bg="#1e293b")
        inner_params.pack(pady=15, padx=15)

        tk.Label(inner_params, text="Número de Cidades:", fg="#cbd5e1", bg="#1e293b",
                 font=("Segoe UI", 11)).grid(row=0, column=0, padx=(0, 10), sticky="e")
        self.entry_cidades = tk.Entry(inner_params, width=8, font=("Segoe UI", 11), 
                                      bg="#0f172a", fg="#e2e8f0", insertbackground="#e2e8f0",
                                      relief="flat", bd=2)
        self.entry_cidades.grid(row=0, column=1, padx=(0, 30))

        tk.Label(inner_params, text="Taxa de Mutação:", fg="#cbd5e1", bg="#1e293b",
                 font=("Segoe UI", 11)).grid(row=0, column=2, padx=(0, 10), sticky="e")
        self.entry_mutacao = tk.Entry(inner_params, width=8, font=("Segoe UI", 11),
                                      bg="#0f172a", fg="#e2e8f0", insertbackground="#e2e8f0",
                                      relief="flat", bd=2)
        self.entry_mutacao.insert(0, "0.05")
        self.entry_mutacao.grid(row=0, column=3, padx=(0, 30))

        tk.Label(inner_params, text="Estagnação:", fg="#cbd5e1", bg="#1e293b",
                 font=("Segoe UI", 11)).grid(row=0, column=4, padx=(0, 10), sticky="e")
        self.entry_estagnacao = tk.Entry(inner_params, width=8, font=("Segoe UI", 11),
                                         bg="#0f172a", fg="#e2e8f0", insertbackground="#e2e8f0",
                                         relief="flat", bd=2)
        self.entry_estagnacao.insert(0, "100")
        self.entry_estagnacao.grid(row=0, column=5, padx=(0, 30))

        btn_frame = tk.Frame(inner_params, bg="#1e293b")
        btn_frame.grid(row=0, column=6, columnspan=2, padx=10)
        
        self.btn_gerar = tk.Button(btn_frame, text="Gerar Matriz", command=self.gerar_matriz,
                  bg="#6366f1", fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2", padx=20, pady=8,
                  activebackground="#4f46e5", activeforeground="white")
        self.btn_gerar.pack(side="left", padx=5)
        
        self.btn_aleatorio = tk.Button(btn_frame, text="Preencher Aleatório", command=self.preencher_aleatorio,
                  bg="#8b5cf6", fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", cursor="hand2", padx=20, pady=8,
                  activebackground="#7c3aed", activeforeground="white")
        self.btn_aleatorio.pack(side="left", padx=5)

        # MATRIZ
        self.frame_matriz_container = tk.Frame(self.scrollable_frame, bg="#1e293b", relief="flat", bd=0)
        self.frame_matriz_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        matriz_title = tk.Label(self.frame_matriz_container, text="Matriz de Distâncias", 
                               fg="#e0e7ff", bg="#1e293b", font=("Segoe UI", 12, "bold"))
        matriz_title.pack(pady=(10, 5))
        
        self.frame_matriz = tk.Frame(self.frame_matriz_container, bg="#1e293b")
        self.frame_matriz.pack(pady=10, padx=15)

        # EXECUÇÃO
        exec_frame = tk.Frame(self.scrollable_frame, bg="#0a0e27")
        exec_frame.pack(pady=15)
        
        self.btn_exec = tk.Button(exec_frame, text="Executar Algoritmo Genético",
                                  command=self.executar, bg="#10b981", fg="white", 
                                  font=("Segoe UI", 13, "bold"),
                                  relief="flat", cursor="hand2", padx=40, pady=12,
                                  activebackground="#059669", activeforeground="white")
        self.btn_exec.pack()

        # PROGRESSO
        progress_frame = tk.Frame(self.scrollable_frame, bg="#1e293b", relief="flat", bd=0)
        progress_frame.pack(fill="x", padx=10, pady=10)
        
        progress_inner = tk.Frame(progress_frame, bg="#1e293b")
        progress_inner.pack(pady=15, padx=20)
        
        self.progress = ttk.Progressbar(progress_inner, orient="horizontal", length=700, 
                                       mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress.pack(pady=5)
        
        self.label_status = tk.Label(progress_inner, text="Aguardando execução...", 
                                     bg="#1e293b", fg="#94a3b8", font=("Segoe UI", 10))
        self.label_status.pack(pady=5)

        # RESULTADO
        result_frame = tk.Frame(self.scrollable_frame, bg="#1e293b", relief="flat", bd=0)
        result_frame.pack(fill="x", padx=10, pady=10)
        
        self.label_resultado = tk.Label(result_frame, text="", bg="#1e293b", fg="#e0e7ff",
                                        font=("Segoe UI", 11), justify="center")
        self.label_resultado.pack(pady=20)

        # HISTÓRICO
        hist_container = tk.Frame(self.scrollable_frame, bg="#1e293b", relief="flat", bd=0)
        hist_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(hist_container, text="Histórico de Gerações", 
                bg="#1e293b", fg="#e0e7ff", font=("Segoe UI", 12, "bold")).pack(pady=(10, 5))
        
        text_frame = tk.Frame(hist_container, bg="#1e293b")
        text_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.text_hist = tk.Text(text_frame, wrap="none", height=12, bg="#0f172a", 
                                fg="#cbd5e1", font=("Consolas", 9), relief="flat", bd=0)
        scroll_y = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_hist.yview)
        scroll_x = ttk.Scrollbar(text_frame, orient="horizontal", command=self.text_hist.xview)
        self.text_hist.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.text_hist.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # GRÁFICO
        self.frame_grafico = tk.Frame(self.scrollable_frame, bg="#1e293b", relief="flat", bd=0)
        self.frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        frame_width = self.scrollable_frame.winfo_reqwidth()
        if frame_width < canvas_width:
            self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

    def gerar_matriz(self):
        for w in self.frame_matriz.winfo_children():
            w.destroy()

        try:
            self.num_cidades = int(self.entry_cidades.get())
            if not (2 <= self.num_cidades <= 20):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido entre 2 e 20.")
            return

        self.entries = []
        tk.Label(self.frame_matriz, text="", bg="#1e293b").grid(row=0, column=0)
        
        for j in range(self.num_cidades):
            tk.Label(self.frame_matriz, text=f"C{j+1}", fg="#818cf8", bg="#1e293b",
                     font=("Segoe UI", 9, "bold")).grid(row=0, column=j+1, padx=2, pady=2)

        for i in range(self.num_cidades):
            tk.Label(self.frame_matriz, text=f"C{i+1}", fg="#818cf8", bg="#1e293b",
                     font=("Segoe UI", 9, "bold")).grid(row=i+1, column=0, padx=2, pady=2)
            linha = []
            for j in range(self.num_cidades):
                if j >= i:
                    e = tk.Entry(self.frame_matriz, width=5, font=("Segoe UI", 9), 
                                state="disabled", disabledbackground="#0f172a", 
                                disabledforeground="#475569", relief="flat", bd=1)
                else:
                    e = tk.Entry(self.frame_matriz, width=5, font=("Segoe UI", 9),
                                bg="#0f172a", fg="#e2e8f0", insertbackground="#e2e8f0",
                                relief="flat", bd=1, highlightthickness=1, 
                                highlightbackground="#334155", highlightcolor="#6366f1")
                e.grid(row=i+1, column=j+1, padx=1, pady=1)
                linha.append(e)
            self.entries.append(linha)

    def preencher_aleatorio(self):
        if not self.entries:
            messagebox.showwarning("Aviso", "Gere a matriz primeiro.")
            return
        for i in range(self.num_cidades):
            for j in range(self.num_cidades):
                if j < i:
                    valor = random.randint(5, 60)
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, str(valor))

    def atualizar_progresso(self, geracao, sem_melhoria, max_estagnacao, melhor_dist):
        # Progresso baseado na estagnação
        progresso = (sem_melhoria / max_estagnacao) * 100
        self.progress["value"] = progresso
        
        if sem_melhoria == 0:
            status_msg = f"Geração {geracao} | NOVA MELHOR SOLUÇÃO | Distância: {melhor_dist:.2f}"
        elif sem_melhoria < max_estagnacao * 0.5:
            status_msg = f"Geração {geracao} | Buscando melhoria: {sem_melhoria}/{max_estagnacao} | Distância: {melhor_dist:.2f}"
        elif sem_melhoria < max_estagnacao * 0.8:
            status_msg = f"Geração {geracao} | Estagnação: {sem_melhoria}/{max_estagnacao} | Distância: {melhor_dist:.2f}"
        else:
            status_msg = f"Geração {geracao} | Finalizando: {sem_melhoria}/{max_estagnacao} | Distância: {melhor_dist:.2f}"
        
        self.label_status.config(text=status_msg)
        
        marcador = "*" if sem_melhoria == 0 else " "
        self.text_hist.insert(tk.END, f"{marcador} Geração {geracao:>4} | Sem melhoria: {sem_melhoria:>3} | Distância: {melhor_dist:>8.2f}\n")
        self.text_hist.see(tk.END)
        self.root.update_idletasks()

    def executar(self):
        try:
            taxa_mutacao = float(self.entry_mutacao.get())
            max_estagnacao = int(self.entry_estagnacao.get())
            
            if max_estagnacao < 10:
                messagebox.showwarning("Aviso", "O limite de estagnação deve ser pelo menos 10.")
                return
            
            matriz = np.zeros((self.num_cidades, self.num_cidades))
            for i in range(self.num_cidades):
                for j in range(self.num_cidades):
                    if j < i:
                        valor = self.entries[i][j].get().strip()
                        matriz[i, j] = float(valor if valor else 0)
                        matriz[j, i] = matriz[i, j]

            self.progress["value"] = 0
            self.text_hist.delete("1.0", tk.END)
            self.text_hist.insert(tk.END, f"Iniciando algoritmo genético com critério de parada por estagnação\n")
            self.text_hist.insert(tk.END, f"Parando após {max_estagnacao} gerações sem melhoria\n")
            self.text_hist.insert(tk.END, f"{'-'*80}\n\n")

            melhor_rota, melhor_dist, historico, tempo_exec, total_geracoes = algoritmo_genetico(
                matriz, taxa_mutacao=taxa_mutacao, max_estagnacao=max_estagnacao, 
                callback=self.atualizar_progresso)

            self.progress["value"] = 100
            self.text_hist.insert(tk.END, f"\n{'-'*80}\n")
            self.text_hist.insert(tk.END, f"Algoritmo finalizado após {total_geracoes} gerações\n")
            self.text_hist.insert(tk.END, f"Critério de parada: {max_estagnacao} gerações sem melhoria\n")

            rota_str = " → ".join([f"C{i+1}" for i in melhor_rota]) + f" → C{melhor_rota[0]+1}"
            self.label_resultado.config(
                text=f"Melhor Rota Encontrada:\n{rota_str}\n\n"
                     f"Distância Total: {melhor_dist:.2f}\n"
                     f"Total de Gerações: {total_geracoes}\n"
                     f"Tempo de Execução: {tempo_exec:.2f}s"
            )

            # GRÁFICO
            
        except Exception as e:
            messagebox.showerror("Erro", str(e))


# ==============================================
#  EXECUÇÃO
# ==============================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CaixeiroApp(root)
    root.mainloop()