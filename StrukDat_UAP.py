import tkinter as tk
from tkinter import ttk, messagebox

# LINKED LIST
class Node:
    def __init__(self, data):
        self.data = data  
        self.next = None 

class LinkedList:
    def __init__(self):
        self.head = None    
        self.size = 0  
    
    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def delete_by_id(self, id_mk):
        if self.head is None:
            return False
        
        if self.head.data.get("id") == id_mk:
            self.head = self.head.next
            self.size -= 1
            return True

        current = self.head
        while current.next is not None:
            if current.next.data.get("id") == id_mk:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def find_by_id(self, id_mk):
        current = self.head
        while current is not None:
            if current.data.get("id") == id_mk:
                return current.data
            current = current.next
        return None
    
    def find_by_nama_sks(self, nama, sks):
        current = self.head
        while current is not None:
            if (current.data.get("nama") == nama and 
                current.data.get("sks") == sks and 
                "persentase" in current.data):
                return current.data
            current = current.next
        return None
    
    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
    
    def get_max_id(self):
        if self.head is None:
            return 0
        max_id = 0
        current = self.head
        while current is not None:
            if current.data.get("id", 0) > max_id:
                max_id = current.data.get("id", 0)
            current = current.next
        return max_id
    
    def display(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

# QUEUE
class Queue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.pop(0)
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def peek(self):
        if self.is_empty():
            return None
        return self.items[0]
    
    def display(self):
        return self.items.copy()

# STACK
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def display(self):
        return self.items.copy()


class PenilaianGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Penilaian Mata Kuliah")
        self.root.geometry("1200x600")

        self.linked_list_mk = LinkedList()  
        self.queue_history = Queue()  # Queue untuk history operasi (FIFO)
        self.stack_undo = Stack()  # Stack untuk undo operasi (LIFO)
        self.selected_matkul_id = 0
        self.nilaidatabase = {}

        # container 
        container_horizontal = tk.Frame(root)
        container_horizontal.pack(fill="both", expand=True, padx=10, pady=10)

        frame_kiri = tk.Frame(container_horizontal)
        frame_kiri.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # input matkul
        frame = tk.LabelFrame(frame_kiri, text="Input Mata Kuliah", padx=10, pady=10)
        frame.pack(fill="x", pady=(0, 10))

        tk.Label(frame, text="Nama Mata Kuliah:").grid(row=0, column=0, sticky="w")
        self.entry_nama = tk.Entry(frame, width=30)
        self.entry_nama.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Jumlah SKS:").grid(row=1, column=0, sticky="w")
        self.combo_sks = ttk.Combobox(frame, values=[2, 3], width=5)
        self.combo_sks.grid(row=1, column=1, pady=5)

      
        # persentase input
        self.frame_persen = tk.LabelFrame(frame_kiri, text="Persentase Komponen (Total 100%)", padx=10, pady=10)
        self.frame_persen.pack(fill="x")

        self.persen_uas = self._buat_entry(self.frame_persen, "Persentase UAS:", 0)
        self.persen_uts = self._buat_entry(self.frame_persen, "Persentase UTS:", 1)
        self.persen_quiz = self._buat_entry(self.frame_persen, "Persentase Quiz:", 2)
        self.persen_tugas = self._buat_entry(self.frame_persen, "Persentase Tugas:", 3)
        self.persen_absensi = self._buat_entry(self.frame_persen, "Persentase Absensi:", 4)

        self.label_responsi = tk.Label(self.frame_persen, text="Persentase Responsi:")
        self.entry_responsi = tk.Entry(self.frame_persen, width=10)
        
        # button tambah mata kuliah
        tk.Button(frame_kiri, text="Tambah Mata Kuliah", command=self.tambah_matakuliah,
                  bg="#2196F3", fg="white", padx=10, pady=5).pack(pady=10)

        # form nilai 
        self.frame_nilai = tk.LabelFrame(frame_kiri, text="Input Nilai", padx=10, pady=10)

        tk.Label(self.frame_nilai, text="Nama Mahasiswa:").grid(row=0, column=0, sticky="w")
        self.nama_mhs = tk.Entry(self.frame_nilai, width=30)
        self.nama_mhs.grid(row=0, column=1, pady=3)
        
        self.nilai_uas = self._buat_entry(self.frame_nilai, "Nilai UAS:", 1)
        self.nilai_uts = self._buat_entry(self.frame_nilai, "Nilai UTS:", 2)
        self.nilai_quiz = self._buat_entry(self.frame_nilai, "Rata-Rata Quiz:", 3)
        self.nilai_tugas = self._buat_entry(self.frame_nilai, "Rata-Rata Tugas:", 4)
        self.nilai_absensi = self._buat_entry(self.frame_nilai, "Nilai Absensi (%):", 5)

        self.label_responsi2 = tk.Label(self.frame_nilai, text="Nilai Responsi Akhir:")
        self.entry_responsi2 = tk.Entry(self.frame_nilai, width=10)
        
        frame_kanan = tk.Frame(container_horizontal)
        frame_kanan.pack(side="right", fill="both", expand=True, padx=(5, 0))

        # tabel matkul
        frame_tabel = tk.LabelFrame(frame_kanan, text="Daftar Mata Kuliah", padx=10, pady=10)
        frame_tabel.pack(fill="x", pady=(0, 10))

        self.tree_matakuliah = ttk.Treeview(frame_tabel, columns=("nama", "sks", "persentase"), show="headings", height=8)
        self.tree_matakuliah.heading("nama", text="Nama Mata Kuliah")
        self.tree_matakuliah.heading("sks", text="SKS")
        self.tree_matakuliah.heading("persentase", text="Persentase")
        self.tree_matakuliah.pack(fill="x")
        
        # untuk select matkul 
        self.tree_matakuliah.bind("<<TreeviewSelect>>", self.pilih_matakuliah)
        self.tree_matakuliah.bind("<<TreeviewDeselect>>", self.deselect_matakuliah)

        # tabel nilai
        frame_tabel_nilai = tk.LabelFrame(frame_kanan, text="Tabel Nilai", padx=10, pady=10)
        frame_tabel_nilai.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame_tabel_nilai, columns=("nama", "nilai", "huruf"), show="headings")
        self.tree.heading("nama", text="Nama")
        self.tree.heading("nilai", text="Nilai Akhir")
        self.tree.heading("huruf", text="Huruf Mutu")
        self.tree.pack(fill="both", expand=True)

        # frame button
        frame_tombol = tk.Frame(root)
        frame_tombol.pack(pady=10)
        
        # hitung
        tk.Button(frame_tombol, text="Hitung & Tambah", command=self.proses_hitung,
                  bg="#4CAF50", fg="white", padx=10).pack(side="left", padx=5)
        
        # delete
        tk.Button(frame_tombol, text="Delete", command=self.hapus_matakuliah,
                  bg="#F44336", fg="white", padx=10).pack(side="left", padx=5)
        
        # undo (menggunakan Stack - LIFO)
        tk.Button(frame_tombol, text="Undo", command=self.undo_action,
                  bg="#FF9800", fg="white", padx=10).pack(side="left", padx=5)

        # histori
        tk.Button(root, text="Lihat History", command=self.show_history).pack(pady=5)

    def _buat_entry(self, parent, label, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
        entry = tk.Entry(parent, width=10)
        entry.grid(row=row, column=1, pady=3)
        return entry
