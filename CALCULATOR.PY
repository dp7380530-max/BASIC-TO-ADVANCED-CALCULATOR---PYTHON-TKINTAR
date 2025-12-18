
# ------------------------------------------------------------------
#   PRJECT : BASIC TO ADVANCED CALCULATOR   ( Python + Tkinter )
#   CREATED BY : DEEPAK PATEL
#   PURPOSE  : Step - by - Step development GUI Calculator
# ------------------------------------------------------------------
import math
from tkinter import *
import customtkinter as ctk
from functools import partial
from tkinter import simpledialog, messagebox
from functools import partial
import random
import sys
root = Tk()

 #----------Global variable to store the current expressio----------------
expr = ""  
first_num = None
operator = None 
current_base = 10
current_unit = None
last_answer = ""
history_list=[]

root.title("Calculator")
root.geometry("300x545")
input_text = StringVar()
root.configure(bg="white")
sys.stdout.reconfigure(encoding='utf-8')

display = Entry(
    root,
    font=("Arial", 20),
    textvariable=input_text,
    bd=0,
    relief="flat",
    justify="right",
    bg="white"

)
display.place(x=10, y=60, width=280, height=55)  # Adjust postion and size


def update_expr(event):
    global expr
    expr = input_text.get()  # sync Entry content with expr


display.bind("<KeyRelease>", update_expr)

# ----------------- Side Menu Frame -----------------
side_menu = Frame(root, bg="white", width=250, height=520)
side_menu.place_forget()

# Hidden initially


def hameburger_menu():
    if side_menu.winfo_ismapped():
        side_menu.place_forget()

    else:
        side_menu.place(x=0, y=60)
        side_menu.lift()


hameburger_btn = Button(root, text="≡", font=("arial", 18, "bold"), bd=0,
                        relief="flat", highlightthickness=0, bg="White", command=hameburger_menu)
hameburger_btn.place(x=5, y=5)

# ---------------- Menu Buttons -----------------


def menu_button(text, command=None):
    btn = Button(
        side_menu,
        text=text,
        font=("arial", 12),
        anchor="w",
        bg="white",
        fg="black",
        bd=0,
        relief="flat",
        activebackground="#f0f0f0",
        activeforeground="black",
        padx=35,
        pady=2,
        highlightthickness=0,
        cursor="hand2",
        command=command
    )
    return btn


btn_standard = menu_button("🧮Standard Calculator")
btn_standard.pack(fill="x", pady=0)

btn_scientific = menu_button("🔬Scientific Calculator")
btn_scientific.pack(fill="x", pady=0)

btn_programmer = menu_button("💻Programmer Calculator")
btn_programmer.pack(fill="x", pady=0)

btn_unit = menu_button("📏Unit Converter")
btn_unit.pack(fill="x", pady=0)

btn_exit = menu_button("🚪Exit", command=root.quit)  
btn_exit.pack(fill="x", pady=0)



def btn_click(item):
    global expr
    expr += str(item)
    input_text.set(expr)


def clear():
    global expr
    expr = ""
    input_text.set("")


def clear_entry():
    global expr
    expr = expr[:-1]
    input_text.set(expr)


def toggle_trig_panel():
    if sci_trig_panel.winfo_ismapped():
        sci_trig_panel.place_forget()
    else:
        sci_trig_panel.place(x=20, y=230)
        sci_trig_panel.lift()


def toggle_func_panel():
    if sci_func_panel.winfo_ismapped():
        sci_func_panel.place_forget()
    else:
        
        sci_func_panel.place(x=20, y=230)
        sci_func_panel.lift()
        sci_trig_panel.place_forget()       


        def make_command(label):
            return lambda: process(label)
        
def toggle_second_function():
    global second_mode
    second_mode = not second_mode

    for btn in trig_button_refs:
        original = trig_original_labels[btn]
        new_label = second_trig_map.get(original, original) if second_mode else original

        btn.configure(
            text=new_label,
            command=lambda t=new_label: process(t)
        )


