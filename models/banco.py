from datetime import datetime
import locale
from models.agend import Agendamento
import sqlite3

class Modelo:
    def conecta(self):
        try:
            self.con = sqlite3.connect('floratime.db')
            self.cursor = self.con.cursor()
            print(">>> Conectado ao BD")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return False

    def desconecta(self):
        if self.con:
            self.cursor.close()
            self.con.close()

    def gera_banco(self):
        if not self.conecta():
            return False

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        print(">>> Tabela USER criada")

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS agendamento(
                ordem INTEGER PRIMARY KEY AUTOINCREMENT,
                horario DATETIME NOT NULL,
                cliente TEXT NOT NULL,
                endereco TEXT NOT NULL,
                servico TEXT NOT NULL,
                valor REAL NOT NULL,
                observacao TEXT
            )
        ''')
        print(">>> Tabela AGENDAMENTO criada")

        self.cursor.execute("SELECT * FROM user WHERE username = 'Admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("""
                INSERT INTO user(username, password)
                VALUES('Admin', 'teste123')
            """)
        print(">>> User ADMIN criado")
        if self.cursor.rowcount > 0:
            self.con.commit()
        self.desconecta()

    def insert(self, obj):
        if not self.conecta():
            return False

        sql = """
            INSERT INTO agendamento (horario, cliente, endereco, servico, valor, observacao)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (
            obj.horario,
            obj.cliente,
            obj.endereco,
            obj.servico,
            obj.valor,
            obj.observacao
        )

        try:
            self.cursor.execute(sql, values)
            self.con.commit()
            insert = True
        except sqlite3.Error as e:
            print(f"Erro ao inserir dados: {e}")
            insert = False
        finally:
            self.desconecta()
        return insert

    def update(self, obj):
        if not self.conecta():
            return False

        sql = """
            UPDATE agendamento
            SET horario = ?, cliente = ?, endereco = ?, servico = ?, valor = ?, observacao = ?
            WHERE ordem = ?
        """
        values = (
            obj.horario,
            obj.cliente,
            obj.endereco,
            obj.servico,
            obj.valor,
            obj.observacao,
            obj.ordem
        )

        updated = False
        try:
            self.cursor.execute(sql, values)
            if self.cursor.rowcount > 0:
                self.con.commit()
                updated = True
        except sqlite3.Error as e:
            print(f"Erro ao atualizar dados: {e}")
            updated = False
        finally:
            self.desconecta()
        return updated

    def delete(self, ordem):
        if not self.conecta():
            return False

        sql = "DELETE FROM agendamento WHERE ordem = ?"

        try:
            self.cursor.execute(sql, (ordem,))
            if self.cursor.rowcount > 0:
                self.con.commit()
                return True
        except sqlite3.Error as e:
            print(f"Erro ao excluir dados: {e}")
            return False
        finally:
            self.desconecta()

    def select(self, ordem):
        if not self.conecta():
            return False

        sql = "SELECT * FROM agendamento WHERE ordem = ?"
        agend = None

        try:
            self.cursor.execute(sql, (ordem,))
            dados = self.cursor.fetchone()
            if dados:
                agend = Agendamento(dados[0], dados[1], dados[2], dados[3], dados[4], dados[5], dados[6])
        except sqlite3.Error as e:
            print(f"Erro ao selecionar dados: {e}")
        finally:
            self.desconecta()
        return agend

    def select_all(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        if not self.conecta():
            return False

        agendamentos = []
        try:
            self.cursor.execute("SELECT * FROM agendamento")
            dados = self.cursor.fetchall()
            if dados:
                for item in dados:
                    data_obj = datetime.strptime(item[1], "%Y-%m-%dT%H:%M")
                    data = data_obj.strftime("%H:%M %d/%m/%Y")
                    end = f"Rua: {item[3]}"
                    val = locale.currency(item[5], grouping=True)
                    agend = Agendamento(item[0], data, item[2], end, item[4], val, item[6])
                    agendamentos.append(agend)
        except sqlite3.Error as e:
            print(f"Erro ao selecionar todos os dados: {e}")
        finally:
            self.desconecta()
        return agendamentos

    def valida_login(self):
        if not self.conecta():
            return False

        try:
            self.cursor.execute("SELECT * FROM user WHERE id = 1")
            dados = self.cursor.fetchone()
            if dados:
                login = (dados[0], dados[1], dados[2])
        except sqlite3.Error as e:
            print(f"Erro ao selecionar dados de login: {e}")
        finally:
            self.desconecta()
        return login