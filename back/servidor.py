from flask import Flask, jsonify, request, Response
from flask_restful import Resource, Api
from flask_cors import CORS
import mysql.connector
  
# para criar o  flask
app = Flask(__name__)
CORS(app) #habilitar qualuqer IP a fazer a requisição 
# creiar a  API 
api = Api(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dividas"
)
mycursor = mydb.cursor(buffered=True)

class Divida(Resource): #Resource é herança da entidade divida
    
    def get(self): # self para pertencer ao escopo da classe
        mycursor.execute("SELECT * FROM divida")
        result = mycursor.fetchall()
        
        row_headers = [ x[0] for x in mycursor.description ]
        dividas=[]
        for rv in result:
            dividas.append(dict(zip(row_headers,rv)))

        return jsonify(dividas) #retornar o objeto JSON
  
    # parte POST
    def post(self):
        data = request.get_json()     # pegar os dados da requisição

        nome_campos_validar = ['nome', 'cpf', 'email','divida', 'objeto', 'situacao'] #validação # mesma coisa usada em Javascript 
        campos_invalidos = []
        for campo in nome_campos_validar:
            if not data[campo]:
                campos_invalidos.append(campo)
        if len(campos_invalidos) > 0:
            return Response(", ".join(campos_invalidos), status=400)
        
        joker_values = [ "%s" for _ in range(len(data.keys())) ] # usando valores coringa substituidos pelos valores reais 
        values = tuple(data.values()) #ignora as chaves e so retorna os valores 
        
       

        sql = "INSERT INTO divida (" + ",".join(data.keys()) + ") VALUES (" + ",".join(joker_values) + ")"   # monta a quary e pega as chaves especificar em qual coluna vai armazenar as chaves separando por vírgula

        mycursor.execute(sql, values) #passando a query e os valores para armazenar no banco
        mydb.commit() # de fato efetuar as mmudanças no banco
        data['id'] = mycursor.rowcount #pegar a quantidade de linhas e armazenando no id

        return jsonify({'data': data})

#mapeando a entidade para formar a API 
# adicionando a resource correspondente 
api.add_resource(Divida, '/divida', '/divida/<int:num>') # declarando o padrão # quando acessar o servidor ele ficar assim primeiro parametro entidade segundo referência para id

# startar a aplicação
if __name__ == '__main__':
  
    app.run(debug = True)   
