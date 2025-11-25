import mysql.connector
import random
import time
from datetime import datetime, timedelta

# Generador de datos
def generate_order():
    customer_id = random.randint(1, 100)
    # Convertimos la fecha a string compatible con MySQL
    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'])
    total_amount = round(random.uniform(50.0, 500.0), 2)
    payment_method = random.choice(['Credit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery'])
    shipping_address = f"{random.randint(100, 999)} Random St, City {chr(random.randint(65, 90))}"
    
    return (customer_id, order_date, status, total_amount, payment_method, shipping_address)

# --- CORRECCIÓN 1: USAR ROOT ---
# Database connection
connection = mysql.connector.connect(
    host='localhost',
    user='mysqluser',
    password='mysqlpw',
    database='ecommerce_db'
)
cursor = connection.cursor()

def insert_order():
    # 1. Generamos los datos
    val = generate_order()

    # --- CORRECCIÓN 2: EL CÓDIGO QUE FALTABA ---
    # Escribimos la instrucción SQL
    sql = """
    INSERT INTO orders 
    (customer_id, order_date, status, total_amount, payment_method, shipping_address) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        # 2. Ejecutamos la orden
        cursor.execute(sql, val)
        
        # --- CORRECCIÓN 3: COMMIT ---
        # ¡FUNDAMENTAL! Sin esto, los datos no se guardan permanentemente
        connection.commit()
        
        print(f"✅ Pedido insertado correctamente: ${val[3]} | Estado: {val[2]}")
        
    except mysql.connector.Error as err:
        print(f"❌ Error al insertar en MySQL: {err}")

try:
    print("🚀 Iniciando inserción de datos... (Ctrl+C para parar)")
    while True:
        insert_order()
        time.sleep(random.randint(1, 5)) # Espera entre 1 y 5 segundos
except KeyboardInterrupt:
    print("Proceso detenido por el usuario.")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada.")