import os
import sys

import customtkinter
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from caixeiro_viajante import Caixeiro
from subida_de_encosta import SubidaDeEncosta
from subida_de_encosta_alterada import SubidaDeEncostaAlterada
from tempera_simulada import TemperaSimulada

customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("system")

appIniciado = False
caixeiro = 0
solucao_inicial = 0
custo_inicial = 0


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Avaliação de IA")
        self.geometry("1280x960")

        # Define o caminho correto para as imagens
        if hasattr(sys, '_MEIPASS'):
            # Quando rodando como executável criado pelo PyInstaller
            base_path = sys._MEIPASS
        else:
            # Quando rodando na IDE
            base_path = os.path.dirname(os.path.abspath(__file__))
            base_path = os.path.join(base_path, "..")  # Subir um nível para encontrar 'images'

        image_path = os.path.join(base_path, "images")

        # Verifica se o arquivo de ícone existe
        icon_path = os.path.join(image_path, "small_app_logo_ico.ico")
        if not os.path.exists(icon_path):
            messagebox.showerror("Erro", f"Ícone não encontrado: {icon_path}")
            sys.exit(1)

        # Define o icone do programa
        self.wm_iconbitmap(icon_path)
        self.iconapp = ImageTk.PhotoImage(file=os.path.join(image_path, "small_app_logo2.png"))
        self.iconphoto(False, self.iconapp)

        # Centralizar a janela na tela
        self.update_idletasks()  # Atualiza as informações da janela
        width = 1280
        height = 960
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Configure grid layout 1x2 for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Carregar a imagem com suporte para modos claro e escuro
        self.logo_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "robologo_light.png")),
            dark_image=Image.open(os.path.join(image_path, "robologo_dark.png")), size=(80, 80))

        # Create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid rows within navigation_frame
        self.navigation_frame.grid_rowconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                                                weight=0)  # The row for the label should not expand
        self.navigation_frame.grid_rowconfigure(20, weight=1)

        '''


            Criando o Título da Sidebar


        '''

        self.nf_title = customtkinter.CTkLabel(self.navigation_frame, text="Avaliação de IA",
                                               font=customtkinter.CTkFont(size=18, weight="bold"))
        self.nf_title.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="n")

        self.nf_subtitle = customtkinter.CTkLabel(self.navigation_frame, text="Caixeiro Viajante",
                                                  font=customtkinter.CTkFont(size=14, weight="normal"))
        self.nf_subtitle.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")

        self.nf_image_label = customtkinter.CTkLabel(self.navigation_frame, text="", image=self.logo_image)
        self.nf_image_label.grid(row=2, column=0, padx=20, pady=0, sticky="n")

        """


            Criando o Input de Tamanho


        """

        self.nf_size = customtkinter.CTkLabel(self.navigation_frame, text="Tamanho",
                                              font=customtkinter.CTkFont(size=12, weight="normal"))
        self.nf_size.grid(row=3, column=0, padx=20, pady=(20, 0), sticky="n")

        self.nf_size_entry = customtkinter.CTkEntry(self.navigation_frame, placeholder_text="Digite algo...",
                                                    font=customtkinter.CTkFont(size=12, weight="normal"))
        self.nf_size_entry.grid(row=4, column=0, padx=20, pady=(0, 0), sticky="n")

        self.nf_button_start = customtkinter.CTkButton(self.navigation_frame, text="Iniciar", command=self.iniciarApp)
        self.nf_button_start.grid(row=5, column=0, padx=20, pady=(15, 0), sticky="n")

        self.nf_button_start_subtitle = customtkinter.CTkLabel(self.navigation_frame,
                                                               text="Ao clicar, o programa gerará o problema e sua solução inicial  ",
                                                               font=customtkinter.CTkFont(size=10, weight="normal",
                                                                                          slant="italic"),
                                                               wraplength=150)
        self.nf_button_start_subtitle.grid(row=6, column=0, padx=20, pady=(5, 0), sticky="n")

        '''


            Criando um Divisor


        '''

        self.nf_divider = customtkinter.CTkFrame(self.navigation_frame, height=3, bg_color="gray", width=80)
        self.nf_divider.grid(row=7, column=0, padx=50, pady=(20, 0), sticky="ew")

        '''


            Criando os Inputs dos Métodos


        '''

        # Subida de Encosta - Título
        self.nf_hc_title = customtkinter.CTkLabel(self.navigation_frame, text="1. Subida de Encosta",
                                                  font=customtkinter.CTkFont(size=12, weight="bold"), wraplength=150)
        self.nf_hc_title.grid(row=8, column=0, padx=20, pady=(20, 0), sticky="n")

        ##########

        # Subida de Encosta (alterada) - Título
        self.nf_hcA_title = customtkinter.CTkLabel(self.navigation_frame, text="2. Subida de Encosta",
                                                   font=customtkinter.CTkFont(size=12, weight="bold"), wraplength=200)
        self.nf_hcA_title.grid(row=9, column=0, padx=20, pady=(0, 0), sticky="n")

        # Subida de Encosta (alterada) - Subtitulo
        self.nf_hcA_subtitle = customtkinter.CTkLabel(self.navigation_frame, text="Algoritmo alterado",
                                                      font=customtkinter.CTkFont(size=10, weight="normal",
                                                                                 slant="italic"))
        self.nf_hcA_subtitle.grid(row=9, column=0, padx=20, pady=(18, 0), sticky="n")

        # Subida de Encosta (alterada) - Input label
        self.nf_hcA_input_label = customtkinter.CTkLabel(self.navigation_frame, text="T-Max",
                                                         font=customtkinter.CTkFont(size=12, weight="normal"),
                                                         wraplength=150)
        self.nf_hcA_input_label.grid(row=9, column=0, padx=20, pady=(45, 0), sticky="n")

        # Subida de Encosta (alterada) - Input
        self.nf_hcA_input = customtkinter.CTkEntry(self.navigation_frame, placeholder_text="Digite algo...",
                                                   font=customtkinter.CTkFont(size=12, weight="normal"))
        self.nf_hcA_input.grid(row=11, column=0, padx=20, pady=(0, 10), sticky="n")

        ##########

        # Têmpera Simulada - Título
        self.nf_sa_title = customtkinter.CTkLabel(self.navigation_frame, text="3. Têmpera Simulada",
                                                  font=customtkinter.CTkFont(size=12, weight="bold"), wraplength=200)
        self.nf_sa_title.grid(row=12, column=0, padx=20, pady=(0, 0), sticky="n")

        # Têmpera Simulada - Input Label (T-Ini)
        self.nf_sa_input_label_tini = customtkinter.CTkLabel(self.navigation_frame, text="T-Ini",
                                                             font=customtkinter.CTkFont(size=12, weight="normal"),
                                                             wraplength=150)
        self.nf_sa_input_label_tini.grid(row=13, column=0, padx=20, pady=(0, 0), sticky="n")

        # Têmpera Simulada - Input (T-Ini)
        self.nf_sa_input_tini = customtkinter.CTkEntry(self.navigation_frame, placeholder_text="Digite algo...",
                                                       font=customtkinter.CTkFont(size=12, weight="normal"))
        self.nf_sa_input_tini.grid(row=14, column=0, padx=20, pady=(0, 0), sticky="n")

        # Têmpera Simulada - Input Label (T-Fim)
        self.nf_sa_input_label_tfim = customtkinter.CTkLabel(self.navigation_frame, text="T-Fim",
                                                             font=customtkinter.CTkFont(size=12, weight="normal"),
                                                             wraplength=150)
        self.nf_sa_input_label_tfim.grid(row=15, column=0, padx=20, pady=(0, 0), sticky="n")

        # Têmpera Simulada - Input (T-Fim)
        self.nf_sa_input_tfim = customtkinter.CTkEntry(self.navigation_frame, placeholder_text="Digite algo...",
                                                       font=customtkinter.CTkFont(size=12, weight="normal"))
        self.nf_sa_input_tfim.grid(row=16, column=0, padx=20, pady=(0, 0), sticky="n")

        # Têmpera Simulada - Input Label (F-Red)
        self.nf_sa_input_label_fred = customtkinter.CTkLabel(self.navigation_frame, text="F-Red",
                                                             font=customtkinter.CTkFont(size=12, weight="normal"),
                                                             wraplength=150)
        self.nf_sa_input_label_fred.grid(row=17, column=0, padx=20, pady=(0, 0), sticky="n")

        # Têmpera Simulada - Input (F-Red)
        self.nf_sa_input_fred = customtkinter.CTkEntry(self.navigation_frame, placeholder_text="Digite algo...",
                                                       font=customtkinter.CTkFont(size=12, weight="normal"))
        self.nf_sa_input_fred.grid(row=18, column=0, padx=20, pady=(0, 0), sticky="n")

        ##########

        # Botão para rodar os algorítmos
        self.nf_button_run = customtkinter.CTkButton(
            self.navigation_frame,
            text="Rodar Algoritmos",
            state="disabled",
            fg_color="gray",  # Cor do fundo quando desabilitado
            hover_color="gray",  # Cor ao passar o mouse (não necessário se sempre desabilitado)
            command=self.rodar_algoritmos
        )
        self.nf_button_run.grid(row=19, column=0, padx=20, pady=(15, 0), sticky="n")

        '''


            Trocar Tema


        '''

        self.nf_appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                   values=["Sistema", "Claro", "Escuro"],
                                                                   command=self.change_appearance_mode_event)
        self.nf_appearance_mode_menu.grid(row=20, column=0, padx=20, pady=20, sticky="s")

        """


            Tela Inicial


        """

        # Criando o Frame Inicial
        self.ms_frame = customtkinter.CTkFrame(self, width=900, corner_radius=0, fg_color="transparent")
        self.ms_frame.grid(row=0, column=1, sticky="nsew")
        self.ms_frame.grid_rowconfigure(0, weight=1)
        self.ms_frame.grid_columnconfigure(0, weight=1)

        # Criando as Tabs
        self.ms_frame_tabs = customtkinter.CTkTabview(self.ms_frame)
        self.ms_frame_tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.ms_frame_tabs.add("Subida de Encosta")
        self.ms_frame_tabs.add("Subida de Encosta Alterada")
        self.ms_frame_tabs.add("Têmpera Simulada")

        """


            Tab Subida de Encosta


        """

        # => Frame Problema

        # Criando e configurando o frame Problema | Subida de Encosta
        self.ms_hc_problem = customtkinter.CTkFrame(self.ms_frame_tabs.tab("Subida de Encosta"), width=200, height=200,
                                                    fg_color="transparent", border_width=1, border_color="gray")
        self.ms_hc_problem.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Criando e configurando o título do frame Problema | Subida de Encosta
        self.ms_hc_problem_title = customtkinter.CTkLabel(self.ms_frame_tabs.tab("Subida de Encosta"),
                                                          text="Problema Gerado",
                                                          font=customtkinter.CTkFont(size=12, weight="normal"))
        self.ms_hc_problem_title.grid(row=0, column=0, padx=5, pady=(15, 0), sticky="n")

        # Criando e configurando o textbox do frame Problema | Subida de Encosta
        self.ms_hc_problem_textbox = customtkinter.CTkTextbox(self.ms_frame_tabs.tab("Subida de Encosta"), width=100)
        self.ms_hc_problem_textbox.grid(row=0, column=0, padx=15, pady=(50, 15), sticky="nsew")
        self.ms_hc_problem_textbox.insert("0.0", "")
        self.ms_hc_problem_textbox.configure(state="disabled")

        ##########
        # => Frame Solução Inicial

        # Criando e configurando o frame Solução Inicial  | Subida de Encosta
        self.ms_hc_init_sol = customtkinter.CTkFrame(self.ms_frame_tabs.tab("Subida de Encosta"), width=200, height=200,
                                                     fg_color="transparent", border_width=1, border_color="gray")
        self.ms_hc_init_sol.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Criando e configurando o título do frame Solução Inicial  | Subida de Encosta
        self.ms_hc_init_sol_title = customtkinter.CTkLabel(self.ms_frame_tabs.tab("Subida de Encosta"),
                                                           text="Solução Inicial",
                                                           font=customtkinter.CTkFont(size=12, weight="normal"))
        self.ms_hc_init_sol_title.grid(row=0, column=1, padx=5, pady=(15, 0), sticky="n")

        # Criando e configurando o textbox do frame Solução Inicial  | Subida de Encosta
        self.ms_hc_init_sol_textbox = customtkinter.CTkTextbox(self.ms_frame_tabs.tab("Subida de Encosta"), width=100)
        self.ms_hc_init_sol_textbox.grid(row=0, column=1, padx=15, pady=(50, 15), sticky="nsew")
        self.ms_hc_init_sol_textbox.insert("0.0", "")
        self.ms_hc_init_sol_textbox.configure(state="disabled")

        ##########
        # => Frame Solução Final

        # Criando e configurando o frame Solução Inicial  | Subida de Encosta
        self.ms_hc_final_sol = customtkinter.CTkFrame(self.ms_frame_tabs.tab("Subida de Encosta"), width=405,
                                                      height=200, fg_color="transparent", border_width=1,
                                                      border_color="gray")
        self.ms_hc_final_sol.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Criando e configurando o título do frame Solução Inicial  | Subida de Encosta
        self.ms_hc_final_sol_title = customtkinter.CTkLabel(self.ms_frame_tabs.tab("Subida de Encosta"),
                                                            text="Resposta do Algoritmo",
                                                            font=customtkinter.CTkFont(size=12, weight="normal"))
        self.ms_hc_final_sol_title.grid(row=1, column=0, columnspan=2, padx=5, pady=(15, 0), sticky="n")

        # Criando e configurando o textbox do frame Solução Inicial  | Subida de Encosta
        self.ms_hc_final_sol_textbox = customtkinter.CTkTextbox(self.ms_frame_tabs.tab("Subida de Encosta"), width=100)
        self.ms_hc_final_sol_textbox.grid(row=1, column=0, columnspan=2, padx=15, pady=(50, 15), sticky="nsew")
        self.ms_hc_final_sol_textbox.insert("0.0", "")
        self.ms_hc_final_sol_textbox.configure(state="disabled")

        ##########

        # Configuração de peso para que os frames se expandam corretamente
        self.ms_frame_tabs.tab("Subida de Encosta").grid_rowconfigure(0, weight=1)
        self.ms_frame_tabs.tab("Subida de Encosta").grid_rowconfigure(1, weight=1)
        self.ms_frame_tabs.tab("Subida de Encosta").grid_columnconfigure(0, weight=1)
        self.ms_frame_tabs.tab("Subida de Encosta").grid_columnconfigure(1, weight=1)

        """


            Tab Subida de Encosta Alterada


        """

        # => Frame Problema

        # Criando e configurando o frame Problema | Subida de Encosta
        self.ms_hcA_problem = customtkinter.CTkFrame(self.ms_frame_tabs.tab("Subida de Encosta Alterada"), width=200,
                                                     height=200, fg_color="transparent", border_width=1,
                                                     border_color="gray")
        self.ms_hcA_problem.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Criando e configurando o título do frame Problema | Subida de Encosta
        self.ms_hcA_problem_title = customtkinter.CTkLabel(self.ms_frame_tabs.tab("Subida de Encosta Alterada"),
                                                           text="Problema Gerado",
                                                           font=customtkinter.CTkFont(size=12, weight="normal"))
        self.ms_hcA_problem_title.grid(row=0, column=0, padx=5, pady=(15, 0), sticky="n")

        # Criando e configurando o textbox do frame Problema | Subida de Encosta
        self.ms_hcA_problem_textbox = customtkinter.CTkTextbox(self.ms_frame_tabs.tab("Subida de Encosta Alterada"),
                                                               width=100)
        self.ms_hcA_problem_textbox.grid(row=0, column=0, padx=15, pady=(50, 15), sticky="nsew")
        self.ms_hcA_problem_textbox.insert("0.0", "")
        self.ms_hcA_problem_textbox.configure(state="disabled")

        ##########
        # => Frame Solução Inicial

        # Criando e configurando o frame Solução Inicial  | Subida de Encosta
        self.ms_hcA_init_sol = customtkinter.CTkFrame(self.ms_frame_tabs.tab("Subida de Encosta Alterada"), width=200,
                                                      height=200, fg_color="transparent", border_width=1,
                                                      border_color="gray")
        self.ms_hcA_init_sol.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Criando e configurando o título do frame Solução Inicial  | Subida de Encosta
        self.ms_hcA_init_sol_title = customtkinter.CTkLabel(self.ms_frame_tabs.tab("Subida de Encosta Alterada"),
                                                            text="Solução Inicial",
                                                            font=customtkinter.CTkFont(size=12, weight="normal"))
        self.ms_hcA_init_sol_title.grid(row=0, column=1, padx=5, pady=(15, 0), sticky="n")

        # Criando e configurando o textbox do frame Solução Inicial  | Subida de Encosta
        self.ms_hcA_init_sol_textbox = customtkinter.CTkTextbox(self.ms_frame_tabs.tab("Subida de Encosta Alterada"),
                                                                width=100)
        self.ms_hcA_init_sol_textbox.grid(row=0, column=1, padx=15, pady=(50, 15), sticky="nsew")
        self.ms_hcA_init_sol_textbox.insert("0.0", "")
        self.ms_hcA_init_sol_textbox.configure(state="disabled")

        ##########
        # => Frame Solução Final

        # Criando e configurando o frame Solução Inicial  | Subida de Encosta
        self.ms_hcA_final_sol = customtkinter.CTkFrame(self.ms_frame_tabs.tab("Subida de Encosta Alterada"), width=405,
                                                       height=200, fg_color="transparent", border_width=1,
                                                       border_color="gray")
        self.ms_hcA_final_sol.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Criando e configurando o título do frame Solução Inicial  | Subida de Encosta
        self.ms_hcA_final_sol_title = customtkinter.CTkLabel(self.ms_frame_tabs.tab("Subida de Encosta Alterada"),
                                                             text="Resposta do Algoritmo",
                                                             font=customtkinter.CTkFont(size=12, weight="normal"))
        self.ms_hcA_final_sol_title.grid(row=1, column=0, columnspan=2, padx=5, pady=(15, 0), sticky="n")

        # Criando e configurando o textbox do frame Solução Inicial  | Subida de Encosta
        self.ms_hcA_final_sol_textbox = customtkinter.CTkTextbox(self.ms_frame_tabs.tab("Subida de Encosta Alterada"),
                                                                 width=100)
        self.ms_hcA_final_sol_textbox.grid(row=1, column=0, columnspan=2, padx=15, pady=(50, 15), sticky="nsew")
        self.ms_hcA_final_sol_textbox.insert("0.0", "")
        self.ms_hcA_final_sol_textbox.configure(state="disabled")

        ##########

        # Configuração de peso para que os frames se expandam corretamente
        self.ms_frame_tabs.tab("Subida de Encosta Alterada").grid_rowconfigure(0, weight=1)
        self.ms_frame_tabs.tab("Subida de Encosta Alterada").grid_rowconfigure(1, weight=1)
        self.ms_frame_tabs.tab("Subida de Encosta Alterada").grid_columnconfigure(0, weight=1)
        self.ms_frame_tabs.tab("Subida de Encosta Alterada").grid_columnconfigure(1, weight=1)

        """


            Tab Têmpera Simulada


        """

        # => Frame Problema

        # Criando e configurando o frame Problema | Têmpera Simulada
        self.ms_ts_problem = customtkinter.CTkFrame(self.ms_frame_tabs.tab("Têmpera Simulada"), width=200, height=200,
                                                    fg_color="transparent", border_width=1, border_color="gray")
        self.ms_ts_problem.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Criando e configurando o título do frame Problema | Têmpera Simulada
        self.ms_ts_problem_title = customtkinter.CTkLabel(self.ms_frame_tabs.tab("Têmpera Simulada"),
                                                          text="Problema Gerado",
                                                          font=customtkinter.CTkFont(size=12, weight="normal"))
        self.ms_ts_problem_title.grid(row=0, column=0, padx=5, pady=(15, 0), sticky="n")

        # Criando e configurando o textbox do frame Problema | Têmpera Simulada
        self.ms_ts_problem_textbox = customtkinter.CTkTextbox(self.ms_frame_tabs.tab("Têmpera Simulada"), width=100)
        self.ms_ts_problem_textbox.grid(row=0, column=0, padx=15, pady=(50, 15), sticky="nsew")
        self.ms_ts_problem_textbox.insert("0.0", "")
        self.ms_ts_problem_textbox.configure(state="disabled")

        ##########
        # => Frame Solução Inicial

        # Criando e configurando o frame Solução Inicial  | Têmpera Simulada
        self.ms_ts_init_sol = customtkinter.CTkFrame(self.ms_frame_tabs.tab("Têmpera Simulada"), width=200, height=200,
                                                     fg_color="transparent", border_width=1, border_color="gray")
        self.ms_ts_init_sol.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Criando e configurando o título do frame Solução Inicial  | Têmpera Simulada
        self.ms_ts_init_sol_title = customtkinter.CTkLabel(self.ms_frame_tabs.tab("Têmpera Simulada"),
                                                           text="Solução Inicial",
                                                           font=customtkinter.CTkFont(size=12, weight="normal"))
        self.ms_ts_init_sol_title.grid(row=0, column=1, padx=5, pady=(15, 0), sticky="n")

        # Criando e configurando o textbox do frame Solução Inicial  | Têmpera Simulada
        self.ms_ts_init_sol_textbox = customtkinter.CTkTextbox(self.ms_frame_tabs.tab("Têmpera Simulada"), width=100)
        self.ms_ts_init_sol_textbox.grid(row=0, column=1, padx=15, pady=(50, 15), sticky="nsew")
        self.ms_ts_init_sol_textbox.insert("0.0", "")
        self.ms_ts_init_sol_textbox.configure(state="disabled")

        ##########
        # => Frame Solução Final

        # Criando e configurando o frame Solução Inicial  | Têmpera Simulada
        self.ms_ts_final_sol = customtkinter.CTkFrame(self.ms_frame_tabs.tab("Têmpera Simulada"), width=405, height=200,
                                                      fg_color="transparent", border_width=1, border_color="gray")
        self.ms_ts_final_sol.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Criando e configurando o título do frame Solução Inicial  | Têmpera Simulada
        self.ms_ts_final_sol_title = customtkinter.CTkLabel(self.ms_frame_tabs.tab("Têmpera Simulada"),
                                                            text="Resposta do Algoritmo",
                                                            font=customtkinter.CTkFont(size=12, weight="normal"))
        self.ms_ts_final_sol_title.grid(row=1, column=0, columnspan=2, padx=5, pady=(15, 0), sticky="n")

        # Criando e configurando o textbox do frame Solução Inicial  | Têmpera Simulada
        self.ms_ts_final_sol_textbox = customtkinter.CTkTextbox(self.ms_frame_tabs.tab("Têmpera Simulada"), width=100)
        self.ms_ts_final_sol_textbox.grid(row=1, column=0, columnspan=2, padx=15, pady=(50, 15), sticky="nsew")
        self.ms_ts_final_sol_textbox.insert("0.0", "")
        self.ms_ts_final_sol_textbox.configure(state="disabled")

        ##########

        # Configuração de peso para que os frames se expandam corretamente
        self.ms_frame_tabs.tab("Têmpera Simulada").grid_rowconfigure(0, weight=1)
        self.ms_frame_tabs.tab("Têmpera Simulada").grid_rowconfigure(1, weight=1)
        self.ms_frame_tabs.tab("Têmpera Simulada").grid_columnconfigure(0, weight=1)
        self.ms_frame_tabs.tab("Têmpera Simulada").grid_columnconfigure(1, weight=1)

        '''


            Adicionando Eventos para o botão "Rodar"


        '''

        self.nf_hcA_input.bind("<KeyRelease>", self.validar_inputs)
        self.nf_sa_input_tini.bind("<KeyRelease>", self.validar_inputs)
        self.nf_sa_input_tfim.bind("<KeyRelease>", self.validar_inputs)
        self.nf_sa_input_fred.bind("<KeyRelease>", self.validar_inputs)

    def change_appearance_mode_event(self, new_appearance_mode):
        appearance_mode_translation = {
            "Sistema": "system",
            "Claro": "light",
            "Escuro": "dark"
        }
        customtkinter.set_appearance_mode(appearance_mode_translation[new_appearance_mode])

    def iniciarApp(self):
        global appIniciado
        global caixeiro
        global solucao_inicial
        global caixeiro_solucao

        tamanho = self.nf_size_entry.get()

        try:
            tamanho = int(tamanho)
            if tamanho > 0:
                appIniciado = True

                # Criar instância de Caixeiro e gerar solução inicial
                caixeiro = Caixeiro(tamanho)
                solucao_inicial = caixeiro.gerar_solucao_inicial()
                custo_inicial = caixeiro.avaliar_solucao(solucao_inicial)

                # Formatar a matriz de distâncias em uma string legível com colchetes
                matriz_legivel = '[\n' + '\n'.join(['  ' + str(linha) for linha in caixeiro.matriz_distancias]) + '\n]'

                # Exibir o problema gerado e a solução inicial | Subida de Encosta
                self.ms_hc_problem_textbox.configure(state="normal")
                self.ms_hc_problem_textbox.delete("1.0", tk.END)
                self.ms_hc_problem_textbox.insert(tk.END, matriz_legivel)
                self.ms_hc_problem_textbox.configure(state="disabled")

                self.ms_hc_init_sol_textbox.configure(state="normal")
                self.ms_hc_init_sol_textbox.delete("1.0", tk.END)
                self.ms_hc_init_sol_textbox.insert(tk.END, str(solucao_inicial) + "\nCusto: " + str(custo_inicial))
                self.ms_hc_init_sol_textbox.configure(state="disabled")

                self.ms_hc_final_sol_textbox.configure(state="normal")
                self.ms_hc_final_sol_textbox.delete("1.0", tk.END)
                self.ms_hc_final_sol_textbox.configure(state="disabled")

                # Exibir o problema gerado e a solução inicial | Subida de Encosta Alterada
                self.ms_hcA_problem_textbox.configure(state="normal")
                self.ms_hcA_problem_textbox.delete("1.0", tk.END)
                self.ms_hcA_problem_textbox.insert(tk.END, matriz_legivel)
                self.ms_hcA_problem_textbox.configure(state="disabled")

                self.ms_hcA_init_sol_textbox.configure(state="normal")
                self.ms_hcA_init_sol_textbox.delete("1.0", tk.END)
                self.ms_hcA_init_sol_textbox.insert(tk.END, str(solucao_inicial) + "\nCusto: " + str(custo_inicial))
                self.ms_hcA_init_sol_textbox.configure(state="disabled")

                self.ms_hcA_final_sol_textbox.configure(state="normal")
                self.ms_hcA_final_sol_textbox.delete("1.0", tk.END)
                self.ms_hcA_final_sol_textbox.configure(state="disabled")

                # Exibir o problema gerado e a solução inicial | Têmpera Simulada
                self.ms_ts_problem_textbox.configure(state="normal")
                self.ms_ts_problem_textbox.delete("1.0", tk.END)
                self.ms_ts_problem_textbox.insert(tk.END, matriz_legivel)
                self.ms_ts_problem_textbox.configure(state="disabled")

                self.ms_ts_init_sol_textbox.configure(state="normal")
                self.ms_ts_init_sol_textbox.delete("1.0", tk.END)
                self.ms_ts_init_sol_textbox.insert(tk.END, str(solucao_inicial) + "\nCusto: " + str(custo_inicial))
                self.ms_ts_init_sol_textbox.configure(state="disabled")

                self.ms_ts_final_sol_textbox.configure(state="normal")
                self.ms_ts_final_sol_textbox.delete("1.0", tk.END)
                self.ms_ts_final_sol_textbox.configure(state="disabled")

                # Verificar entradas para habilitar o botão
                self.validar_inputs()

            else:
                messagebox.showwarning("Erro", "O valor inserido deve ser maior que 0.")
        except ValueError:
            messagebox.showwarning("Erro", "O valor inserido não é numérico.")

    def validar_inputs(self, event=None):
        if (
                appIniciado and
                self.nf_hcA_input.get() and
                self.nf_sa_input_tini.get() and
                self.nf_sa_input_tfim.get() and
                self.nf_sa_input_fred.get()):
            self.nf_button_run.configure(state="normal",
                                         fg_color=customtkinter.ThemeManager.theme["CTkButton"]["fg_color"],
                                         hover_color=customtkinter.ThemeManager.theme["CTkButton"]["hover_color"])
        else:
            self.nf_button_run.configure(state="disabled", fg_color="gray", hover_color="gray")

    def rodar_algoritmos(self):
        try:
            t_max = int(self.nf_hcA_input.get())
            t_ini = int(self.nf_sa_input_tini.get())
            t_fim = int(self.nf_sa_input_tfim.get())
            f_red = float(self.nf_sa_input_fred.get())

            if t_max > 0 and t_ini > 0 and t_fim > 0 and f_red > 0:
                # Executar Subida de Encosta
                subida_de_encosta = SubidaDeEncosta(caixeiro.num_cidades, caixeiro.matriz_distancias)
                melhor_solucao_se, melhor_valor_se = subida_de_encosta.subida_encosta(solucao_inicial, custo_inicial,
                                                                                      caixeiro)

                # Exibir resultado Subida de Encosta
                self.ms_hc_final_sol_textbox.configure(state="normal")
                self.ms_hc_final_sol_textbox.delete("1.0", tk.END)
                self.ms_hc_final_sol_textbox.insert(tk.END, f'Solução: {melhor_solucao_se}\nCusto: {melhor_valor_se}')
                self.ms_hc_final_sol_textbox.configure(state="disabled")

                # Executar Subida de Encosta Alterada
                subida_de_encosta_alterada = SubidaDeEncostaAlterada(caixeiro.num_cidades, caixeiro.matriz_distancias)
                melhor_solucao_sea, melhor_valor_sea = subida_de_encosta_alterada.subida_encosta_alterada(
                    solucao_inicial, custo_inicial, caixeiro, t_max)

                # Exibir resultado Subida de Encosta Alterada
                self.ms_hcA_final_sol_textbox.configure(state="normal")
                self.ms_hcA_final_sol_textbox.delete("1.0", tk.END)
                self.ms_hcA_final_sol_textbox.insert(tk.END,
                                                     f'Solução: {melhor_solucao_sea}\nCusto: {melhor_valor_sea}')
                self.ms_hcA_final_sol_textbox.configure(state="disabled")

                # Executar Têmpera Simulada
                tempera_simulada = TemperaSimulada(caixeiro.num_cidades, caixeiro.matriz_distancias)
                melhor_solucao_ts, melhor_valor_ts = tempera_simulada.tempera(solucao_inicial, custo_inicial, caixeiro,
                                                                              t_ini, t_fim, f_red)

                # Exibir resultado Têmpera Simulada
                self.ms_ts_final_sol_textbox.configure(state="normal")
                self.ms_ts_final_sol_textbox.delete("1.0", tk.END)
                self.ms_ts_final_sol_textbox.insert(tk.END, f'Solução: {melhor_solucao_ts}\nCusto: {melhor_valor_ts}')
                self.ms_ts_final_sol_textbox.configure(state="disabled")

            else:
                messagebox.showwarning("Erro", "Todos os valores inseridos devem ser maiores que 0.")
        except ValueError:
            messagebox.showwarning("Erro", "Todos os valores inseridos devem ser numéricos.")


# Cria a janela da aplicação
app = App()
app.mainloop()