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
        self.queue_history = Queue() 
        self.stack_undo = Stack()  
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
        
        # undo 
        tk.Button(frame_tombol, text="Undo", command=self.undo_action,
                  bg="#FF9800", fg="white", padx=10).pack(side="left", padx=5)

        # histori
        tk.Button(root, text="Lihat History", command=self.show_history).pack(pady=5)

    def _buat_entry(self, parent, label, row):
            tk.Label(parent, text=label).grid(row=row, column=0, sticky="w")
            entry = tk.Entry(parent, width=10)
            entry.grid(row=row, column=1, pady=3)
            return entry
        
    def tambah_matakuliah(self):
                try:
                    nama = self.entry_nama.get().strip()
                    sks_str = self.combo_sks.get().strip()
                    
                    if not nama:
                        messagebox.showerror("Error", "Nama mata kuliah harus diisi")
                        return
                    
                    if not sks_str:
                        messagebox.showerror("Error", "Jumlah SKS harus dipilih")
                        return
                        
                    sks = int(sks_str)
                    
                    # validasi nilai wok
                    try:
                        p_uas = float(self.persen_uas.get() or 0)
                        p_uts = float(self.persen_uts.get() or 0)
                        p_quiz = float(self.persen_quiz.get() or 0)
                        p_tugas = float(self.persen_tugas.get() or 0)
                        p_absen = float(self.persen_absensi.get() or 0)
                        
                        total = p_uas + p_uts + p_quiz + p_tugas + p_absen
                        
                        p_responsi = 0
                        if sks == 3:
                            # kalau 3 tambah responsi
                            self.label_responsi.grid(row=5, column=0, sticky="w")
                            self.entry_responsi.grid(row=5, column=1, pady=3)
                            
                            p_responsi = float(self.entry_responsi.get() or 0)
                            total += p_responsi
                        else:
                            self.label_responsi.grid_remove()
                            self.entry_responsi.grid_remove()
                        
                        if total != 100:
                            messagebox.showerror("Error", f"Total persentase HARUS 100% (Saat ini: {total}%)")
                            return
                        
                    except ValueError:
                        messagebox.showerror("Error", "Persentase komponen harus berupa angka")
                        return
        
                    persentase_dict = {
                        "persen_uas": p_uas,
                        "persen_uts": p_uts,
                        "persen_quiz": p_quiz,
                        "persen_tugas": p_tugas,
                        "persen_absensi": p_absen,
                        "persen_responsi": p_responsi
                    }
                    
        
                    persentase_str = f"UAS:{p_uas}%, UTS:{p_uts}%, Quiz:{p_quiz}%, Tugas:{p_tugas}%, Absen:{p_absen}%"
                    if sks == 3:
                        persentase_str += f", Responsi:{p_responsi}%"
                    
                    #auto increment saja
                    if self.linked_list_mk.size > 0:
                        max_id_mk = self.linked_list_mk.get_max_id()
                        id_mk = max_id_mk + 1
                    else:
                        id_mk = 1
        
                    data_mk = {
                        "id": id_mk,
                        "nama": nama,
                        "sks": sks, 
                        "persentase": persentase_dict
                    }
                    self.linked_list_mk.append(data_mk)
                    
        
                    item_id = self.tree_matakuliah.insert("", "end", values=(nama, sks, persentase_str), tags=(nama,))
                    
                    history_msg = f"Tambah mata kuliah {nama} (SKS: {sks})"
                    self.queue_history.enqueue(history_msg)
                    self.stack_undo.push({"action": "tambah", "data": data_mk, "id": id_mk})
                    
                    messagebox.showinfo("Sukses", f"Mata kuliah {nama} berhasil ditambahkan")
                    self.entry_nama.delete(0, tk.END)
                    self.combo_sks.set("")  
                    self.entry_nama.focus()
                except ValueError:
                    messagebox.showerror("Error", "SKS harus berupa angka (2 atau 3)")
                except Exception as e:
                    messagebox.showerror("Error", f"Terjadi kesalahan:\n{e}")

    def proses_hitung(self):
        try:
            nama = self.entry_nama.get()
            sks = int(self.combo_sks.get())

            p_uas = float(self.persen_uas.get())
            p_uts = float(self.persen_uts.get())
            p_quiz = float(self.persen_quiz.get())
            p_tugas = float(self.persen_tugas.get())
            p_absen = float(self.persen_absensi.get())

            total = p_uas + p_uts + p_quiz + p_tugas + p_absen

            p_responsi = 0
            if sks == 3:
                self.label_responsi.grid(row=5, column=0, sticky="w")
                self.entry_responsi.grid(row=5, column=1, pady=3)
                self.label_responsi2.grid(row=6, column=0, sticky="w")
                self.entry_responsi2.grid(row=6, column=1, pady=3)

                p_responsi = float(self.entry_responsi.get() or 0)
                total += p_responsi
            else:
                self.label_responsi.grid_remove()
                self.entry_responsi.grid_remove()
                self.label_responsi2.grid_remove()
                self.entry_responsi2.grid_remove()

            if total != 100:
                messagebox.showerror("Error", "Total persentase HARUS 100%")
                return

            nilai_uas = float(self.nilai_uas.get())
            nilai_uts = float(self.nilai_uts.get())
            nilai_quiz = float(self.nilai_quiz.get())
            nilai_tugas = float(self.nilai_tugas.get())
            nilai_absensi = float(self.nilai_absensi.get())

            nilai_responsi = float(self.entry_responsi2.get() or 0) if sks == 3 else 0

            nilai_akhir = (
                nilai_uas * p_uas/100 +
                nilai_uts * p_uts/100 +
                nilai_quiz * p_quiz/100 +
                nilai_tugas * p_tugas/100 +
                nilai_absensi * p_absen/100
            )

            if sks == 3:
                nilai_akhir += nilai_responsi * p_responsi/100


            nilai = nilai_akhir
            if nilai == 100:
                huruf, bobot = "A+", 4.0
            elif nilai >= 76:
                huruf, bobot = "A", 4.0
            elif nilai >= 71:
                huruf, bobot = "B+", 3.5
            elif nilai >= 66:
                huruf, bobot = "B", 3.0
            elif nilai >= 61:
                huruf, bobot = "C+", 2.5
            elif nilai >= 56:
                huruf, bobot = "C", 2.0
            elif nilai >= 45:
                huruf, bobot = "D", 1.0
            else:
                huruf, bobot = "E", 0.0


            # validasi nama
            nama_mahasiswa = self.nama_mhs.get().strip()
            if not nama_mahasiswa:
                messagebox.showerror("Error", "Nama mahasiswa harus diisi")
                return
            
            # cek udah di select belom
            if self.selected_matkul_id is None:
                messagebox.showerror("Error", "Pilih mata kuliah terlebih dahulu dari tabel")
                return
            
            id_matakuliah = self.selected_matkul_id
            
            # autoincrement nilai
            if self.nilaidatabase:
                new_id = max(self.nilaidatabase.keys()) + 1
            else:
                new_id = 1
            
            # Simpan ke nilaidatabase
            self.nilaidatabase[new_id] = {
                "id_matakuliah": id_matakuliah,
                "nama_mhs": nama_mahasiswa,
                "nilai_akhir": round(nilai_akhir, 2),
                "nilai_mutu": huruf
            }

            history_msg = f"Hitung nilai mata kuliah {nama} untuk mahasiswa {nama_mahasiswa} (Nilai: {round(nilai_akhir, 2)}, Huruf: {huruf})"
            self.queue_history.enqueue(history_msg)
            self.stack_undo.push({"action": "hitung", "data": self.nilaidatabase[new_id]})

            messagebox.showinfo("Sukses", f"Nilai berhasil dihitung untuk MK: {nama}\nMahasiswa: {nama_mahasiswa}\nNilai: {round(nilai_akhir, 2)} ({huruf})")
            
            # update yg di pilih
            self.update_tabel_nilai()
            
            # reset inputan
            self.nama_mhs.delete(0, tk.END)
            self.nilai_uas.delete(0, tk.END)
            self.nilai_uts.delete(0, tk.END)
            self.nilai_quiz.delete(0, tk.END)
            self.nilai_tugas.delete(0, tk.END)
            self.nilai_absensi.delete(0, tk.END)
            self.entry_responsi2.delete(0, tk.END)
            if sks == 3:
                self.label_responsi2.grid_remove()
                self.entry_responsi2.grid_remove()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan:\n{e}")


    def pilih_matakuliah(self, event):
            selection = self.tree_matakuliah.selection()
            if not selection:
                return
            
            item = selection[0]
            values = self.tree_matakuliah.item(item, "values")
            nama = values[0]
            sks = int(values[1])
            
            mk_data = self.linked_list_mk.find_by_nama_sks(nama, sks)
            
            if mk_data:
                self.selected_matkul_id = mk_data.get("id")
                self.frame_nilai.pack(fill="x", pady=(10, 0))
                self.entry_nama.delete(0, tk.END)
                self.entry_nama.insert(0, nama)
                self.combo_sks.set(str(sks))
    
                persen = mk_data.get("persentase", {})
                self.persen_uas.delete(0, tk.END)
                self.persen_uas.insert(0, str(persen.get("persen_uas", 0)))
                self.persen_uts.delete(0, tk.END)
                self.persen_uts.insert(0, str(persen.get("persen_uts", 0)))
                self.persen_quiz.delete(0, tk.END)
                self.persen_quiz.insert(0, str(persen.get("persen_quiz", 0)))
                self.persen_tugas.delete(0, tk.END)
                self.persen_tugas.insert(0, str(persen.get("persen_tugas", 0)))
                self.persen_absensi.delete(0, tk.END)
                self.persen_absensi.insert(0, str(persen.get("persen_absensi", 0)))
    
                p_responsi = persen.get("persen_responsi", 0)
                if sks == 3 and p_responsi > 0:
                    self.label_responsi.grid(row=5, column=0, sticky="w")
                    self.entry_responsi.grid(row=5, column=1, pady=3)
                    self.entry_responsi.delete(0, tk.END)
                    self.entry_responsi.insert(0, str(p_responsi))
                else:
                    self.label_responsi.grid_remove()
                    self.entry_responsi.grid_remove()
    
                # reset inputan
                self.nama_mhs.delete(0, tk.END)
                self.nilai_uas.delete(0, tk.END)
                self.nilai_uts.delete(0, tk.END)
                self.nilai_quiz.delete(0, tk.END)
                self.nilai_tugas.delete(0, tk.END)
                self.nilai_absensi.delete(0, tk.END)
                self.entry_responsi2.delete(0, tk.END)
                self.label_responsi2.grid_remove()
                self.entry_responsi2.grid_remove()
                
                # update tabel
                self.update_tabel_nilai()
        
    def deselect_matakuliah(self, event):
        self.selected_matkul_id = None
        self.frame_nilai.pack_forget()
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def update_tabel_nilai(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # nampilin data yang idnya sama ama yang dipilih (left join)
        if self.selected_matkul_id is not None:
            for id_nilai, data in self.nilaidatabase.items():
                if data.get("id_matakuliah") == self.selected_matkul_id:
                    nama_mhs = data.get("nama_mhs", "")
                    nilai_akhir = data.get("nilai_akhir", 0)
                    huruf = data.get("nilai_mutu", "")
                    self.tree.insert("", "end", values=(nama_mhs, round(nilai_akhir, 2), huruf))
    
    def hapus_matakuliah(self):
        selection = self.tree_matakuliah.selection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih mata kuliah yang ingin dihapus terlebih dahulu")
            return
        
        item = selection[0]
        values = self.tree_matakuliah.item(item, "values")
        nama = values[0]
        
        if not messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus mata kuliah {nama}?"):
            return
        
        self.tree_matakuliah.delete(item)
        
        sks = int(values[1])
        mk_data = self.linked_list_mk.find_by_nama_sks(nama, sks)
        id_mk_hapus = mk_data.get("id") if mk_data else None
        
        if id_mk_hapus: 
            self.linked_list_mk.delete_by_id(id_mk_hapus)
        
        if self.selected_matkul_id == id_mk_hapus:
            self.selected_matkul_id = None
            self.frame_nilai.pack_forget()

            for item in self.tree.get_children():
                self.tree.delete(item)
        
        history_msg = f"Hapus mata kuliah {nama}"
        self.queue_history.enqueue(history_msg)
        if mk_data:
            self.stack_undo.push({"action": "hapus", "data": mk_data})
        
        messagebox.showinfo("Sukses", f"Mata kuliah {nama} berhasil dihapus")
        
        self.entry_nama.delete(0, tk.END)
        self.combo_sks.set("")
        self.persen_uas.delete(0, tk.END)
        self.persen_uts.delete(0, tk.END)
        self.persen_quiz.delete(0, tk.END)
        self.persen_tugas.delete(0, tk.END)
        self.persen_absensi.delete(0, tk.END)
        self.entry_responsi.delete(0, tk.END)
        self.nama_mhs.delete(0, tk.END)
        self.nilai_uas.delete(0, tk.END)
        self.nilai_uts.delete(0, tk.END)
        self.nilai_quiz.delete(0, tk.END)
        self.nilai_tugas.delete(0, tk.END)
        self.nilai_absensi.delete(0, tk.END)
        self.entry_responsi2.delete(0, tk.END)
        self.label_responsi.grid_remove()
        self.entry_responsi.grid_remove()
        self.label_responsi2.grid_remove()
        self.entry_responsi2.grid_remove()

    def undo_action(self):
        if self.stack_undo.is_empty():
            messagebox.showinfo("Info", "Tidak ada operasi yang bisa di-undo")
            return
        
        last_action = self.stack_undo.pop()
        action_type = last_action.get("action")
        
        try:
            if action_type == "tambah":
                data_mk = last_action.get("data")
                id_mk = last_action.get("id")
                
                if self.linked_list_mk.delete_by_id(id_mk):
                    # Hapus matkuknya
                    for item in self.tree_matakuliah.get_children():
                        values = self.tree_matakuliah.item(item, "values")
                        if values[0] == data_mk.get("nama") and int(values[1]) == data_mk.get("sks"):
                            self.tree_matakuliah.delete(item)
                            break
                    
                    messagebox.showinfo("Undo", f"Mata kuliah {data_mk.get('nama')} telah dihapus (undo)")
            
            elif action_type == "hapus":
                # undo hapus 
                data_mk = last_action.get("data")

                self.linked_list_mk.append(data_mk)
                
                # tambah kembali matkulnya
                nama = data_mk.get("nama")
                sks = data_mk.get("sks")
                persen = data_mk.get("persentase", {})
                persentase_str = f"UAS:{persen.get('persen_uas', 0)}%, UTS:{persen.get('persen_uts', 0)}%, Quiz:{persen.get('persen_quiz', 0)}%, Tugas:{persen.get('persen_tugas', 0)}%, Absen:{persen.get('persen_absensi', 0)}%"
                if sks == 3:
                    persentase_str += f", Responsi:{persen.get('persen_responsi', 0)}%"
                
                self.tree_matakuliah.insert("", "end", values=(nama, sks, persentase_str), tags=(nama,))
                
                messagebox.showinfo("Undo", f"Mata kuliah {nama} telah dikembalikan (undo)")
            
            elif action_type == "hitung":
                # undo hitung nilai
                data_nilai = last_action.get("data")
                id_matakuliah = data_nilai.get("id_matakuliah")
                
                # cari dan hapus dari nilaidatabase
                for id_nilai, nilai_data in list(self.nilaidatabase.items()):
                    if (nilai_data.get("id_matakuliah") == id_matakuliah and 
                        nilai_data.get("nama_mhs") == data_nilai.get("nama_mhs")):
                        del self.nilaidatabase[id_nilai]
                        break
                
                # update tabel nilai
                self.update_tabel_nilai()
                
                messagebox.showinfo("Undo", f"Nilai untuk {data_nilai.get('nama_mhs')} telah dihapus (undo)")
            
            # hapus juga dari queue history
            if not self.queue_history.is_empty():
                self.queue_history.dequeue()
                
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan undo:\n{e}")

    def show_history(self):
        window = tk.Toplevel()
        window.title("History Operasi")
        window.geometry("400x300")

        text = tk.Text(window, wrap="word")
        text.pack(fill="both", expand=True)

        # liat histori
        history_items = self.queue_history.display()
        for item in history_items:
            text.insert("end", "• " + item + "\n")


root = tk.Tk()
app = PenilaianGUI(root)
root.mainloop()




