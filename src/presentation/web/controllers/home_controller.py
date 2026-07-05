import os
from flask import Flask, render_template

class HomeController:
    """Controller responsável pelas rotas globais da aplicação,

    como a página inicial e telas de erro (404).
    """

    def __init__(self, app: Flask):
        """Recebe a instância global do Flask criada no bootstrap."""
        self.app = app
        self._register_routes()

    def _register_routes(self):
        
        @self.app.route("/", methods=["GET"])
        def index():
            return render_template("index.html")

        @self.app.errorhandler(404)
        def page_not_found(e):
            return render_template("404.html"), 404