def process(symbol):
    global expr, first_num, operator,current_base, current_unit, last_answer
    
    if symbol == "ANS":
        if last_answer == "":
            return
        if expr == "" or expr == "Error":
            expr = last_answer
        else:
            expr += last_answer
         
        input_text.set(expr)
        return
    
    if symbol in  ("Length", "Weight", "Temperature", "Volume", "Speed", "Time"):
        current_unit = symbol
        expr = ""
        input_text.set(f"{symbol} selected")
        return

    elif symbol == "=" and current_unit is not None:
        try:
            value = float(expr)
            if current_unit == "Length":
                expr = str(value / 1000)
            elif current_unit == "Weight":
                expr = str(value * 1000)
            elif current_unit == "Temperature":
                expr = str((value * 9/5)+32)
            elif current_unit == "Volume":
                expr = str(value * 1000)
            elif current_unit == "Speed":
                expr = str(value * 1000 / 3600)
            elif current_unit == "Time":
                expr = str(value * 60)
            input_text.set(expr)
            last_answer = expr 
            current_unit = None
        except:
            input_text.set("Error")
            expr = ""
            current_unit = None
        return
    
    elif symbol == "=":
        try:
            result = str(eval(expr))
            expr = result
            last_answer = result
            input_text.set(result)
           
          
        except:
            expr = "Error"
            input_text.set(expr)
    

    
    if symbol == "DEC":
        current_base = 10
    
        try:
            if expr != "":
                expr = str(int(expr, current_base))  
                input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    
    elif symbol == "BIN":
        current_base = 2
        try:
            if expr != "":
                expr = bin(int(expr, 10))[2:]  
                input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    
    elif symbol == "OCT":
        current_base = 8
        try:
            if expr != "":
                expr = oct(int(expr, 10))[2:]  
                input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    
    elif symbol == "HEX":
        current_base = 16
        try:
            if expr != "":
                expr = hex(int(expr, 10))[2:].upper()  
                input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    print("PROCESS CALLED WITH:", symbol)

    # Normal numbers or operators
    if symbol in "0123456789.+-*/()":
        expr += symbol
        input_text.set(expr)

    # Percentage
    elif symbol == "%":
        try:
            expr = str(eval(expr + "/100"))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    # +/- toggle
    elif symbol == "+/-":
        try:
            if expr.startswith("-"):
                expr = expr[1:]
            else:
                expr = "-" + expr
            input_text.set(expr)
        except:
            pass

    # 1/x
    elif symbol == "¹⁄x":
        try:
            expr = str(1 / float(expr))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    # x²
    elif symbol == "x²":
        try:
            expr = str(float(expr) ** 2)
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    # √x
    elif symbol == "√x":
        try:
            expr = str(math.sqrt(float(expr)))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    # BACKSPACE (X)
    elif symbol == "X":
        expr = expr[:-1]
        input_text.set(expr)

    # CLEAR
    elif symbol == "C":
        expr = ""
        input_text.set("")
    # π
    elif symbol == "e":
        expr += str(math.e)
        input_text.set(expr)
    elif symbol == "|x|":
        try:
            expr = str(abs(float(expr)))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "n!":
        try:
            expr = str(math.factorial(int(expr)))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

            first_num = None
            operator = None
            expr = ""

    elif symbol == "xʸ":
        if expr != "":
            first_num = float(expr)
            operator = "**"
            expr = ""
            input_text.set("")

    elif symbol == "log":
        try:
            expr = str(math.log10(float(expr)))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "ln":
        try:
            expr = str(math.log(float(expr)))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "exp":
        try:
            expr = str(math.exp(float(expr)))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "mod":
        expr += "%"
        input_text.set(expr)

    elif symbol == "2√x":
        try:
            value = eval(expr) if expr != "" else 0
            expr = str(2*math.sqrt(float(value)))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "10ˣ":
        try:
            value = eval(expr)
            result = 10 ** value
            input_text.set(str(result))
            expr = str(result)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "x³":
        try:
            expr = str(float(expr)**3)
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "3√x":
        try:
            expr = str(float(expr)**(1/3))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "y√x":
         try:
             if expr == "":
                 input_text.set("Error")
             else:
                y = simpledialog.askfloat("y-th Root", "Enter the value of y:")
             if y is not None:
                 expr_value = float(expr)
                 result = expr_value ** (1/y)
                 expr = str(result)
                 input_text.set(expr)
                 
         except Exception as e:
             input_text.set("Error")
             expr = ""
              


    elif symbol == "2ˣ":
        try:
            expr_value = float(expr)
            result = 2 ** expr_value
            expr = str(result)
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "logᵧ(x)":
        try:
            if expr == "":
                input_text.set("Error")
            else:
                y = simpledialog.askfloat("logᵧ(x)", "Enter base y:")
                
                if y is not None and y > 0 and y != 1 :
                    x = float(expr)
                    result = math.log(x,y)
                    expr = str(result)
                    input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
            
    elif symbol == "In":
        try:
            if expr == "":
                input_text.set("Error")
            else:
                x = float(expr)
                if x <= 0 :
                    input_text.set("Error")
                    expr = ""
                else:
                    expr = str(math.log(x))
                    input_text.set(expr)
        except:
            input_text.set("Error")
            expr=""
                # ---------- TRIGONOMETRY ----------
    elif symbol == "sin":
        try:
            expr = str(math.sin(math.radians(float(expr))))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "cos":
        try:
            expr = str(math.cos(math.radians(float(expr))))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "tan":
        try:
            expr = str(math.tan(math.radians(float(expr))))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "sec":
        try:
            expr = str(1 / math.cos(math.radians(float(expr))))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "csc":
        try:
            expr = str(1 / math.sin(math.radians(float(expr))))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "cot":
        try:
            expr = str(1 / math.tan(math.radians(float(expr))))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "hyp":
        try:
            x = float(expr)
            y = simpledialog.askfloat("Hypotenuse", "Enter second value:")
            if y is not None:
                expr = str(math.hypot(x, y))
                input_text.set(expr)
        except:
            input_text.set("Error")
            expr = "" 
     # ---------- FUNCTION ----------
    elif symbol in ("|x|", "abs"):
        try:
            display.unbind("<KeyRelease>")
            value = float(expr)
            expr = str(abs(value))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
        finally:
            display.bind("<KeyRelease>", update_expr)


    elif symbol == "⌈x⌉":
        try:
            expr = str(math.ceil(float(expr)))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "rand":
        try:
            expr = str(round(random.random(), 6))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "→dms":
        try:
            deg = float(expr)
            d = int(deg)
            m_float = abs(deg - d) * 60
            m = int(m_float)
            s = (m_float - m) * 60
            expr = f"{d}° {m}' {round(s,2)}\""
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "→deg":
        try:
            parts = expr.replace("°", " ").replace("'", " ").replace('"', " ").split()
            d, m, s = map(float, parts)
            expr = str(d + m/60 + s/3600)
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "⌊x⌋":
        try:
            expr = str(math.floor(float(expr)))  
            input_text.set(expr)                  
        except:
            input_text.set("Error")               
            expr = ""
