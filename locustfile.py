from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    
    def on_start(self):
        # Reemplaza con credenciales válidas para la autenticación
        login_data = {'username': 'pcsan', 'password': '12345678'}
        self.client.post("/login/", login_data)
    
    @task
    def load_main_page(self):
        # Solicitud a la página principal
        self.client.get("/")

    @task
    def create_pedido(self):
        # Reemplaza con datos de prueba válidos para el pedido
        pedido_data = {'mesa': 1}
        self.client.post("/crear_pedido/", pedido_data)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Tiempo de espera entre tareas
    host = "http://localhost:8000"  # Asegúrate de que el puerto y la URL sean correctos
