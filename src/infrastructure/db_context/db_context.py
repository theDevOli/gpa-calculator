import os

class Context:
    """Gerencia a persistência de dados em arquivos CSV para o sistema.

    Esta classe funciona como um contexto de banco de dados simplificado baseado em arquivos.
    Ela garante a criação do diretório de armazenamento, inicializa os arquivos com os 
    cabeçalhos corretos (`headers`) e provê operações básicas de CRUD (Create, Read, Update, Delete)
    diretamente nas linhas dos arquivos CSV (`student.csv` ou `course.csv`).

    Attributes:
        file_name (str): Nome do arquivo gerenciado por esta instância ('student.csv' ou 'course.csv').
        header (str): Cabeçalho correspondente às colunas do CSV do arquivo selecionado.
        path (str): Caminho absoluto completo para o arquivo físico no disco.
    """

    _student_header = "student_id,name,student_tax_id,courses_id"
    _course_header = "course_id,name,credit_hours,grade"

    def __init__(self, file_name: str):
        """Inicializa o contexto e garante a existência física do arquivo e diretório de banco de dados.

        Cria o diretório `db/` (caso não exista) um nível acima do arquivo atual e inicializa 
        o arquivo CSV correspondente com o cabeçalho apropriado caso o arquivo seja novo ou esteja vazio.

        Args:
            file_name (str): O nome do arquivo a ser gerenciado. Deve ser obrigatoriamente 
                             'student.csv' ou 'course.csv'.

        Raises:
            ValueError: Se `file_name` for vazio ou não for um dos dois valores permitidos.
        """
        if not file_name:
            raise ValueError("O nome do arquivo não pode ser vazio.")

        if file_name not in ("student.csv", "course.csv"):
            raise ValueError(
                "O nome do arquivo deve ser 'student.csv' ou 'course.csv'."
            )

        self.file_name = file_name
        self.header = (
            self._student_header
            if file_name == "student.csv"
            else self._course_header
        )

        db_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "db")
        )
        os.makedirs(db_dir, exist_ok=True)

        self.path = os.path.join(db_dir, self.file_name)

        if not os.path.exists(self.path) or os.path.getsize(self.path) == 0:
            with open(self.path, "w", encoding="utf-8") as file:
                file.write(self.header)

    def _reader(self) -> list[str]:
        """Lê o arquivo CSV de forma privada, ignorando o cabeçalho.

        Returns:
            list[str]: Uma lista de strings onde cada string representa uma linha não vazia 
                       do arquivo CSV (removendo espaços em branco das pontas). Retorna uma lista
                       vazia se o arquivo não existir.
        """
        if not os.path.exists(self.path):
            return []

        with open(self.path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        return [
            line.strip()
            for line in lines[1:]
            if line.strip()
        ]

    def _appender(self, csv_data: str) -> None:
        """Adiciona uma nova linha de dados de forma privada ao fim do arquivo.

        Garante a formatação correta de quebra de linha (`\\n`) apenas se o arquivo 
        já contiver dados além do cabeçalho inicial.

        Args:
            csv_data (str): A string formatada em CSV a ser adicionada ao arquivo.
        """
        with open(self.path, "a", encoding="utf-8") as file:
            if os.path.getsize(self.path) > len(self.header):
                file.write("\n")

            file.write(csv_data)

    def get_all_entities(self) -> list[str]:
        """Recupera todas as linhas de registros cadastrados (excluindo o cabeçalho).

        Returns:
            list[str]: Lista contendo as strings cruas de cada entidade salva no CSV.
        """
        return self._reader()

    def save_entity(self, csv_data: str) -> None:
        """Salva um novo registro de entidade no fim do arquivo CSV correspondente.

        Args:
            csv_data (str): String serializada em formato CSV representando a nova entidade.
        """
        self._appender(csv_data)

    def update_entity(self, updated_csv_data: str, entity_id: str) -> None:
        """Atualiza um registro existente no CSV com base no ID da entidade.

        O método reescreve o arquivo por completo, localizando a linha que se inicia com o 
        `entity_id` fornecido e substituindo-a pelos novos dados. As demais linhas permanecem intactas.

        Args:
            updated_csv_data (str): A linha em formato CSV contendo os dados atualizados da entidade.
            entity_id (str): O identificador único (ID) da entidade que será substituída.
        """
        lines = self._reader()

        with open(self.path, "w", encoding="utf-8") as file:
            file.write(self.header)

            for line in lines:
                if line.startswith(entity_id):
                    file.write(f"\n{updated_csv_data}")
                else:
                    file.write(f"\n{line}")

    def remove_entity(self, entity_id: str) -> None:
        """Remove um registro do arquivo CSV com base no ID da entidade.

        O método reescreve o arquivo por completo, omitindo a linha que se inicia com o
        `entity_id` fornecido.

        Args:
            entity_id (str): O identificador único (ID) da entidade a ser excluída.
        """
        lines = self._reader()

        with open(self.path, "w", encoding="utf-8") as file:
            file.write(self.header)

            for line in lines:
                if not line.startswith(entity_id):
                    file.write(f"\n{line}")