# ---------- NATURAL LOG ----------
            
    elif symbol == "sin⁻¹":
        try:
            x = float(expr)
            if -1 <= x <= 1:
                expr = str(math.degrees(math.asin(x)))
                input_text.set(expr)
            else:
                input_text.set("Error")
                expr = ""
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "cos⁻¹":
        try:
            x = float(expr)
            if -1 <= x <= 1:
                expr = str(math.degrees(math.acos(x)))
                input_text.set(expr)
            else:
                input_text.set("Error")
                expr = ""
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "tan⁻¹":
        try:
            x = float(expr)
            expr = str(math.degrees(math.atan(x)))
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "sec⁻¹":
        try:
            x = float(expr)
            if abs(x) >= 1:
                expr = str(math.degrees(math.acos(1/x)))
                input_text.set(expr)
            else:
                input_text.set("Error")
                expr = ""
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "csc⁻¹":
        try:
            x = float(expr)
            if abs(x) >= 1:
                expr = str(math.degrees(math.asin(1/x)))
                input_text.set(expr)
            else:
                input_text.set("Error")
                expr = ""
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "cot⁻¹":
        try:
            x = float(expr)
            if x == 0:
                input_text.set("Error")
                expr = ""
            else:
                expr = str(math.degrees(math.atan(1/x)))
                input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
            
            
    # ---------- PROGRAMMER CALCULATOR LOGIC ----------
   
    elif symbol == "AND":
        try:
            first_num = int(expr, current_base)   
            operator = "AND"                       
            expr = ""                              
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "OR":
        try:
            value = int(expr, current_base)
            expr = str(value | value)
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "XOR":
        try:
            value = int(expr, current_base)
            expr = str(value ^ value)
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == "NOT":
        try:
            value = int(expr, current_base)
            expr = str(~value)
            input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""

    elif symbol == "<<":
        try:
            value = int(expr, current_base)
            shift = simpledialog.askinteger("Shift", "Enter number of bits to shift left:")
            if shift is not None:
                expr = str(value << shift)
                input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    elif symbol == ">>":
        try:
            value = int(expr, current_base)
            shift = simpledialog.askinteger("Shift", "Enter number of bits to shift right:")
            if shift is not None:
                expr = str(value >> shift)
                input_text.set(expr)
        except:
            input_text.set("Error")
            expr = ""
    
