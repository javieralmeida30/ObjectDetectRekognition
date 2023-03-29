import boto3
import csv
from PIL import Image, ImageDraw, ImageFont, ImageTk
import io
import tkinter as tk
from tkinter import filedialog

# Credenciales de AWS

with open('credentials.csv', 'r') as file:
    next(file)
    reader = csv.reader(file)
    for line in reader:
        access_key_ID = line[0]
        secret_access_key = line[1]

# Configurar el cliente de Rekognition
client = boto3.client('rekognition',
                      aws_access_key_id=access_key_ID,
                      aws_secret_access_key=secret_access_key,
                      region_name='aws-region-number')

# Configuración de la ventana
root = tk.Tk()
root.title("Detector de objetos en imágenes")
root.geometry("800x600")

# Imagen de fondo
bg_image = tk.PhotoImage(file="C:\\Users\...background.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0)

# Función para mostrar los resultados
def show_results(detect_objects):
    # Imagen original
    imagen = Image.open(io.BytesIO(source_bytes))
    draw = ImageDraw.Draw(imagen)

    font = ImageFont.truetype("arial.ttf", 18)

    for label in detect_objects['Labels']:
        print(label["Name"])
        print("Confidence: ", label["Confidence"])

        for instances in label['Instances']:
            if 'BoundingBox' in instances:

                box = instances["BoundingBox"]

                left = imagen.width * box['Left']
                top = imagen.height * box['Top']
                width = imagen.width * box['Width']
                height = imagen.height * box['Height']

                points = (
                            (left,top),
                            (left + width, top),
                            (left + width, top + height),
                            (left , top + height),
                            (left, top)
                        )
                draw.line(points, width=5, fill = "#20e641")

                shape = [(left - 2, top - 45), (width + 2 + left, top)]
                draw.rectangle(shape, fill = "#20e641")

                draw.text((left + 270, top - 40), label["Name"], font=font, fill='#000000')

    
    # Redimensionar la imagen si es demasiado grande
    max_size = (270, 500)
    imagen.thumbnail(max_size, Image.ANTIALIAS)
    
    # Mostrar la imagen con los resultados
    imagen.show()

    # Convertir la imagen a PhotoImage para mostrarla en la interfaz de tkinter
    modified_image = ImageTk.PhotoImage(imagen)

    # Mostrar la imagen modificada en un cuadro de texto
    image_label.config(image=modified_image)
    image_label.image = modified_image

    # Mostrar los resultados en la interfaz de tkinter
    result_label.config(text="Estos son los resultados de tu imagen:")
    results_text.config(state="normal")
    results_text.delete("1.0", tk.END)
    for label in detect_objects['Labels']:
        results_text.insert(tk.END, label["Name"] + "\n")
    results_text.config(state="disabled")

# Función para procesar la imagen
def process_image():
    # Abrir ventana para seleccionar la imagen
    file_path = filedialog.askopenfilename()

    # Leer la imagen seleccionada
    with open(file_path, 'rb') as image_file:
        global source_bytes
        source_bytes = image_file.read()

    # Detectar los objetos en la imagen
    detect_objects = client.detect_labels(Image={'Bytes': source_bytes})

    # Mostrar los resultados
    show_results(detect_objects)

# Botones
def on_process_button_click():
    process_image()
    
process_button = tk.Button(root, text="Procesar imagen", font=("Arial Bold", 20), command=on_process_button_click)
process_button.place(x=370, y=500)

def on_exit_button_click():
    root.destroy()
    
exit_button = tk.Button(root, text="Salir", font=("Arial Bold", 20), command=on_exit_button_click)
exit_button.place(x=610, y=500)

image_label = tk.Label(root)
image_label.place(x=50, y=50)

result_label = tk.Label(root, font=("Arial Bold", 16))
result_label.place(x=350, y=50)

results_text = tk.Text(root, height=10, width=30, font=("Arial", 16), state="disabled")
results_text.place(x=350, y=100)

root.mainloop()
