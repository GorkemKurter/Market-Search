import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
import webbrowser

def filter_options_wm(country_selected):
    options_window = tk.Toplevel(root)
    options_window.title("Görüntüleme seçenekleri")
    options_window.configure(background="#333333")
    options_window.geometry(f"{1024}x{720}")

    left_frame = tk.Frame(options_window, bg='#333333')
    button_container = tk.Frame(left_frame, bg="#333333")

    button_container.pack(expand=True, fill="both")
    left_frame.pack(expand=True, fill="both", side="left")

    right_frame = tk.Frame(options_window, bg="#333333")
    filter_container = tk.Frame(right_frame, bg="#333333")

    filter_container.pack(expand=True, fill="both")
    right_frame.pack(expand=True, fill="both", side="right")

    machine_option_var = tk.StringVar()

    filter_option_var = tk.StringVar()

    option_6kg_1000rpm = tk.Radiobutton(button_container, text="6 kg 1000 rpm", variable=machine_option_var,
                                        value="6 kg 1000 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_6kg_1200rpm = tk.Radiobutton(button_container, text="6 kg 1200 rpm", variable=machine_option_var,
                                        value="6 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_6kg_1400rpm = tk.Radiobutton(button_container, text="6 kg 1400 rpm", variable=machine_option_var,
                                        value="6 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_7kg_1000rpm = tk.Radiobutton(button_container, text="7 kg 1000 rpm", variable=machine_option_var,
                                        value="7 kg 1000 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_7kg_1200rpm = tk.Radiobutton(button_container, text="7 kg 1200 rpm", variable=machine_option_var,
                                        value="7 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_7kg_1400rpm = tk.Radiobutton(button_container, text="7 kg 1400 rpm", variable=machine_option_var,
                                        value="7 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_8kg_1000rpm = tk.Radiobutton(button_container, text="8 kg 1000 rpm", variable=machine_option_var,
                                        value="8 kg 1000 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_8kg_1200rpm = tk.Radiobutton(button_container, text="8 kg 1200 rpm", variable=machine_option_var,
                                        value="8 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_8kg_1400rpm = tk.Radiobutton(button_container, text="8 kg 1400 rpm", variable=machine_option_var,
                                        value="8 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_8kg_1600rpm = tk.Radiobutton(button_container, text="8 kg 1600 rpm", variable=machine_option_var,
                                        value="8 kg 1600 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_9kg_1000rpm = tk.Radiobutton(button_container, text="9 kg 1000 rpm", variable=machine_option_var,
                                        value="9 kg 1000 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_9kg_1200rpm = tk.Radiobutton(button_container, text="9 kg 1200 rpm", variable=machine_option_var,
                                        value="9 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_9kg_1400rpm = tk.Radiobutton(button_container, text="9 kg 1400 rpm", variable=machine_option_var,
                                        value="9 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    option_10kg_1200rpm = tk.Radiobutton(button_container, text="10 kg 1200 rpm", variable=machine_option_var,
                                         value="10 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                         selectcolor='#666666', highlightcolor='#333333')

    option_10kg_1400rpm = tk.Radiobutton(button_container, text="10 kg 1400 rpm", variable=machine_option_var,
                                         value="10 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                         selectcolor='#666666', highlightcolor='#333333')

    option_filter_All = tk.Radiobutton(filter_container, text="Tüm ürünleri göster", variable=filter_option_var,
                                       value="Show All", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                       selectcolor='#666666', highlightcolor='#333333')

    option_filter_top5 = tk.Radiobutton(filter_container, text="En ucuz 5 ürünü göster", variable=filter_option_var,
                                        value="Top 5", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    country = country_selected

    filtered_search_button = tk.Button(filter_container, text="Ara", bg="#333333", fg="#FFFFFF", font=("Helvetica", 15),
                                       command=lambda: database_opener_wm(country, machine_option_var.get(),
                                                                          filter_option_var.get()))

    # Empty Labels:
    Unseen_label_1 = tk.Label(filter_container, text="", bg="#333333")
    Unseen_label_2 = tk.Label(button_container, text="", bg="#333333")

    Header_label = tk.Label(options_window, text="{} Marketi:{} Makineleri".format(country, "Çamaşır"), bg="#333333",
                            fg='#FFFFFF', font=("Helvetica", 20))

    Header_label.pack(anchor="center")
    separator_frame = tk.Frame(options_window, bg='#FFFFFF', width=3)
    separator_frame.pack(anchor="center", padx=20, fill="y", expand=True, pady=20)

    Unseen_label_2.pack(anchor="center", pady=10)
    option_6kg_1000rpm.pack(anchor="center", pady=10)
    option_6kg_1200rpm.pack(anchor="center", pady=10)
    option_6kg_1400rpm.pack(anchor="center", pady=10)
    option_7kg_1000rpm.pack(anchor="center", pady=10)
    option_7kg_1200rpm.pack(anchor="center", pady=10)
    option_7kg_1400rpm.pack(anchor="center", pady=10)
    option_8kg_1000rpm.pack(anchor="center", pady=10)
    option_8kg_1200rpm.pack(anchor="center", pady=10)
    option_8kg_1400rpm.pack(anchor="center", pady=10)
    option_8kg_1600rpm.pack(anchor="center", pady=10)
    option_9kg_1000rpm.pack(anchor="center", pady=10)
    option_9kg_1200rpm.pack(anchor="center", pady=10)
    option_9kg_1400rpm.pack(anchor="center", pady=10)
    option_10kg_1200rpm.pack(anchor="center", pady=10)
    option_10kg_1400rpm.pack(anchor="center", pady=10)

    Unseen_label_1.pack(anchor="center", pady=120)
    option_filter_All.pack(anchor="center", pady=25)
    option_filter_top5.pack(anchor="center", pady=30)
    filtered_search_button.pack(anchor="center")


def filter_options_wd(country_selected):
    options_window = tk.Toplevel(root)
    options_window.title("Görüntüleme seçenekleri")
    options_window.configure(background="#333333")
    options_window.geometry(f"{1024}x{720}")

    left_frame = tk.Frame(options_window, bg='#333333')
    button_container = tk.Frame(left_frame, bg="#333333")

    button_container.pack(expand=True, fill="both")
    left_frame.pack(expand=True, fill="both", side="left")

    right_frame = tk.Frame(options_window, bg="#333333")
    filter_container = tk.Frame(right_frame, bg="#333333")

    filter_container.pack(expand=True, fill="both")
    right_frame.pack(expand=True, fill="both", side="right")

    machine_option_var = tk.StringVar()

    filter_option_var = tk.StringVar()

    option_7_5kg_1200rpm = tk.Radiobutton(button_container, text="7&5 kg 1200 rpm", variable=machine_option_var,
                                          value="7&5 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                          selectcolor='#666666', highlightcolor='#333333')

    option_7_5kg_1400rpm = tk.Radiobutton(button_container, text="7&5 kg 1400 rpm", variable=machine_option_var,
                                          value="7&5 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                          selectcolor='#666666', highlightcolor='#333333')

    option_8_5kg_1200rpm = tk.Radiobutton(button_container, text="8&5 kg 1200 rpm", variable=machine_option_var,
                                          value="8&5 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                          selectcolor='#666666', highlightcolor='#333333')

    option_8_5kg_1400rpm = tk.Radiobutton(button_container, text="8&5 kg 1400 rpm", variable=machine_option_var,
                                          value="8&5 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                          selectcolor='#666666', highlightcolor='#333333')

    option_8_6kg_1200rpm = tk.Radiobutton(button_container, text="8&6 kg 1200 rpm", variable=machine_option_var,
                                          value="8&6 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                          selectcolor='#666666', highlightcolor='#333333')

    option_8_6kg_1400rpm = tk.Radiobutton(button_container, text="8&6 kg 1400 rpm", variable=machine_option_var,
                                          value="8&6 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                          selectcolor='#666666', highlightcolor='#333333')

    option_9_6kg_1400rpm = tk.Radiobutton(button_container, text="9&6 kg 1400 rpm", variable=machine_option_var,
                                          value="9&6 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                          selectcolor='#666666', highlightcolor='#333333')

    option_10_6kg_1400rpm = tk.Radiobutton(button_container, text="10&6 kg 1400 rpm", variable=machine_option_var,
                                           value="10&6 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20,
                                           indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_10_7kg_1400rpm = tk.Radiobutton(button_container, text="10&7 kg 1400 rpm", variable=machine_option_var,
                                           value="10&7 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20,
                                           indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_11_7kg_1400rpm = tk.Radiobutton(button_container, text="11&7 kg 1400 rpm", variable=machine_option_var,
                                           value="11&7 kg 1400 rpm", bg='#333333', fg='#FFFFFF', width=20,
                                           indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_12_8kg_1400rpm = tk.Radiobutton(button_container, text="12&8 kg 1200 rpm", variable=machine_option_var,
                                           value="12&8 kg 1200 rpm", bg='#333333', fg='#FFFFFF', width=20,
                                           indicatoron=0, selectcolor='#666666', highlightcolor='#333333')

    option_filter_All = tk.Radiobutton(filter_container, text="Tüm ürünleri göster", variable=filter_option_var,
                                       value="Show All", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                       selectcolor='#666666', highlightcolor='#333333')

    option_filter_top5 = tk.Radiobutton(filter_container, text="En ucuz 5 ürünü göster", variable=filter_option_var,
                                        value="Top 5", bg='#333333', fg='#FFFFFF', width=20, indicatoron=0,
                                        selectcolor='#666666', highlightcolor='#333333')

    country = country_selected

    filtered_search_button = tk.Button(filter_container, text="Ara", bg="#333333", fg="#FFFFFF", font=("Helvetica", 15),
                                       command=lambda: database_opener_wd(country, machine_option_var.get(),
                                                                          filter_option_var.get()))

    # Empty Labels:
    Unseen_label_1 = tk.Label(filter_container, text="", bg="#333333")
    Unseen_label_2 = tk.Label(button_container, text="", bg="#333333")

    Header_label = tk.Label(options_window,
                            text="{} Marketi:{} Makineleri".format(country, "Yıkayıcı Kurutucu Çamaşır"), bg="#333333",
                            fg='#FFFFFF', font=("Helvetica", 20))

    Header_label.pack(anchor="center")
    separator_frame = tk.Frame(options_window, bg='#FFFFFF', width=3)
    separator_frame.pack(anchor="center", padx=20, fill="y", expand=True, pady=20)

    Unseen_label_2.pack(anchor="center", pady=10)
    option_7_5kg_1200rpm.pack(anchor="center", pady=10)
    option_7_5kg_1400rpm.pack(anchor="center", pady=10)
    option_8_5kg_1200rpm.pack(anchor="center", pady=10)
    option_8_5kg_1400rpm.pack(anchor="center", pady=10)
    option_8_6kg_1200rpm.pack(anchor="center", pady=10)
    option_8_6kg_1400rpm.pack(anchor="center", pady=10)
    option_9_6kg_1400rpm.pack(anchor="center", pady=10)
    option_10_6kg_1400rpm.pack(anchor="center", pady=10)
    option_10_7kg_1400rpm.pack(anchor="center", pady=10)
    option_11_7kg_1400rpm.pack(anchor="center", pady=10)
    option_12_8kg_1400rpm.pack(anchor="center", pady=10)

    Unseen_label_1.pack(anchor="center", pady=120)
    option_filter_All.pack(anchor="center", pady=25)
    option_filter_top5.pack(anchor="center", pady=30)
    filtered_search_button.pack(anchor="center")

def machine_selecting_wm(machine_option_var,adress,query):

    if machine_option_var == "6 kg 1000 rpm":
        parameter = ('%6%', '1000')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "6 kg 1200 rpm":
        parameter = ('%6%', '1200')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "6 kg 1400 rpm":
        parameter = ('%6%', '1400')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "7 kg 1000 rpm":
        parameter = ('%7%', '1000')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "7 kg 1200 rpm":
        parameter = ('%7%', '1200')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "7 kg 1400 rpm":
        parameter = ('%7%', '1400')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "8 kg 1000 rpm":
        parameter = ('%8%', '1000')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "8 kg 1200 rpm":
        parameter = ('%8%', '1200')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "8 kg 1400 rpm":
        parameter = ('%8%', '1400')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "8 kg 1600 rpm":
        parameter = ('%8%', '1600')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "9 kg 1000 rpm":
        parameter = ('%9%', '1000')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "9 kg 1200 rpm":
        parameter = ('%9%', '1200')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "9 kg 1400 rpm":
        parameter = ('%9%', '1400')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "10 kg 1200 rpm":
        parameter = ('%10%', '1200')
        show_database_window_wm(adress, query, parameter)

    elif machine_option_var == "10 kg 1400 rpm":
        parameter = ('%10%', '1400')
        show_database_window_wm(adress, query, parameter)

def machine_selecting_wd(machine_option_var,adress,query):
    if machine_option_var == "7&5 kg 1200 rpm":
        parameter = ('%7%', '%5%', '1200')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "7&5 kg 1400 rpm":
        parameter = ('%7%', '%5%', '1400')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "8&5 kg 1200 rpm":
        parameter = ('%8%', '%5%', '1200')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "8&5 kg 1400 rpm":
        parameter = ('%8%', '%5%', '1400')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "8&6 kg 1200 rpm":
        parameter = ('%8%', '%6%', '1200')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "8&6 kg 1400 rpm":
        parameter = ('%8%', '%6%', '1400')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "9&6 kg 1400 rpm":
        parameter = ('%9%', '%6%', '1400')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "10&6 kg 1400 rpm":
        parameter = ('%10%', '%6%', '1400')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "10&7 kg 1400 rpm":
        parameter = ('%10%', '%7%', '1400')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "11&7 kg 1400 rpm":
        parameter = ('%11%', '%7%', '1400')
        show_database_window_wd(adress, query, parameter)

    elif machine_option_var == "12&8 kg 1200 rpm":
        parameter = ('%12%', '%8%', '1200')
        show_database_window_wd(adress, query, parameter)



def database_opener_wm(country, machine_option_var, filter_option_var):

    if country == "Fransa" and filter_option_var == "Show All":
        adress = r"marketscrapping\French Market\washingmachines_fr.db"
        query = f"SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines where CAPACITY_kg LIKE ? and RPM=? ORDER BY PRICE ASC"
        machine_selecting_wm(machine_option_var,adress,query)
    elif country == "Fransa" and filter_option_var == "Top 5":
        adress = r"marketscrapping\French Market\washingmachines_fr.db"
        query = f"SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines where CAPACITY_kg LIKE ? and RPM=? ORDER BY PRICE ASC LIMIT 5"
        machine_selecting_wm(machine_option_var, adress, query)

    if country == "İngiltere" and filter_option_var == "Show All":
        adress = r"marketscrapping\England Market\washingmachines_en.db"
        query = f"SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines where CAPACITY_kg LIKE ? and RPM=? ORDER BY PRICE ASC"
        machine_selecting_wm(machine_option_var, adress, query)
    elif country == "İngiltere" and filter_option_var == "Top 5":
        adress = r"marketscrapping\England Market\washingmachines_en.db"
        query = f"SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines where CAPACITY_kg LIKE ? and RPM=? ORDER BY PRICE ASC LIMIT 5"
        machine_selecting_wm(machine_option_var, adress, query)
def database_opener_wd(country, machine_option_var, filter_option_var):

    if country == "Fransa" and filter_option_var == "Show All":
        adress = r"marketscrapping\French Market\washerdryers_fr.db"
        query = f"SELECT BRAND_NAME, MODEL_NAME, CAPACITY_WASH, CAPACITY_DRY,RPM, PRICE, Product_Link FROM washerdryers where CAPACITY_WASH LIKE ? and CAPACITY_DRY LIKE ? and RPM=? ORDER BY PRICE ASC"
        machine_selecting_wd(machine_option_var,adress,query)
    elif country == "Fransa" and filter_option_var == "Top 5":
        adress = r"marketscrapping\French Market\washerdryers_fr.db"
        query = f"SELECT BRAND_NAME, MODEL_NAME, CAPACITY_WASH, CAPACITY_DRY,RPM, PRICE, Product_Link FROM washerdryers where CAPACITY_WASH LIKE ? and CAPACITY_DRY LIKE ? and RPM=? ORDER BY PRICE ASC LIMIT 5"
        machine_selecting_wd(machine_option_var,adress,query)

    if country == "İngiltere" and filter_option_var == "Show All":
        adress = r"marketscrapping\England Market\washerdryers_en.db"
        query = f"SELECT BRAND_NAME, MODEL_NAME, CAPACITY_WASH, CAPACITY_DRY,RPM, PRICE, Product_Link FROM washerdryers where CAPACITY_WASH LIKE ? and CAPACITY_DRY LIKE ? and RPM=? ORDER BY PRICE ASC"
        machine_selecting_wd(machine_option_var, adress, query)
    elif country == "İngiltere" and filter_option_var == "Top 5":
        adress = r"marketscrapping\England Market\washerdryers_en.db"
        query = f"SELECT BRAND_NAME, MODEL_NAME, CAPACITY_WASH, CAPACITY_DRY,RPM, PRICE, Product_Link FROM washerdryers where CAPACITY_WASH LIKE ? and CAPACITY_DRY LIKE ? and RPM=? ORDER BY PRICE ASC LIMIT 5"
        machine_selecting_wd(machine_option_var, adress, query)


def on_country_selected(*args):
    selected_country = country_var.get()


def Main_page_on_button_click():
    selected_country = country_var.get()
    selected_machine_type = machine_var.get()
    if (selected_country == "Fransa" or selected_country == "İngiltere") and selected_machine_type == "Çamaşır Makinesi":
        filter_options_wm(selected_country)
    elif (selected_country == "Fransa" or selected_country == "İngiltere") and selected_machine_type == "Yıkama-Kurutma Makinesi":
        filter_options_wd(selected_country)
    else:
        messagebox.showinfo("Uyarı", "Yapım aşamasında")
        machine_var.set("Çamaşır Makinesi")


def open_link(event):
    selected_item = tree.selection()[0]
    link = tree.item(selected_item, "values")[-1]
    webbrowser.open_new(link)


def show_database_window_wm(adress, query, parameter):
    global tree
    db_window = tk.Toplevel(root)
    db_window.title(f"{country_var.get()} Marketi")

    window_size = 1200
    db_window.geometry(f"{window_size}x{window_size}")

    filter_frame_label = ttk.Frame(db_window)
    filter_frame_label.pack(fill="both")

    filter_frame = ttk.Frame(db_window)
    filter_frame.pack(fill="both")

    frame = ttk.Frame(db_window)
    frame.pack(expand=True, fill="both")

    empty_label_searchfilter = tk.Label(filter_frame_label, text="Filtreleme:", font=("Helvetica", 20)).pack(
        side="left", anchor="n", padx=80)
    brand_name_label = tk.Label(filter_frame_label, text="Marka Adı", font=("Helvetica", 15)).pack(side="left",
                                                                                                   anchor="n", padx=45)
    model_name_label = tk.Label(filter_frame_label, text="Model Adı", font=("Helvetica", 15)).pack(side="left",
                                                                                                   anchor="n", padx=20)
    price_interval_label = tk.Label(filter_frame_label, text="Fiyat Aralığı(En düşük - En Yüksek)",
                                    font=("Helvetica", 15)).pack(side="left", anchor="n", padx=20)

    conn = sqlite3.connect(adress)
    cursor = conn.cursor()
    cursor.execute(query, parameter)
    table_data = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    tree = ttk.Treeview(frame, columns=column_names, show='headings', selectmode='extended')
    tree.column("MODEL_NAME", width=300)
    for col in column_names:
        tree.heading(col, text=col)
        if col != "MODEL_NAME":
            tree.column(col, width=10)
        if col == "PRODUCT_LINK":
            tree.column(col, width=300)
            tree.bind("<Button-1>", open_link)
    for row in table_data:
        tree.insert("", "end", values=row)

    conn.close()

    y_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)

    tree.grid(row=0, column=0, sticky="nsew")

    y_scrollbar.grid(row=0, column=1, sticky="ns")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    def reset_cmd():
        brand_name.set(value="")
        model_name.set(value="")
        price_highest.set(value="")
        price_lowest.set(value="")

        conn = sqlite3.connect(adress)
        cursor = conn.cursor()

        cursor.execute(query, parameter)
        results = cursor.fetchall()

        for data in results:
            tree.insert("", "end", values=data)

        conn.close()

    def inner_filter_cmd(brand_name_function, model_name_function, min_price_function, max_price_function):
        brand_name = brand_name_function
        model_name = model_name_function
        min_price = min_price_function
        max_price = max_price_function

        for item in tree.get_children():
            tree.delete(item)

        if min_price == "" and max_price == "":
            query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_kg LIKE ? AND RPM=? ORDER BY PRICE ASC"
            parameter_filter = (f"%{brand_name}%", f"%{model_name}%", f"%{parameter[0]}", parameter[1])
        elif min_price != "" and max_price == "":
            query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_kg LIKE ? AND RPM=? AND PRICE >= ? ORDER BY PRICE ASC"
            parameter_filter = (f"%{brand_name}%", f"%{model_name}%", f"%{parameter[0]}", parameter[1], min_price)
        elif min_price == "" and max_price != "":
            query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_kg LIKE ? AND RPM=? AND PRICE <= ? ORDER BY PRICE ASC"
            parameter_filter = (
            f"%{brand_name}%", f"%{model_name}%", f"%{parameter[0]}", parameter[1], min_price, max_price)
        elif min_price != "" and max_price != "":
            query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_kg LIKE ? AND RPM=? AND PRICE BETWEEN ? AND ? ORDER BY PRICE ASC"
            parameter_filter = (
            f"%{brand_name}%", f"%{model_name}%", f"%{parameter[0]}", parameter[1], min_price, max_price)

        # query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_kg LIKE ? AND RPM=? AND PRICE BETWEEN ? AND ? ORDER BY PRICE ASC"

        conn = sqlite3.connect(adress)
        cursor = conn.cursor()

        cursor.execute(query_filter, parameter_filter)
        results = cursor.fetchall()

        for data in results:
            tree.insert("", "end", values=data)

        conn.close()

    empty_label_texboxfield = tk.Label(filter_frame, text="").pack(side="left", anchor="n", padx=155)

    brand_name = tk.StringVar(value="")
    brand_name_textbox = tk.Entry(filter_frame, textvariable=brand_name)
    brand_name_textbox.pack(side="left", anchor="n", pady=15, padx=13)

    model_name = tk.StringVar(value="")
    model_name_textbox = tk.Entry(filter_frame, textvariable=model_name)
    model_name_textbox.pack(side="left", anchor="n", pady=15, padx=20)

    price_lowest = tk.StringVar(value="")
    price_lowest_textbox = tk.Entry(filter_frame, textvariable=price_lowest)
    price_lowest_textbox.pack(side="left", anchor="n", pady=15, padx=20)

    tk.Label(filter_frame, text="-", font=("Helvetica", 15)).pack(side="left", anchor="n", pady=15, padx=10)

    price_highest = tk.StringVar(value="")
    price_highest_textbox = tk.Entry(filter_frame, textvariable=price_highest)
    price_highest_textbox.pack(side="left", anchor="n", pady=15, padx=20)

    Apply_button = tk.Button(filter_frame, text="Uygula", font=("Helvetica", 12),
                             command=lambda: inner_filter_cmd(brand_name.get(), model_name.get(), price_lowest.get(),
                                                              price_highest.get()))
    Apply_button.pack(side="left", anchor="n", pady=15, padx=10)
    Reset_button = tk.Button(filter_frame, text="Sıfırla", font=("Helvetica", 12), command=reset_cmd)
    Reset_button.pack(side="left", anchor="n", pady=15, padx=20)


def show_database_window_wd(adress, query, parameter):
    global tree
    db_window = tk.Toplevel(root)
    db_window.title(f"{country_var.get()} Marketi")

    window_size = 1200
    db_window.geometry(f"{window_size}x{window_size}")

    filter_frame_label = ttk.Frame(db_window)
    filter_frame_label.pack(fill="both")

    filter_frame = ttk.Frame(db_window)
    filter_frame.pack(fill="both")

    frame = ttk.Frame(db_window)
    frame.pack(expand=True, fill="both")

    empty_label_searchfilter = tk.Label(filter_frame_label, text="Filtreleme:", font=("Helvetica", 20)).pack(
        side="left", anchor="n", padx=80)
    brand_name_label = tk.Label(filter_frame_label, text="Marka Adı", font=("Helvetica", 15)).pack(side="left",
                                                                                                   anchor="n", padx=45)
    model_name_label = tk.Label(filter_frame_label, text="Model Adı", font=("Helvetica", 15)).pack(side="left",
                                                                                                   anchor="n", padx=20)
    price_interval_label = tk.Label(filter_frame_label, text="Fiyat Aralığı(En düşük - En Yüksek)",
                                    font=("Helvetica", 15)).pack(side="left", anchor="n", padx=20)

    conn = sqlite3.connect(adress)
    cursor = conn.cursor()
    cursor.execute(query, parameter)
    table_data = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    tree = ttk.Treeview(frame, columns=column_names, show='headings', selectmode='extended')
    tree.column("MODEL_NAME", width=300)
    for col in column_names:
        tree.heading(col, text=col)
        if col != "MODEL_NAME":
            tree.column(col, width=10)
        if col == "PRODUCT_LINK":
            tree.column(col, width=300)
            tree.bind("<Button-1>", open_link)
    for row in table_data:
        tree.insert("", "end", values=row)

    conn.close()

    y_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)

    tree.grid(row=0, column=0, sticky="nsew")

    y_scrollbar.grid(row=0, column=1, sticky="ns")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    def reset_cmd():
        brand_name.set(value="")
        model_name.set(value="")
        price_highest.set(value="")
        price_lowest.set(value="")

        conn = sqlite3.connect(adress)
        cursor = conn.cursor()

        cursor.execute(query, parameter)
        results = cursor.fetchall()

        for data in results:
            tree.insert("", "end", values=data)

        conn.close()

    def inner_filter_cmd(brand_name_function, model_name_function, min_price_function, max_price_function):
        brand_name = brand_name_function
        model_name = model_name_function
        min_price = min_price_function
        max_price = max_price_function

        for item in tree.get_children():
            tree.delete(item)

        if min_price == "" and max_price == "":
            query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_WASH, CAPACITY_DRY, RPM, PRICE, Product_Link FROM washerdryers WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_WASH LIKE ? AND CAPACITY_DRY LIKE ? AND RPM=?  ORDER BY PRICE ASC"
            parameter_filter = (f"%{brand_name}%", f"%{model_name}%", f"%{parameter[0]}", f"%{parameter[1]}", parameter[2])
        elif min_price != "" and max_price == "":
            query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_WASH, CAPACITY_DRY, RPM, PRICE, Product_Link FROM washerdryers WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_WASH LIKE ? AND CAPACITY_DRY LIKE ? AND RPM=? AND PRICE >= ? ORDER BY PRICE ASC"
            parameter_filter = (f"%{brand_name}%", f"%{model_name}%", f"%{parameter[0]}", f"%{parameter[1]}", parameter[2], min_price)
        elif min_price == "" and max_price != "":
            query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_WASH, CAPACITY_DRY, RPM, PRICE, Product_Link FROM washerdryers WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_WASH LIKE ? AND CAPACITY_DRY LIKE ? AND RPM=? AND PRICE <= ? ORDER BY PRICE ASC"
            parameter_filter = (f"%{brand_name}%", f"%{model_name}%", f"%{parameter[0]}", f"%{parameter[1]}", parameter[2], max_price)
        elif min_price != "" and max_price != "":
            query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_WASH, CAPACITY_DRY, RPM, PRICE, Product_Link FROM washerdryers WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_WASH LIKE ? AND CAPACITY_DRY LIKE ?  AND RPM=? AND PRICE BETWEEN ? AND ? ORDER BY PRICE ASC"
            parameter_filter = (f"%{brand_name}%", f"%{model_name}%", f"%{parameter[0]}", f"%{parameter[1]}", parameter[2], min_price, max_price)

        # query_filter = "SELECT BRAND_NAME, MODEL_NAME, CAPACITY_kg, RPM, PRICE, Product_Link FROM washingmachines WHERE (LOWER(BRAND_NAME) LIKE LOWER(?) OR BRAND_NAME = '') AND (LOWER(MODEL_NAME) LIKE LOWER(?) OR MODEL_NAME = '') AND CAPACITY_kg LIKE ? AND RPM=? AND PRICE BETWEEN ? AND ? ORDER BY PRICE ASC"

        conn = sqlite3.connect(adress)
        cursor = conn.cursor()

        cursor.execute(query_filter, parameter_filter)
        results = cursor.fetchall()

        for data in results:
            tree.insert("", "end", values=data)

        conn.close()

    empty_label_texboxfield = tk.Label(filter_frame, text="").pack(side="left", anchor="n", padx=155)

    brand_name = tk.StringVar(value="")
    brand_name_textbox = tk.Entry(filter_frame, textvariable=brand_name)
    brand_name_textbox.pack(side="left", anchor="n", pady=15, padx=13)

    model_name = tk.StringVar(value="")
    model_name_textbox = tk.Entry(filter_frame, textvariable=model_name)
    model_name_textbox.pack(side="left", anchor="n", pady=15, padx=20)

    price_lowest = tk.StringVar(value="")
    price_lowest_textbox = tk.Entry(filter_frame, textvariable=price_lowest)
    price_lowest_textbox.pack(side="left", anchor="n", pady=15, padx=20)

    tk.Label(filter_frame, text="-", font=("Helvetica", 15)).pack(side="left", anchor="n", pady=15, padx=10)

    price_highest = tk.StringVar(value="")
    price_highest_textbox = tk.Entry(filter_frame, textvariable=price_highest)
    price_highest_textbox.pack(side="left", anchor="n", pady=15, padx=20)

    Apply_button = tk.Button(filter_frame, text="Uygula", font=("Helvetica", 12),
                             command=lambda: inner_filter_cmd(brand_name.get(), model_name.get(), price_lowest.get(),
                                                              price_highest.get()))
    Apply_button.pack(side="left", anchor="n", pady=15, padx=10)
    Reset_button = tk.Button(filter_frame, text="Sıfırla", font=("Helvetica", 12), command=reset_cmd)
    Reset_button.pack(side="left", anchor="n", pady=15, padx=20)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pazar Görüntüleme")

    root.configure(bg='#333333')

    root.geometry("400x350")

    title_label = tk.Label(root, text="Pazar Görüntüleme", font=("Helvetica", 16), bg='#333333', fg='#FFFFFF')
    title_label.pack(pady=10)

    welcome_label = tk.Label(root, text="Hoşgeldiniz!", font=("Helvetica", 12), bg='#333333', fg='#FFFFFF')
    welcome_label.pack(pady=10)

    country_label = tk.Label(root, text="Ülke Seçiniz", font=("Helvetica", 12), bg='#333333', fg='#FFFFFF')
    country_label.pack()

    countries = ["Fransa", "Almanya", "İngiltere", "İspanya", "İtalya", "Rusya", "Tümü"]
    country_var = tk.StringVar()
    country_combobox = ttk.Combobox(root, textvariable=country_var, values=countries)
    country_combobox.pack(pady=5)
    country_combobox.set(countries[0])
    country_var.trace_add("write", on_country_selected)

    tk.Label(root, text="", bg='#333333').pack(pady=5)

    machine_label = tk.Label(root, text="Makine Türü Seçiniz", font=("Helvetica", 12), bg='#333333', fg='#FFFFFF')
    machine_label.pack()

    machine_var = tk.StringVar(value="Çamaşır Makinesi")
    washer_radiobutton = tk.Radiobutton(root, text="Çamaşır Makinesi", variable=machine_var, value="Çamaşır Makinesi",
                                        bg='#333333', fg='#FFFFFF', indicatoron=1, selectcolor='#333333',
                                        highlightcolor='#333333')
    washer_radiobutton.pack(pady=2)

    dryer_radiobutton = tk.Radiobutton(root, text="Yıkama-Kurutma Makinesi", variable=machine_var,
                                       value="Yıkama-Kurutma Makinesi", bg='#333333', fg='#FFFFFF', indicatoron=1,
                                       selectcolor='#333333', highlightcolor='#333333')
    dryer_radiobutton.pack(pady=2)

    tk.Label(root, text="", bg='#333333').pack(pady=5)

    open_button = tk.Button(root, text="Aç", command=Main_page_on_button_click, font=("Helvetica", 12), bg='#333333',
                            fg='#FFFFFF')
    open_button.pack(pady=10)
    root.mainloop()