def calculate():
    global expr ,last_answer,history_list
    try:
        result = str(eval(expr))
        input_text.set(result)
        expr = result
        history_list.append(f"{expr}={result}")
    except:
        input_text.set("Error")
        expr = ""
        
        
def show_history():
    if not history_list:
        messagebox.showinfo("History", "No history yet!")
        return
    
    history_win = Toplevel(root)
    history_win.title("Calculator History")
    history_win.geometry("300x400")
    
    # Listbox me history show kare
    listbox = Listbox(history_win, font=("Arial", 12))
    listbox.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Insert all history items
    for item in history_list:
        listbox.insert(END, item)
    
    # Optional: Clear history button
    clear_btn = Button(history_win, text="Clear History", command=lambda: [listbox.delete(0, END), history_list.clear()])
    clear_btn.pack(pady=5)
    
history_btn = Button(root, text="🕘", font=("arial", 15), bd=0, relief="flat",
                     bg="white", cursor="hand2", command= show_history)
history_btn.place(x=250, y=5)




std_frame = ctk.CTkFrame(root, width=300, height=500, fg_color="white")

sci_frame = ctk.CTkFrame(root, width=400, height=600, fg_color="white")
bottom_panel = ctk.CTkFrame(sci_frame, width=352, height=120, fg_color="#f2f2f2",
                            corner_radius=20, border_width=2, border_color="white")
bottom_panel.place(x=7, y=528)  
# Trigonometry Button
btn_width = 120
btn_height = 40
trig_btn = ctk.CTkButton(bottom_panel, text="Trigonometry", width=btn_width, height=btn_height,
                         fg_color="#4da6ff", text_color="white")
trig_btn.place(x=20, y=20)

# Function Button
func_btn = ctk.CTkButton(bottom_panel, text="Function", width=btn_width, height=btn_height,
                         fg_color="#4da6ff", text_color="white", command=toggle_func_panel)
func_btn.place(x=214, y=20)

trig_btn = ctk.CTkButton(
    bottom_panel,
    text="Trigonometry",
    width=120, height=40,
    fg_color="#4da6ff",
    text_color="white",
    command=toggle_trig_panel     
)
trig_btn.place(x=20, y=20)


prog_frame = ctk.CTkFrame(root, width=300, height=595,fg_color = "white")
unit_frame = ctk.CTkFrame(root, width=400, height=600,fg_color="white")
display.lift()


def show_frame(frame):
    std_frame.place_forget()  
    sci_frame.place_forget()
    prog_frame.place_forget()
    unit_frame.place_forget()
    
    frame.place(x=0, y=60)
    side_menu.place_forget()
    if frame == sci_frame:
        bottom_panel.lift()


sci_trig_panel = ctk.CTkFrame(
    sci_frame, width=300, height=150, fg_color="white")
sci_func_panel = ctk.CTkFrame(
    sci_frame, width=250, height=120, fg_color="white")
sci_second_panel = ctk.CTkFrame(
    sci_frame, width=300, height=150, fg_color="white")

sci_trig_panel.place_forget()
sci_func_panel.place_forget()
sci_second_panel.place_forget()

        

trig_buttons = [
               ["2nd", "sin", "cos", "tan"],
               ["hyp", "sec", "csc", "cot"],
]
second_mode = False
trig_button_refs = []
trig_original_labels = {}
second_trig_map = {
    "sin": "sin⁻¹",
    "cos": "cos⁻¹",
    "tan": "tan⁻¹",
    "sec": "sec⁻¹",
    "csc": "csc⁻¹",
    "cot": "cot⁻¹"
}



x_start = 20
y_start = 23

