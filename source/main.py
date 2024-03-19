import tkinter
import tkinter.messagebox
import customtkinter
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

openai.api_key = "sk-******"

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.message_cnt = 0
        # configure window
        self.title("Park Seung Kyun Chatbot.py")
        self.geometry(f"{1100}x{900}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=102)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=180)
        self.grid_rowconfigure(1, weight=1)
        
        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Chat Log", orientation="vertical", label_font=("Helvetica", 18))
        self.scrollable_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        
        # create button
        self.button = customtkinter.CTkButton(master=self, text="Send", command=self.send_message, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), font=("Helvetica", 18))
        self.button.grid(row=1, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, border_width=2, font=("Helvetica", 18))
        self.textbox.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.textbox.insert("0.0", '이 사람의 장점은 무엇인가요?')
        self.send_message()
        self.textbox.insert("0.0", '질문을 입력해주세요...')

    def send_message(self):
        response = query_engine.query(f"{self.textbox.get(0.0, 'end')}")
        temp = list(f"{response}")
        cnt = 1
        for i in range(len(temp)):
            if (i > 60 * cnt) & (temp[i] == ' '):
                temp[i] = '\n'
                cnt = cnt + 1
        response = ''.join(temp)

        label1 = customtkinter.CTkLabel(master=self.scrollable_frame, text="Question", font=("Helvetica", 18),justify="left")
        label2 = customtkinter.CTkLabel(master=self.scrollable_frame, text=f"{self.textbox.get(0.0, 'end')}", font=("Helvetica", 14),justify="left")
        label3 = customtkinter.CTkLabel(master=self.scrollable_frame, text="Answer", font=("Helvetica", 18),justify="left")
        label4 = customtkinter.CTkLabel(master=self.scrollable_frame, text=f"{response}", font=("Helvetica", 14),justify="left")
        label1.grid(row=self.message_cnt*4, column=0, padx=10, pady=(0, 5), sticky="w")
        label2.grid(row=self.message_cnt*4+1, column=0, padx=10, pady=(0, 5), sticky="w")
        label3.grid(row=self.message_cnt*4+2, column=0, padx=10, pady=(0, 5), sticky="w")
        label4.grid(row=self.message_cnt*4+3, column=0, padx=10, pady=(0, 5), sticky="w")
        self.textbox.delete("0.0", "end")

        self.message_cnt = self.message_cnt + 1

if __name__ == "__main__":
    documents = SimpleDirectoryReader("./data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    app = App()
    app.mainloop()