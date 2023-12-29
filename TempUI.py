import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import webbrowser

def filter_options():
    options_window = tk.Toplevel(root)
    options_window.title("Görüntüleme seçenekleri")
    options_window.configure(background="#333333")
    options_window.geometry(f"{1024}x{720}")

    left_frame = tk.Frame(options_window, bg='#333333')
    button_container = tk.Frame(left_frame,bg="#333333")

    button_container.pack(expand=True,fill="both")
    left_frame.pack(expand=True, fill="both", side="left")

    right_frame = tk.Frame(options_window,bg="#333333")
    filter_container = tk.Frame(right_frame,bg="#333333")

    filter_container.pack(expand=True,fill="both")
    right_frame.pack(expand=True,fill="both",side="right")
    
    '''empty_label2 = tk.Label(options_window,text = "",bg="#333333")
    empty_label2.pack()

    empty_label3 = tk.Label(options_window,text = "",bg="#333333")
    empty_label3.pack(pady=5)'''   

    machine_option_var = tk.StringVar()

    filter_option_var = tk.StringVar()

    option_6kg_1000rpm = tk.Radiobutton(button_container, text="6 kg 1000 rpm", variable=machine_option_var, value="6kg 1000 rpm", bg='#333333', fg='#FFFFFF',width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_6kg_1200rpm = tk.Radiobutton(button_container, text="6 kg 1200 rpm", variable=machine_option_var, value="6 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_6kg_1400rpm = tk.Radiobutton(button_container, text="6 kg 1400 rpm", variable=machine_option_var, value="6 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_7kg_1000rpm = tk.Radiobutton(button_container, text="7 kg 1000 rpm", variable=machine_option_var, value="7 kg 1000 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_7kg_1200rpm = tk.Radiobutton(button_container, text="7 kg 1200 rpm", variable=machine_option_var, value="7 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_7kg_1400rpm = tk.Radiobutton(button_container, text="7 kg 1400 rpm", variable=machine_option_var, value="7 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_8kg_1000rpm = tk.Radiobutton(button_container, text="8 kg 1000 rpm", variable=machine_option_var, value="8 kg 1000 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_8kg_1200rpm = tk.Radiobutton(button_container, text="8 kg 1200 rpm", variable=machine_option_var, value="8 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_8kg_1400rpm = tk.Radiobutton(button_container, text="8 kg 1400 rpm", variable=machine_option_var, value="8 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_8kg_1600rpm = tk.Radiobutton(button_container, text="8 kg 1600 rpm", variable=machine_option_var, value="8 kg 1600 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_9kg_1000rpm = tk.Radiobutton(button_container, text="9 kg 1000 rpm", variable=machine_option_var, value="9 kg 1000 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_9kg_1200rpm = tk.Radiobutton(button_container, text="9 kg 1200 rpm", variable=machine_option_var, value="9 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_9kg_1400rpm = tk.Radiobutton(button_container, text="9 kg 1400 rpm", variable=machine_option_var, value="9 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_10kg_1200rpm = tk.Radiobutton(button_container, text="10 kg 1200 rpm", variable=machine_option_var, value="10 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_10kg_1400rpm = tk.Radiobutton(button_container, text="10 kg 1400 rpm", variable=machine_option_var, value="10 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')
    
    option_filter_All = tk.Radiobutton(filter_container,text="Tüm ürünleri göster", variable=filter_option_var, value="Show All", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')
    
    option_filter_top5 = tk.Radiobutton(filter_container,text="En ucuz 5 ürünü göster", variable=filter_option_var, value="Top 5", bg='#333333', fg='#FFFFFF', width=20 ,indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_6kg_1000rpm.pack(anchor="center",pady=10)
    option_6kg_1200rpm.pack(anchor="center",pady=10)
    option_6kg_1400rpm.pack(anchor="center",pady=10)
    option_7kg_1000rpm.pack(anchor="center",pady=10)
    option_7kg_1200rpm.pack(anchor="center",pady=10)
    option_7kg_1400rpm.pack(anchor="center",pady=10)
    option_8kg_1000rpm.pack(anchor="center",pady=10)
    option_8kg_1200rpm.pack(anchor="center",pady=10)
    option_8kg_1400rpm.pack(anchor="center",pady=10)
    option_8kg_1600rpm.pack(anchor="center",pady=10)
    option_9kg_1000rpm.pack(anchor="center",pady=10)
    option_9kg_1200rpm.pack(anchor="center",pady=10)
    option_9kg_1400rpm.pack(anchor="center",pady=10)
    option_10kg_1200rpm.pack(anchor="center",pady=10)
    option_10kg_1400rpm.pack(anchor="center",pady=10)
    option_filter_All.pack(anchor="center",pady=10)
    option_filter_top5.pack(anchor="center",pady=10)
    

def on_country_selected(*args):
    selected_country = country_var.get()
    welcome_label.config(text=f"Hoşgeldiniz! Ülke seçildi: {selected_country}")

def on_button_click():
    selected_country = country_var.get()
    if selected_country == "Fransa":
        #show_database_option_window()
        filter_options()
    else:
        messagebox.showinfo("Uyarı", "Yapım aşamasında")
        # Varsayılan olarak çamaşır makinesini seç
        machine_var.set("Çamaşır Makinesi")

def show_database_option_window():
    selected_machine = machine_var.get()
    show_database_window(selected_machine)

def open_link(event):
    selected_item = tree.selection()[0]
    link = tree.item(selected_item, "values")[-1]
    webbrowser.open_new(link)

def show_database_window(machine_type):
    global tree
    db_window = tk.Toplevel(root)
    db_window.title(f"{country_var.get()} Marketi")

    window_size = 1200
    db_window.geometry(f"{window_size}x{window_size}")

    # SQLite veritabanına bağlan
    conn = sqlite3.connect(r"C:\Users\gorkemk\Desktop\Genel\Market_Search\marketscrapping\French Market\washingmachines_but_fr.db")
    cursor = conn.cursor()

    # Tablo verilerini çek
    cursor.execute(f"SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines")
    table_data = cursor.fetchall()

    # Tablo başlıklarını al
    column_names = [desc[0] for desc in cursor.description]

    # Frame oluştur
    frame = ttk.Frame(db_window)
    frame.pack(expand=True, fill="both")

    # Veritabanı Treeview
    tree = ttk.Treeview(frame, columns=column_names, show='headings', selectmode='extended')
    tree.column("MODEL_NAME", width=300)
    for col in column_names:
        tree.heading(col, text=col)
        if col != "MODEL_NAME":
            tree.column(col, width=10)
        if col == "Product_Link":
            tree.column(col, width=300)
            tree.bind("<Button-1>", open_link)
    for row in table_data:
        tree.insert("", "end", values=row)

    # Dikey kaydırma çubuğu
    y_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)

    # Treeview'ı grid'e yerleştir
    tree.grid(row=0, column=0, sticky="nsew")

    # Kaydırma çubuğunu grid'e yerleştir
    y_scrollbar.grid(row=0, column=1, sticky="ns")

    # Grid konfigürasyonu
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Bağlantıyı kapat
    conn.close()

if __name__ == "__main__":
    # Ana pencereyi oluştur
    root = tk.Tk()
    root.title("Pazar Görüntüleme")

    # Arka plan rengini ayarla
    root.configure(bg='#333333')

    # Başlangıç boyutunu belirle
    root.geometry("400x350")

    # Başlık etiketi
    title_label = tk.Label(root, text="Pazar Görüntüleme", font=("Helvetica", 16), bg='#333333', fg='#FFFFFF')
    title_label.pack(pady=10)

    # Hoşgeldiniz etiketi
    welcome_label = tk.Label(root, text="Hoşgeldiniz!", font=("Helvetica", 12), bg='#333333', fg='#FFFFFF')
    welcome_label.pack(pady=10)

    # Ülke seçimi
    country_label = tk.Label(root, text="Ülke Seçiniz", font=("Helvetica", 12), bg='#333333', fg='#FFFFFF')
    country_label.pack()

    countries = ["Fransa", "Almanya", "İngiltere", "İspanya", "İtalya", "Rusya"]
    country_var = tk.StringVar()
    country_combobox = ttk.Combobox(root, textvariable=country_var, values=countries)
    country_combobox.pack(pady=5)
    country_combobox.set(countries[0])
    country_var.trace_add("write", on_country_selected)

    # Boşluk ekleyerek görünümü düzenle
    tk.Label(root, text="", bg='#333333').pack(pady=5)

    # Çamaşır makinesi ve yıkama-kurutma makinesi seçenekleri
    machine_label = tk.Label(root, text="Makine Türü Seçiniz", font=("Helvetica", 12), bg='#333333', fg='#FFFFFF')
    machine_label.pack()

    machine_var = tk.StringVar(value="Çamaşır Makinesi")  # Varsayılan olarak çamaşır makinesini seç
    washer_radiobutton = tk.Radiobutton(root, text="Çamaşır Makinesi", variable=machine_var, value="Çamaşır Makinesi", bg='#333333', fg='#FFFFFF', indicatoron=1, selectcolor='#333333', highlightcolor='#333333')
    washer_radiobutton.pack(pady=2)

    dryer_radiobutton = tk.Radiobutton(root, text="Yıkama-Kurutma Makinesi", variable=machine_var, value="Yıkama-Kurutma Makinesi", bg='#333333', fg='#FFFFFF', indicatoron=1, selectcolor='#333333', highlightcolor='#333333')
    dryer_radiobutton.pack(pady=2)

    # Boşluk ekleyerek görünümü düzenle
    tk.Label(root, text="", bg='#333333').pack(pady=5)

    # Aç butonu
    open_button = tk.Button(root, text="Aç", command=on_button_click, font=("Helvetica", 12), bg='#333333', fg='#FFFFFF')
    open_button.pack(pady=10)

    # Pencereyi göster
    root.mainloop()