x_gap = 20
y_gap = 20

button_width = 50
button_height = 40

for row_index, row in enumerate(trig_buttons):
    for col_index, text in enumerate(row):
        
        if text == "2nd":
            cmd = toggle_second_function
        else:
            cmd = lambda t =text: process(t)

        b = ctk.CTkButton(
            sci_trig_panel,
            text=text,
            width=button_width,
            height=button_height,
            fg_color="#e6e6e6",
            text_color="black",
            corner_radius=15,
            border_color="black",
            command=cmd

        )
        b.place(
            x=x_start + col_index*(button_width + x_gap),
            y=y_start + row_index*(button_height + y_gap)
        )
        if text != "2nd":
            trig_button_refs.append(b)
            trig_original_labels[b] = text
            
            

        func_buttons = [
            ["|x|", "⌊x⌋", "⌈x⌉"],
            ["rand", "→dms", "→deg"]
        ]

x_start = 20
y_start = 13
x_gap = 25
y_gap = 25
button_width = 50
button_height = 40

for row_index, row in enumerate(func_buttons):
    for col_index, text in enumerate(row):
        b = ctk.CTkButton(
            sci_func_panel,
            text=text,
            width=button_width,
            height=button_height,
            fg_color="#d9d9d9",
            text_color="black",
            corner_radius=15,
            border_width=2,
            border_color="white",
            command=lambda fn=text: process(fn)
        )
        b.place(
            x=x_start + col_index*(button_width + x_gap),
            y=y_start + row_index*(button_height + y_gap)
        )

        

show_frame(std_frame)

btn_standard.config(command=lambda: show_frame(std_frame))
btn_scientific.config(command=lambda: show_frame(sci_frame))
btn_programmer.config(command=lambda: show_frame(prog_frame))
btn_unit.config(command = lambda: show_frame(unit_frame))



def create_button(text, x, y, width=80, height=60, bg="#f0f0f0", fg="black", command=None, frame=None):
    if frame is None:
        frame = std_frame
    if text == "=":
        bg = "#4da6ff"
        fg = "white"
        hover = "#3399ff"
    else:
        hover = "#e6e6e6"

    btn = ctk.CTkButton(
        frame,
        text=text,
        font=("Segoe UI", 14),
        corner_radius=8,
        fg_color=bg,
        border_width=1,
        border_color="#a9a9a9",
        text_color=fg,
        hover_color=hover,
        command=command,
        width=int(width),
        height=int(height)
    )

    btn.place(x=x, y=y)
    return btn


standard_buttons = [
    ["%",    "CE",  "C",    "X"],
    ["¹⁄x",  "x²",  "√x",   "/"],
    ["7",    "8",   "9",   "*"],
    ["4",    "5",   "6",   "-"],
    ["1",    "2",   "3",   "+"],
    ["+/-",  "0",   ".",   "="],

]

start_x = 13
start_y = 130
gap = 4
btn_width = 62
btn_height = 52

for r in range(len(standard_buttons)):
    for c in range(len(standard_buttons[r])):
        text = standard_buttons[r][c]
        if text == "C":
            cmd = clear
        elif text == "CE":
            cmd = clear_entry
        elif text == "X":
            cmd = clear_entry
        elif text == "=":
            cmd = calculate
        else:
            def cmd(t=text): return process(t)

        create_button(
            text,
            x=start_x + c * (btn_width + gap),
            y=start_y + r * (btn_height + gap),
            command=cmd
        )

scientific_buttons = [
    ["2ⁿᵈ", "π", "e", "C", "x"],
    ["x²", "1/x", "|x|", "exp", "mod"],
    ["2√x", "(", ")", "n!", "/"],
    ["xʸ", "7", "8", "9", "*"],
    ["10ˣ", "4", "5", "6", "-"],
    ["log", "1", "2", "3", "+"],
    ["In", "+/-", "0", ".", "="]

]


second_function_active = False
second_map = {
    "x²": "x³",
    "2√x": "3√x",
    "xʸ": "y√x",
    "10ˣ": "2ˣ",
    "log": "logᵧ(x)",
    "In": "eˣ"
}
scientific_button_refs = []
original_labels = {}

start_x = 13
start_y = 130
gap = 4
btn_width = 62
btn_height = 52

