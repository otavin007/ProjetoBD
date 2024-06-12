from apibdusers import database, login_manager
from flask_login import UserMixin
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash




@login_manager.user_loader
def load_usuario(userid):
    user = Usuario.query.get(int(userid))
    if user:
        return jsonify({
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
            'pagou': user.pagou,
            'admin': user.admin,
            'idontaatual': user.idontaatual

        })
    return None

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    senha = database.Column(database.String, nullable=False)  # Alteramos para salvar a senha criptografada
    email = database.Column(database.String, nullable=False, unique=True)
    admin = database.Column(database.Boolean, nullable=False)

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)



class Endereco(database.Model):
    ID_Endereco = database.Column(database.Integer(8), nullable=False, unique=True)
    CEP = database.Column(database.Integer(8), nullable=False)
    Logradouro = database.Column(database.String(50), nullable=False)
    Bairro = database.Column(database.String(50), nullable=False)
    Cidade = database.Column(database.String(50), nullable=False)
    UF = database.Column(database.String(2), nullable=False)

class Cliente(database.Model):
    ID_Cliente = database.Column(database.Integer(8), primary_key=True, nullable=False, unique=True)
    ID_Endereco = database.Column(database.Integer(8), database.ForeignKey('Endereco.ID_Endereco'), nullable=False)
    NR_Cliente = database.Column(database.Integer(6), nullable=False)
    Complemento_Cliente = database.Column(database.String(50), nullable=False)
    Nome_Cliente = database.Column(database.String(50), nullable=False)
    CPF_Cliente = database.Column(database.Integer(11), nullable=False)
    Telefone_Cliente = database.Column(database.Integer(11), nullable=False, unique=True)
    Email_Cliente = database.Column(database.String(50), nullable=False, unique=True)
    Dt_Nasc_Cliente = database.Column(database.Date)


class Funcionario(database.Model):
    ID_Funcionario = database.Column(database.Integer(8), primary_key=True, nullable=False, unique=True)
    ID_Endereco = database.Column(database.Integer(8), database.ForeignKey('Endereco.ID_Endereco'), nullable=False)
    NR_Funcionario = database.Column(database.Integer(6), nullable=False)
    Complemento_Funcionario = database.Column(database.String(50), nullable=False)
    Nome_Funcionario = database.Column(database.String(50), nullable=False)
    
class Fornecedor(database.Model):
    ID_Fornecedor = database.Column(database.Integer(8), primary_key=True, nullable=False, unique=True)
    ID_Endereco = database.Column(database.Integer(8), database.ForeignKey('Endereco.ID_Endereco'), nullable=False)
    NR_Fornecedor = database.Column(database.Integer(6), nullable=False)
    Complemento_Fornecedor = database.Column(database.String(50), nullable=False)
    Nome_Fornecedor = database.Column(database.String(50), nullable=False, unique=True)
    CNPJ_Fornecedor = database.Column(database.Integer(14), nullable=False, unique=True)
    Telefone_Fornecedor = database.Column(database.Integer(11), nullable=False, unique=True)
    
class Mesa(database.Model):
    ID_Mesa = database.Column(database.Integer(8), primary_key=True, nullable=False, unique=True)
    Capacidade_Mesa = database.Column(database.Integer(2), nullable=False)
    Disponibilidade_Mesa = database.Column(database.Boolean, nullable=False)

class Estoque(database.Model):
    ID_Lote = database.Column(database.Integer(8), primary_key=True, nullable=False, unique=True)
    ID_Fornecedor = database.Column(database.Integer(8), database.ForeignKey('Fornecedor.ID_Fornecedor'), nullable=False)
    Dt_Fabricacao = database.Column(database.Date)
    Validade_Lote = database.Column(database.Date)
    Qtde_Estoque = database.Column(database.Integer(4), nullable=False)
    
class MateriaPrima(database.Model):
    ID_Materia_Prima = database.Column(database.Integer(8), primary_key=True, nullable=False, unique=True)
    ID_Lote = database.Column(database.Integer(8), database.ForeignKey('Estoque.ID_Lote'), nullable=False)
    Nome_Materia_Prima = database.Column(database.String(50), nullable=False, unique=True)
    Qtde_Estoque = database.Column(database.Integer(4), nullable=False)
    Validade_Materia_Prima = database.Column(database.Date, nullable=False)
    
class Produto(database.Model):
    ID_Produto = database.Column(database.Integer(8), primary_key=True, nullable=False, unique=True)
    ID_Lote = database.Column(database.Integer(8), database.ForeignKey('Estoque.ID_Lote'), nullable=False)
    Preco_Produto = database.Column(database.Float(6.2), nullable=False)
    
class Producao(database.Model):
    ID_Producao = database.Column(database.Integer(8), primary_key=True, nullable=False, unique=True)
    ID_Produto = database.Column(database.Integer(8), database.ForeignKey('Produto.ID_Produto'), nullable=False)
    ID_Materia_Prima = database.Column(database.Integer(8), database.ForeignKey('MateriaPrima.ID_Materia_Prima'), nullable=False)
    Dt_Fabricacao = database.Column(database.Date, nullable=False)
    Qtd_Produzida = database.Column(database.Integer(4), nullable=False)
    
class Pedido(database.Model):
    ID_Pedido = database.Column(database.Integer(8), primary_key=True, nullable=False, unique=True)
    ID_Mesa = database.Column(database.Integer(8), database.ForeignKey('Mesa.ID_Mesa'), nullable=False)
    ID_Produto = database.Column(database.Integer(8), database.ForeignKey('Produto.ID_Produto'), nullable=False)
    ID_Cliente = database.Column(database.Integer(8), database.ForeignKey('Cliente.ID_Cliente'), nullable=False)
    ID_Funcionario = database.Column(database.Integer(8), database.ForeignKey('Funcionario.ID_Funcionario'), nullable=False)
    Dt_Pedido = database.Column(database.Date, nullable=False)
    Forma_Pagamento = database.Column(database.String(30), nullable=False)
    Desconto_Produto = database.Column(database.Float(6.2), nullable=False)
    
class PedidoProduto(database.Model):
    ID_Produto = database.Column(database.Integer(8), database.ForeignKey('Produto.ID_Produto'), primary_key=True, nullable=False, unique=True)
    ID_Pedido = database.Column(database.Integer(8), database.ForeignKey('Pedido.ID_Pedido'), primary_key=True)
    Qtde_Produto = database.Column(database.Integer(4), nullable=False)
    
class MateriaPrimaProduto(database.Model):
    ID_Produto = database.Column(database.Integer(8), database.ForeignKey('Produto.ID_Produto'), primary_key=True, nullable=False, unique=True)
    ID_Materia_Prima = database.Column(database.Integer(8), database.ForeignKey('MateriaPrima.ID_Materia_Prima'), primary_key=True)
    
class MateriaPrimaFornecedor(database.Model):
    ID_Materia_Prima = database.Column(database.Integer(8), database.ForeignKey('MateriaPrima.ID_Materia_Prima'), primary_key=True, nullable=False, unique=True)
    ID_Fornecedor = database.Column(database.Integer(8), database.ForeignKey('Fornecedor.ID_Fornecedor'), primary_key=True)
