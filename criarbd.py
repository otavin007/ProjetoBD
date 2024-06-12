from apibdusers import database, app
from apibdusers.models import  Usuario, Funcionario, Cliente, Fornecedor, Mesa, Estoque, MateriaPrima,Pedido, Produto, PedidoProduto, Producao, MateriaPrimaProduto, MateriaPrimaFornecedor,  load_usuario



with app.app_context():
    database.create_all()