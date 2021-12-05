from flask import Flask, request
from flask_restful import Resource, Api
from habilidades import Habilidades, ListaHabilidades
import json

app = Flask(__name__)
api = Api(app)


desenvolvedores = [
    {
    'id':'0',
    'nome':'Rafael',
     'habilidades':['Python', 'Flask']
     },
    {
    'id':'1',
    'nome':'Galleani',
     'habilidades':['Python', 'Django']}
]

# devolve um desenvolvedor pelo ID, também altera e deleta um desenvolvedor #
class Desenvolvedor(Resource):
    def get(self, id):
        try:
            response = desenvolvedores[id]
        except IndexError:
            mensagem = 'Desenvolvedor de ID {} não existe'.format(id)
            response = {'status': 'erro', 'mensagem': mensagem}
        except Exception:
            mensagem = 'Erro desconhecido. Procure o administrador da API'
            response = {'status': 'erro', 'mensagem': mensagem}
        return (response)

    def put(self, id):
        dados = json.loads(request.data)
        desenvolvedores[id] = dados
        return dados

    def delete(self, id):
        desenvolvedores.pop(id)
        return {'status':'sucesso','mensagem':'Registro Excluído'}


# Lista todos os desenvolvedores e permite registrar um novo desenvolvedor #
class ListaDesenvolvedores(Resource):
    def get(self):
        return desenvolvedores

    def post(self):
        dados = json.loads(request.data)
        posicao = len(desenvolvedores)
        dados['id'] = posicao
        lista_habilidades_cadastradas = ListaHabilidades.get(self)
        lista_habilidades_dados = dados['habilidades']

        lista_habilidades_cadastradas_k = []

        for x in lista_habilidades_cadastradas:
            lista_habilidades_cadastradas_k.append(x['habilidade']);

        art = list(set(lista_habilidades_dados) - set(lista_habilidades_cadastradas_k))

        if art != []:
            return 'Habilidades {} não existe na lista'.format(art)

        desenvolvedores.append(dados)
        return desenvolvedores[posicao]

api.add_resource(Desenvolvedor, '/dev/<int:id>/')
api.add_resource(ListaDesenvolvedores, '/dev/')
api.add_resource(ListaHabilidades, '/habilidades/')
api.add_resource(Habilidades, '/habilidades/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)