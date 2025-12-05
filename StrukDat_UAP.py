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