for r in range(len(scientific_buttons)):
    for c in range(len(scientific_buttons[r])):
        text = scientific_buttons[r][c]
        if text == "C":
            cmd = clear
        elif text == "CE":
            cmd = clear_entry
        elif text == "x":
            cmd = clear_entry
        elif text == "=":
            cmd = calculate
        elif text == "2ⁿᵈ":
            cmd = toggle_second_function
        else:
         cmd = lambda t=text: process(t)

        btn = create_button(
            text=text,
            x=start_x + c * (btn_width + gap),
            y=start_y + r * (btn_height + gap),
            frame=sci_frame,
            command=cmd
        )
        if text in second_map:
            scientific_button_refs.append(btn)
            original_labels[btn] = text
            
            
programmer_buttons = [
    ["DEC", "BIN", "OCT", "HEX",],
    ["AND", "OR",  "XOR", "NOT",],
    ["<<",  ">>",  "C",   "x"],
    ["(",   ")",   "%",   "/"],
    ["7",   "8",   "9",   "*"],
    ["4",   "5",   "6",   "-"],
    ["1",   "2",   "3",   "+"],
    ["+/-",   "0",  ".",   "="]
]

start_x = 20
start_y = 140   

gap_x = 62
gap_y = 56

btn_width = 62
btn_height = 52

for r, row in enumerate(programmer_buttons):
    for c, text in enumerate(row):

        if text == "":
            continue
        if text == "C":
            cmd = clear
        elif text == "CE":
            cmd = clear_entry
        elif text == "x":
            cmd = clear_entry
        elif text == "=":
            cmd = calculate
        else:
            cmd = lambda t=text: process(t)
       
        btn = create_button(
            text=text,
            x=start_x + c * (btn_width + gap),
            y=start_y + r * (btn_height + gap),
            frame=prog_frame,
            command=cmd
        )
        
    # ---------------- UNIT CONVERTER BUTTONS ----------------
    def ans_button_pressed():
        global expr, last_answer
        if last_answer == "":
         return  
    if expr == "" or expr == "Error":
        expr = last_answer
    else:
        expr += last_answer
    input_text.set(expr)

    def unit_action(unit_type):
        print(f"{unit_type} Converter clicked!")  

unit_buttons = [
    ["Length", "Weight", "Temperature"],
    ["Volume", "Speed", "Time"]
]

start_x = 20
start_y = 200
gap_x = 11  
gap_y = 10  
btn_width = 100
btn_height = 50



for r, row in enumerate(unit_buttons):
    for c, text in enumerate(row):
        btn = create_button(
            text=text,
            x=start_x + c * (btn_width + gap_x),
            y=start_y + r * (btn_height + gap_y),
            frame=unit_frame,
            width=btn_width,
            height=btn_height,
            command=lambda t=text:process(t)
        )
    
def ans_button_click():
        global expr , last_answer
        print("ANS BUTTON CLICKED last_answer", last_answer)
        if last_answer == "":
            return
        if expr == "" or expr =="Error":
            expr = last_answer
        else:
            expr += last_answer 
                        
        input_text.set(expr)
        
un_buttons = [
    ["7", "8", "9", "C"],
    ["4", "5", "6", "X"],
    ["1", "2", "3", "="],
    ["0", ".", "ANS", "+/-"]
]

start_x = 20
start_y =315  

gap_x = 20
gap_y = 10

btn_width = 62
btn_height = 52   

for r, row in enumerate(un_buttons):
    for c, text in enumerate(row):
        if text == "":
            continue
        
        if text == "ANS":
            cmd = ans_button_click
        elif text == "C":
            cmd = clear
        elif text == "X":
            cmd = clear_entry
        elif text == "=":
            cmd = lambda:process("=")
        else:
            cmd = lambda t=text: process(t)  
            
        btn = create_button(
            text=text,
            x=start_x + c * (btn_width + gap_x),
            y=start_y + r * (btn_height + gap_y),
            frame=unit_frame,
            command=cmd
        )
footer = ctk.CTkLabel(
    root,
    text="This Calculator Design By Nethike Intern Deepak Patel",
    text_color="Black",
    fg_color="white",
    font=("Arial", 9, "italic"),
    width=300,   
    height=20  
)
footer.place(x=0, y=660)  

        
root.mainloop()