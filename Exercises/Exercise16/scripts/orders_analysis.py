from pymongo import MongoClient
from time import sleep
from datetime import datetime, timedelta

# Establish MongoDB connection
client = MongoClient('mongodb://root:example@localhost:27017/') 

# --- CORRECCIÓN 1: NOMBRES EXACTOS ---
db = client['ecommerce_db']       
collection = db['changes_orders'] 

def get_orders_per_status():
    pipeline = [
      { "$group": { "_id": "$status", "count": { "$sum": 1 } } },
      { "$sort": { "count": -1 } }
    ]
    
    results = collection.aggregate(pipeline)
    
    for result in results:
        # Usamos .get() por si el estado es nulo
        estado = result.get('_id', 'Unknown')
        print(f"Status: {estado} - Count: {result['count']}")

def get_top_price_order():
    # Buscamos todos, ordenamos por 'total_amount' descendente (-1) y limitamos a 1
    top_order_cursor = collection.find().sort("total_amount", -1).limit(1)
    
    # Convertimos cursor a lista
    top_order = list(top_order_cursor)
    
    if top_order:
        # Extraemos los datos del primer (y único) resultado
        order = top_order[0]
        oid = order.get('order_id', 'N/A')
        amount = order.get('total_amount', 0)
        print(f"Top price order: Order ID {oid} - Total Amount: ${amount:.2f}")
    else:
        print("No orders found.")

try:
    print("Iniciando análisis... (Ctrl+C para salir)")
    while True:
        print("-" * 40)
        print(f"Order status count at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:")
        print("-" * 40)
        get_orders_per_status()
        print("-" * 40)
        get_top_price_order()
        print("-" * 40)
        print("\n")
        sleep(10)  # Wait for 10 seconds before running again
except KeyboardInterrupt:
    print("Process stopped by user.")
finally:
    client.close()