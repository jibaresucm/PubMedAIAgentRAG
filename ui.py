import queue
import threading

import customtkinter as ctk

from SessionManager import SessionManager

class UserBubble(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(
            master,
            text=text,
            font=("Arial", 18),
            text_color="#F0F0F0",
            fg_color="#383838",
            corner_radius=30,
            padx=5,
            pady=10,
            justify="left",
            wraplength=450
        )

class ModelOutput(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="x", padx=10, pady=5)
        
        self.state = "output" #["output", "tool_call", "tool_response", "thinking"]
        self.current_line_buffer = ""

    def set_wraplength(self, width):
        self.configure(wraplength=max(width - 20, 100))

    def new_output(self, text):
        """Añade texto y el Label crece solo."""
        current_text = self.cget("text")
        self.configure(text=current_text + text)
        
        self.update_idletasks()
        self.master.update_idletasks()
        
    def state_change():
        pass
        
    

class App(ctk.CTk):
    def __init__(self, sm: SessionManager):
        super().__init__()
        self.geometry("800x600")
        self.title("PubMed AI Agent")
        self.configure(fg_color="#121212")
        
        self.sm = sm
        self.turn = True
        
        #Header
        self.header_frame = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color="transparent")
        self.header_frame.pack(side="top", fill="x")
        
        self.title_label = ctk.CTkLabel(self.header_frame, 
                                        text="PubMed AI Agent", 
                                        font=("Arial", 22, "bold"))
        self.title_label.pack(pady=10)
        
        #Divisor de header
        self.divider = ctk.CTkFrame(self, height=2, fg_color="#333333") 
        self.divider.pack(side="top", fill="x", padx=20)
        
        # Chat contenido
        self.chat_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.chat_frame.pack(side="top", fill="both", expand=True, padx=20, pady=(20, 0))

        # Input container
        self.input_container = ctk.CTkFrame(self, fg_color="transparent", border_width=1, corner_radius=15)
        self.input_container.pack(side="bottom", fill="x", padx=20, pady=20)

        #Input
        self.entry = ctk.CTkTextbox(self.input_container, 
                                    fg_color="transparent", 
                                    height=80, 
                                    border_width=0,
                                    font=("Arial", 18),
                                    activate_scrollbars=True) # Scrollbar si el texto es muy largo
        self.entry.pack(side="left", fill="x", expand=True, padx=(15, 5), pady=10)
        
        def handle_key_event(event):
            if event.state & 0x0001:#Si shift presionado nada
                return
            elif  event.state & 0x0004:#Si control
                return
            else: #Si no enter (hacer el send message)
                self.send_message()
                return "break"
    
        self.entry.bind("<Return>", handle_key_event)

        # Boton de enviar
        self.btn = ctk.CTkButton(self.input_container, 
                                text="➤", 
                                width=30, 
                                height=30, 
                                fg_color="transparent", 
                                hover_color="#333333",
                                command=self.send_message) 
        self.btn.pack(side="bottom", padx=(0, 10), pady=10)
        
        #Gestión de mensajes
        self.message_queue = queue.Queue()
        self.bind("<<DataAvailable>>", self.process_queue)
        
        #Resize de texto de chat
        self.chat_frame.bind("<Configure>", self.on_chat_resize)
    
    def scroll_to_bottom(self):
        # 1. Actualizamos el diseño para que el Label tenga su nuevo tamaño
        self.chat_frame.update_idletasks()
        
        # 2. Accedemos al Canvas interno que gestiona el scroll
        canvas = self.chat_frame._parent_canvas
        
        # 3. Forzamos a que el scrollregion (el área total de scroll)
        # se ajuste al tamaño real de todo lo que hay dentro (bbox="all")
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # 4. Movemos la vista al final (1.0 = 100%)
        canvas.yview_moveto(1.0)
        
    def on_chat_resize(self, event):
        """
        'event' contiene el nuevo ancho (event.width) 
        del chat_frame que acaba de cambiar.
        """
        # Recorremos todos los widgets hijos
        for widget in self.chat_frame.winfo_children():
            # Si el hijo es un ModelOutput, actualizamos su ancho
            if isinstance(widget, ModelOutput):
                widget.set_wraplength(event.width)
                
    def process_queue(self, event=None):
        """Esta función solo se ejecuta cuando se dispara el evento."""
        try:
            while not self.message_queue.empty():
                msg = self.message_queue.get_nowait()
                if self.current_model_widget and self.current_model_widget.winfo_exists():
                    self.current_model_widget.new_output(msg)
                    
                self.scroll_to_bottom()
                
                self.message_queue.task_done()
                
        except queue.Empty:
            pass
        
    def model_new_data(self, texto):
        self.message_queue.put(texto)
        
        #Genera evento
        self.event_generate("<<DataAvailable>>", when="tail")


    def add_user_message(self, text):
        bubble = UserBubble(self.chat_frame, text)
        bubble.pack(anchor="e", pady=10) 
        self.current_model_widget = None 

    def add_model_message(self):
        # 1. Creamos el widget
        self.current_model_widget = ModelOutput(self.chat_frame)
        self.current_model_widget.pack(fill="x", padx=10, pady=5)


    def send_message(self):
        prompt = self.entry.get("0.0", "end").strip()
        if prompt and self.turn:
            self.entry.delete("0.0", "end")
            self.add_user_message(prompt)
            self.add_model_message()

            self.turn = False
            
            threading.Thread(target=self.send_to_model, args=(prompt, ), daemon=True).start()
            
    def send_to_model(self, prompt):

        self.sm.send_prompt_to_model(prompt, self)
        
        self.turn = True