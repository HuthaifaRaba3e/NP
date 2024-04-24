import tkinter as tk
from tkinter import ttk
import requests
from urllib.parse import urlparse

class PyBrowser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyBrowser")
        self.geometry("650x500")
        
        # Simple cache dictionary
        self.cache = {}
        
        # URL Entry
        self.url_label = tk.Label(self, text="URL:")
        self.url_label.grid(row=0, column=0, sticky="w")
        self.url_entry = tk.Entry(self, width=50)
        self.url_entry.grid(row=0, column=1, columnspan=2)

        # Method Dropdown
        self.method_label = tk.Label(self, text="Method:")
        self.method_label.grid(row=1, column=0, sticky="w")
        self.method_var = tk.StringVar()
        self.method_entry = ttk.Combobox(self, width=17, textvariable=self.method_var)
        self.method_entry['values'] = ('GET', 'POST', 'PUT', 'DELETE', 'HEAD')
        self.method_entry.current(0)
        self.method_entry.grid(row=1, column=1)

        # Headers Entry
        self.headers_label = tk.Label(self, text="Headers:")
        self.headers_label.grid(row=2, column=0, sticky="w")
        self.headers_entry = tk.Entry(self, width=50)
        self.headers_entry.grid(row=2, column=1, columnspan=2)

        # Response Text
        self.response_text = tk.Text(self, height=20, width=60)
        self.response_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        # Send Button
        self.send_button = tk.Button(self, text="Send Request", command=self.send_request)
        self.send_button.grid(row=4, column=1, pady=10)

    def send_request(self):
        url = self.url_entry.get()
        method = self.method_var.get()
        headers = self.parse_headers(self.headers_entry.get())

        # Check cache for GET requests
        if method == 'GET' and url in self.cache:
            response = self.cache[url]
            self.display_response(response, cached=True)
        else:
            try:
                response = requests.request(method, url, headers=headers)
                if method == 'GET':
                    self.cache[url] = response  # Cache the response
                self.display_response(response)
            except requests.exceptions.RequestException as e:
                self.response_text.delete(1.0, tk.END)
                self.response_text.insert(tk.END, f"Error: {str(e)}")

    def parse_headers(self, headers_str):
        headers = {}
        if headers_str:
            lines = headers_str.split('\n')
            for line in lines:
                line = line.strip()
                if line:
                    key_value = line.split(':', 1)
                    if len(key_value) == 2:
                        headers[key_value[0].strip()] = key_value[1].strip()
        return headers

    def display_response(self, response, cached=False):
        self.response_text.delete(1.0, tk.END)
        cache_status = " (from cache)" if cached else ""
        self.response_text.insert(tk.END, f"Status Code: {response.status_code}{cache_status}\n")
        self.response_text.insert(tk.END, "Headers:\n")
        self.response_text.insert(tk.END, f"{response.headers}\n\n")
        self.response_text.insert(tk.END, "Response Body:\n")
        self.response_text.insert(tk.END, response.text)

if __name__ == "__main__":
     app = PyBrowser()
     app.mainloop()
