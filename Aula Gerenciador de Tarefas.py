import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime

class Gerenciador_Tarefas:
    def __init__(self,janela):
        self.janela = janela
        self.janela.title("Gerenciador de Tarefas")
        self.janela.geometry("800x600")

        self.tarefas = []

        self.style = ttk.Style()
        self.style.theme_use("clam")

    def criar_widgets(self):
        frame_principal = ttk.Frame(self.janela,padding="10")
        frame_principal.pack(fill=tk.BOTH,expand=True)

        Entrada_frame = ttk.Frame(frame_principal,padding=10)
        Entrada_frame.pack(fill=tk.X)

        ttk.Label(Entrada_frame,text="Tarefa:").grid(row=0,column=0,padx=5,sticky=tk.W)
        self.Entrada_tarefa = ttk.Entry(Entrada_frame,width=50)
        self.Entrada_tarefa.grid(row=0,column=1,padx=5,pady=5)
        self.Entrada_tarefa.focus()                                                          #definir onde o cursor vai iniciar

        ttk.Label(Entrada_frame,text="Descrição:").grid(row=1,column=0,padx=5,sticky=tk.W)
        self.Entrada_descrição = ttk.Entry(Entrada_frame,width=50)
        self.Entrada_descrição.grid(row=1,column=1,padx=5,pady=5)

        ttk.Label(Entrada_frame,text="Prioridades:").grid(row=2,column=0,padx=5,sticky=tk.W) #sticky alinha à esquerda
        self.prioridade = tk.StringVar(value="Média")
        ttk.Combobox(Entrada_frame,textvariable=self.prioridade,values={"Baixa","Média","Alta"},state="readonly").grid(row=2,column=1,padx=5,pady=5,sticky=tk.W)   #escrever dentro de uma caixa de seleção e abrir a lista apenas para leitura
        ttk.Label(Entrada_frame,text="Data de Vencimento").grid(row=3,column=0,sticky=tk.W)
    
        self.entrada_data = ttk.Entry(Entrada_frame,width=20)
        self.entrada_data.grid(row=3,column=1,padx=5,pady=5,sticky=tk.W)
        self.entrada_data.insert(0,datetime.now().strftime("%d/%m/%Y"))

        botoes_frame = ttk.Frame(Entrada_frame)
        botoes_frame.grid(row=1,column=1,pady=10,sticky=tk.W)
    
        ttk.Button(botoes_frame,text="Adicionar").pack(side=tk.LEFT,padx=5)
        ttk.Button(botoes_frame,text="Editar").pack(side=tk.LEFT,padx=5)
        ttk.Button(botoes_frame,text="Remover").pack(side=tk.LEFT,padx=5)
        ttk.Button(botoes_frame,text="Marcar como concluída").pack(side=tk.LEFT,padx=5)

        self.tree = ttk.Treeview(frame_principal,columns=("ID","Tarefa","Descrição","Prioridade","Data","Concluída") #cria tipo uma planilha do excel
                                 ,show="headings",selectmode="browse")

        self.tree.column("ID",width=30,anchor=tk.CENTER)
        self.tree.heading("ID",text="ID")

        self.tree.column("Tarefa",width=150,anchor=tk.CENTER)
        self.tree.heading("Tarefa",text="Tarefa")

        self.tree.column("Descrição",width=200,anchor=tk.CENTER)
        self.tree.heading("Descrição",text="Descrição")

        self.tree.column("Prioridade",width=80,anchor=tk.CENTER)
        self.tree.heading("Prioridade",text="Prioridade")

        self.tree.column("Data",width=80,anchor=tk.CENTER)
        self.tree.heading("Data",text="Data de Vencimento")

        self.tree.column("Concluída",width=80,anchor=tk.CENTER)
        self.tree.heading("Concluída",text="Concluída")
        
        self.tree.pack(fill=tk.BOTH,expand=True,pady=10)    

        Scrollbar = ttk.Scrollbar(self.tree,orient=tk.VERTICAL,command=self.tree.yview)

        self.tree.configure(yscroll=Scrollbar.set)
        Scrollbar.pack(side=tk.RIGHT,fill=tk.Y)       

        self.tree.bind("<<TreeViewSelect>>",self.adicionar_tarefa)    


    def adicionar_tarefa(self):
        terefa= self.Entrada_tarefa.get().strip() #strip anula espaços colocados antes do que foi digitado dentro do frame. .GET pega o que você digitou e guarda, o APPEND adiciona o que foi digitado dentro da lista 
        descrição= self.Entrada_descrição.get().strip()
        prioridade = self.prioridade.get()
        data =  self.entrada_data.get().strip()
        nova_tarefa = {
            "id": len(self.tarefas)+1,
            "tarefa": terefa,
            "descrição": descrição,
            "prioridade": prioridade,
            "data": data,
            "concluída": False

        }
        self.tarefas.append(nova_tarefa)

        self.limpar_campos()

    def editar(self):
        selecionado = self.tree.selection()
        if not selecionado:
            return
        
        item = self.tree.item(selecionado)
        id_tarefa = item['values'][0]

        tarefa = self.Entrada_tarefa.get().strip
        descrição = self.Entrada_descrição.get().strip
        prioridade = self.prioridade.get()
        data = self.entrada_data.get().strip

        for opcao in self.tarefas:
            if opcao['id'] == id_tarefa:
                opcao['tarefa'] = tarefa
                opcao['descrição'] = descrição 
                opcao['prioridade'] = prioridade
                opcao['data'] = data 
                break            

    def remover_tarefa(self):
        selecionado = self.tree.selection()         
        if not selecionado:
            return

        item = self.tree.item(selecionado)
        id_tarefa = item['values'][0]

        self.tarefas=[opcao for opcao in self.tarefas if opcao['id']!= id_tarefa]
    
        self.limpar_campos()

    def marcar_concluida(self):
        selecionado = self.tree.selection()
        if not selecionado:
            return

        item= self.tree.item(selecionado)
        id_tarefa = item["values"][0]

        for opcao in self.tarefas:
            if opcao["id"] == id_tarefa:
                opcao["concluída"] = not['concluída']
                break

    def limpar_campos(self):
        self.Entrada_tarefa.delete(0,tk.END)
        self.Entrada_descrição.delete(0,tk.END)
        self.prioridade.set("Média")
        self.entrada_data.delete(0,tk.END)
        self.entrada_data.insert(0,datetime.now().strftime("%d/%m/%Y"))

    def atualizar_lista(self):
        for itens,tarefa in enumerate(self.tarefas,1):
            tarefa['id'] = itens #mantém os id's atualizados

        for item in self.tree.get_children():
            self.tree.delete(item)

        for tarefa in self.tarefas:
            self.tree.insert('',tk.END,values=(tarefa['id'],tarefa['tarefa'],tarefa['descricao'],tarefa['prioridade'],tarefa['data'],'sim' if tarefa['concluida'] else 'não' ))    


    def selecionar_tarefa (self,event):
        selecionado= self.tree.selection()
        if not selecionado:
            return

        item= self.tree.item(selecionado)

        valores= item['values']

        self.limpar_tarefa()

        self.entrada_tarefa.insert(0,valores[1])
        self.entrada_descricao.insert(0,valores[2])
        self.prioridade.set(valores[3])
        self.entrada_data.insert(0,valores[4])
        self.entrada_data.delete(0,tk.END)    

janela= tk.Tk()
app=Gerenciador_Tarefas(janela)
janela.mainloop()            


        
        



































        