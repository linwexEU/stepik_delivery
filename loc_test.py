from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 2)

    @task
    def get_task(self):
        self.client.get("/cart/")
