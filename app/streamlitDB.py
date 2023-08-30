import psycopg2

class db:

    def __init__(self, db_config):
        # Configurações do banco de dados
        self.db_config = db_config
    
    # Função para conectar-se ao banco de dados
    def connect_to_db(self):
        try:
            connection = psycopg2.connect(**self.db_config)
            return connection
        except Exception as e:
            print(f"Erro ao conectar-se ao banco de dados: {e}")
            return None
    
    # Função para inserir dados na tabela
    def inserir_dados(self, nome, email):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            
            insert_query = 'INSERT INTO usuario (nome, email) VALUES (%s, %s)'
            data = (nome, email)
            
            cursor.execute(insert_query, data)
            connection.commit()
            
            cursor.close()
            connection.close()
            
            print("Dados inseridos com sucesso.")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao inserir dados:", error)
    
    
    # Função para atualizar dados na tabela
    def atualizar_dados(self, id, novo_nome, novo_email):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            
            update_query = 'UPDATE usuario SET nome = %s, email = %s WHERE id = %s'
            data = (novo_nome, novo_email, id)
            
            cursor.execute(update_query, data)
            connection.commit()
            
            cursor.close()
            connection.close()
            
            print("Dados atualizados com sucesso.")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao atualizar dados:", error)
    
    # Função para ler dados da tabela
    def ler_dados(self):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            
            select_query = 'SELECT * FROM usuario'
            
            cursor.execute(select_query)
            resultados = cursor.fetchall()
            
            cursor.close()
            connection.close()
    
            return resultados
        except (Exception, psycopg2.Error) as error:
            print("Erro ao ler dados:", error)
    
    #Função para buscar id pelo nome e email
    def encontrar_id(self, nome, email):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
    
            search_query = 'SELECT id FROM usuario WHERE nome = %s AND email = %s;'
            data = (nome, email)
            
            cursor.execute(search_query, data)
            resultados = cursor.fetchall()
            ids = []
    
            for linha in resultados:
                ids.append(linha[0])
    
            cursor.close()
            connection.close()
    
            return ids
        except (Exception, psycopg2.Error) as error:
            print("Erro ao encontrar dados:", error)
    
    
    def buscar_por_id(self, id):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            
            search_query = 'SELECT * FROM usuario WHERE id = %s;'
            
            cursor.execute(search_query, (id,))
            resultado = cursor.fetchall()[0]
            
            cursor.close()
            connection.close()
    
            return resultado
        except (Exception, psycopg2.Error) as error:
            print("Erro ao encontrar dados:", error)

    def buscar_por_nome(self, nome):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            
            search_query = 'SELECT * FROM usuario WHERE nome ILIKE %s;'
            
            cursor.execute(search_query, (nome,))
            resultado = cursor.fetchall()
            
            cursor.close()
            connection.close()
    
            return resultado
        except (Exception, psycopg2.Error) as error:
            print("Erro ao encontrar dados:", error)
    
    
    #Função para deletar dados na tabela
    def deletar_dados(self, id):
        try:
            connection = self.connect_to_db()
            cursor = connection.cursor()
            
            excluded = self.buscar_por_id(id)
            delete_query = 'DELETE FROM usuario WHERE id = %s'
            data = (id,)

            cursor.execute(delete_query, data)
            connection.commit()
            print(excluded)
            
            cursor.close()
            connection.close()
            
            print("Dados deletados com sucesso.")
        except (Exception, psycopg2.Error) as error:
            print("Erro ao deletar dados:", error)