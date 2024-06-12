from apibdusers import app, database
import requests
from flask import request, jsonify
from flask_login import login_user, login_required, current_user
from apibdusers.models import Usuario, Funcionario, Cliente, Fornecedor, Mesa, Estoque, MateriaPrima,Pedido, Produto, PedidoProduto, Producao, MateriaPrimaProduto, MateriaPrimaFornecedor,  load_usuario




@app.route('/api/login', methods=['POST'])
def loguser():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'message': 'Falta o email ou a senha'}), 400

    user = Usuario.query.filter_by(email=email).first()

    if not user or not user.check_password(senha):
        return jsonify({'message': 'Credenciais inválidas'}), 401

    print(user.id)
    return load_usuario(user.id)
    


#---------------------- FUNCOES USUARIO ---------------------------------

#---------------------criacao de conta do usuario -----------------------
@app.route('/api/create_user', methods=['POST'])
def create_user():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    admin = data.get('admin')

    if not nome or not email or not senha:
        return jsonify({'message': 'Falta nome, email ou senha'}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'message': 'Email já cadastrado'}), 400

    user = Usuario(nome=nome, email=email,senha=senha, pagou=False, admin=admin, idontaatual=1)
    user.set_password(senha)
    database.session.add(user)
    database.session.commit()


    return jsonify({'message': 'Usuário criado com sucesso'})





#---------------------- FUNCOES do cliente ---------------------------------

@app.route('/api/create_cliente', methods=['POST'])
def create_cliente():
    data = request.json
    id_endereco = data.get('id_endereco')
    nr_cliente = data.get('nr_cliente')
    complemento_cliente = data.get('complemento_cliente')
    nome_cliente = data.get('nome_cliente')
    cpf_cliente = data.get('cpf_cliente')
    telefone_cliente = data.get('telefone_cliente')
    email_cliente = data.get('email_cliente')
    dt_nasc_cliente = data.get('dt_nasc_cliente')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_endereco or not nr_cliente or not complemento_cliente or not nome_cliente or not cpf_cliente or not telefone_cliente or not email_cliente or not dt_nasc_cliente:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Verifica se o cliente já existe pelo CPF ou email
    if Cliente.query.filter_by(CPF_Cliente=cpf_cliente).first() or Cliente.query.filter_by(Email_Cliente=email_cliente).first():
        return jsonify({'message': 'Cliente já cadastrado'}), 400

    # Cria o novo cliente
    cliente = Cliente(
        ID_Endereco=id_endereco,
        NR_Cliente=nr_cliente,
        Complemento_Cliente=complemento_cliente,
        Nome_Cliente=nome_cliente,
        CPF_Cliente=cpf_cliente,
        Telefone_Cliente=telefone_cliente,
        Email_Cliente=email_cliente,
        Dt_Nasc_Cliente=dt_nasc_cliente
    )

    # Adiciona o cliente ao banco de dados
    database.session.add(cliente)
    database.session.commit()

    return jsonify({'message': 'Cliente criado com sucesso'})


# Rota para obter todos os clientes
@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.serialize() for cliente in clientes])

# Rota para obter um cliente por ID
@app.route('/api/cliente/<int:cliente_id>', methods=['GET'])
def get_cliente_by_id(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if cliente:
        return jsonify(cliente.serialize())
    else:
        return jsonify({'message': 'Cliente não encontrado'}), 404

# Rota para excluir um cliente por ID
@app.route('/api/cliente/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if cliente:
        database.session.delete(cliente)
        database.session.commit()
        return jsonify({'message': 'Cliente excluído com sucesso'})
    else:
        return jsonify({'message': 'Cliente não encontrado'}), 404






 #---------------------- FUNCOES FUNCIONARIO ---------------------------------

# Rota para criar um novo funcionário
@app.route('/api/create_funcionario', methods=['POST'])
def create_funcionario():
    data = request.json
    id_endereco = data.get('id_endereco')
    nr_funcionario = data.get('nr_funcionario')
    complemento_funcionario = data.get('complemento_funcionario')
    nome_funcionario = data.get('nome_funcionario')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_endereco or not nr_funcionario or not complemento_funcionario or not nome_funcionario:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Cria o novo funcionário
    funcionario = Funcionario(
        ID_Endereco=id_endereco,
        NR_Funcionario=nr_funcionario,
        Complemento_Funcionario=complemento_funcionario,
        Nome_Funcionario=nome_funcionario
    )

    # Adiciona o funcionário ao banco de dados
    database.session.add(funcionario)
    database.session.commit()

    return jsonify({'message': 'Funcionário criado com sucesso'})

# Rota para obter todos os funcionários
@app.route('/api/funcionarios', methods=['GET'])
def get_funcionarios():
    funcionarios = Funcionario.query.all()
    return jsonify([funcionario.serialize() for funcionario in funcionarios])

# Rota para obter um funcionário por ID
@app.route('/api/funcionario/<int:funcionario_id>', methods=['GET'])
def get_funcionario_by_id(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    if funcionario:
        return jsonify(funcionario.serialize())
    else:
        return jsonify({'message': 'Funcionário não encontrado'}), 404

# Rota para excluir um funcionário por ID
@app.route('/api/funcionario/<int:funcionario_id>', methods=['DELETE'])
def delete_funcionario(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    if funcionario:
        database.session.delete(funcionario)
        database.session.commit()
        return jsonify({'message': 'Funcionário excluído com sucesso'})
    else:
        return jsonify({'message': 'Funcionário não encontrado'}), 404





#---------------------- FUNCOES Fornecedor ---------------------------------
# Rota para criar um novo fornecedor
@app.route('/api/create_fornecedor', methods=['POST'])
def create_fornecedor():
    data = request.json
    id_endereco = data.get('id_endereco')
    nr_fornecedor = data.get('nr_fornecedor')
    complemento_fornecedor = data.get('complemento_fornecedor')
    nome_fornecedor = data.get('nome_fornecedor')
    cnpj_fornecedor = data.get('cnpj_fornecedor')
    telefone_fornecedor = data.get('telefone_fornecedor')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_endereco or not nr_fornecedor or not complemento_fornecedor or not nome_fornecedor or not cnpj_fornecedor or not telefone_fornecedor:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Verifica se o fornecedor já existe pelo CNPJ ou nome
    if Fornecedor.query.filter_by(CNPJ_Fornecedor=cnpj_fornecedor).first() or Fornecedor.query.filter_by(Nome_Fornecedor=nome_fornecedor).first():
        return jsonify({'message': 'Fornecedor já cadastrado'}), 400

    # Cria o novo fornecedor
    fornecedor = Fornecedor(
        ID_Endereco=id_endereco,
        NR_Fornecedor=nr_fornecedor,
        Complemento_Fornecedor=complemento_fornecedor,
        Nome_Fornecedor=nome_fornecedor,
        CNPJ_Fornecedor=cnpj_fornecedor,
        Telefone_Fornecedor=telefone_fornecedor
    )

    # Adiciona o fornecedor ao banco de dados
    database.session.add(fornecedor)
    database.session.commit()

    return jsonify({'message': 'Fornecedor criado com sucesso'})

# Rota para obter todos os fornecedores
@app.route('/api/fornecedores', methods=['GET'])
def get_fornecedores():
    fornecedores = Fornecedor.query.all()
    return jsonify([fornecedor.serialize() for fornecedor in fornecedores])

# Rota para obter um fornecedor por ID
@app.route('/api/fornecedor/<int:fornecedor_id>', methods=['GET'])
def get_fornecedor_by_id(fornecedor_id):
    fornecedor = Fornecedor.query.get(fornecedor_id)
    if fornecedor:
        return jsonify(fornecedor.serialize())
    else:
        return jsonify({'message': 'Fornecedor não encontrado'}), 404

# Rota para excluir um fornecedor por ID
@app.route('/api/fornecedor/<int:fornecedor_id>', methods=['DELETE'])
def delete_fornecedor(fornecedor_id):
    fornecedor = Fornecedor.query.get(fornecedor_id)
    if fornecedor:
        database.session.delete(fornecedor)
        database.session.commit()
        return jsonify({'message': 'Fornecedor excluído com sucesso'})
    else:
        return jsonify({'message': 'Fornecedor não encontrado'}), 404



#---------------------- FUNCOES mesa ---------------------------------
# Rota para criar uma nova mesa
@app.route('/api/create_mesa', methods=['POST'])
def create_mesa():
    data = request.json
    capacidade_mesa = data.get('capacidade_mesa')
    disponibilidade_mesa = data.get('disponibilidade_mesa')

    # Verifica se todos os campos necessários foram fornecidos
    if not capacidade_mesa or not disponibilidade_mesa:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Cria a nova mesa
    mesa = Mesa(
        Capacidade_Mesa=capacidade_mesa,
        Disponibilidade_Mesa=disponibilidade_mesa
    )

    # Adiciona a mesa ao banco de dados
    database.session.add(mesa)
    database.session.commit()

    return jsonify({'message': 'Mesa criada com sucesso'})

# Rota para obter todas as mesas
@app.route('/api/mesas', methods=['GET'])
def get_mesas():
    mesas = Mesa.query.all()
    return jsonify([mesa.serialize() for mesa in mesas])

# Rota para obter uma mesa por ID
@app.route('/api/mesa/<int:mesa_id>', methods=['GET'])
def get_mesa_by_id(mesa_id):
    mesa = Mesa.query.get(mesa_id)
    if mesa:
        return jsonify(mesa.serialize())
    else:
        return jsonify({'message': 'Mesa não encontrada'}), 404

# Rota para excluir uma mesa por ID
@app.route('/api/mesa/<int:mesa_id>', methods=['DELETE'])
def delete_mesa(mesa_id):
    mesa = Mesa.query.get(mesa_id)
    if mesa:
        database.session.delete(mesa)
        database.session.commit()
        return jsonify({'message': 'Mesa excluída com sucesso'})
    else:
        return jsonify({'message': 'Mesa não encontrada'}), 404


# Rota para mudar a disponibilidade de uma mesa
@app.route('/api/mesa/<int:mesa_id>/disponibilidade', methods=['PUT'])
def change_mesa_disponibilidade(mesa_id):
    data = request.json
    disponibilidade = data.get('disponibilidade')

    # Verifica se a disponibilidade foi fornecida
    if disponibilidade is None:
        return jsonify({'message': 'Falta informar a disponibilidade'}), 400

    # Verifica se a mesa existe
    mesa = Mesa.query.get(mesa_id)
    if not mesa:
        return jsonify({'message': 'Mesa não encontrada'}), 404

    # Altera a disponibilidade da mesa
    mesa.Disponibilidade_Mesa = disponibilidade
    database.session.commit()

    return jsonify({'message': f'Disponibilidade da mesa {mesa_id} alterada para {disponibilidade}'})



#---------------------- FUNCOES etoque ---------------------------------
# Rota para criar um novo lote no estoque
@app.route('/api/create_estoque', methods=['POST'])
def create_estoque():
    data = request.json
    id_fornecedor = data.get('id_fornecedor')
    dt_fabricacao = data.get('dt_fabricacao')
    validade_lote = data.get('validade_lote')
    qtde_estoque = data.get('qtde_estoque')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_fornecedor or not dt_fabricacao or not validade_lote or not qtde_estoque:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Cria o novo lote no estoque
    estoque = Estoque(
        ID_Fornecedor=id_fornecedor,
        Dt_Fabricacao=dt_fabricacao,
        Validade_Lote=validade_lote,
        Qtde_Estoque=qtde_estoque
    )

    # Adiciona o lote ao banco de dados
    database.session.add(estoque)
    database.session.commit()

    return jsonify({'message': 'Lote no estoque criado com sucesso'})

# Rota para obter todos os lotes no estoque
@app.route('/api/estoques', methods=['GET'])
def get_estoques():
    estoques = Estoque.query.all()
    return jsonify([estoque.serialize() for estoque in estoques])

# Rota para obter um lote no estoque por ID
@app.route('/api/estoque/<int:estoque_id>', methods=['GET'])
def get_estoque_by_id(estoque_id):
    estoque = Estoque.query.get(estoque_id)
    if estoque:
        return jsonify(estoque.serialize())
    else:
        return jsonify({'message': 'Lote no estoque não encontrado'}), 404

# Rota para excluir um lote no estoque por ID
@app.route('/api/estoque/<int:estoque_id>', methods=['DELETE'])
def delete_estoque(estoque_id):
    estoque = Estoque.query.get(estoque_id)
    if estoque:
        database.session.delete(estoque)
        database.session.commit()
        return jsonify({'message': 'Lote no estoque excluído com sucesso'})
    else:
        return jsonify({'message': 'Lote no estoque não encontrado'}), 404
    



#---------------------- FUNCOES materia prima ---------------------------------

# Rota para criar uma nova matéria-prima
@app.route('/api/create_materia_prima', methods=['POST'])
def create_materia_prima():
    data = request.json
    id_lote = data.get('id_lote')
    nome_materia_prima = data.get('nome_materia_prima')
    qtde_estoque = data.get('qtde_estoque')
    validade_materia_prima = data.get('validade_materia_prima')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_lote or not nome_materia_prima or not qtde_estoque or not validade_materia_prima:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Verifica se a matéria-prima já existe pelo nome
    if MateriaPrima.query.filter_by(Nome_Materia_Prima=nome_materia_prima).first():
        return jsonify({'message': 'Matéria-prima já cadastrada'}), 400

    # Cria a nova matéria-prima
    materia_prima = MateriaPrima(
        ID_Lote=id_lote,
        Nome_Materia_Prima=nome_materia_prima,
        Qtde_Estoque=qtde_estoque,
        Validade_Materia_Prima=validade_materia_prima
    )

    # Adiciona a matéria-prima ao banco de dados
    database.session.add(materia_prima)
    database.session.commit()

    return jsonify({'message': 'Matéria-prima criada com sucesso'})

# Rota para obter todas as matérias-primas
@app.route('/api/materias_primas', methods=['GET'])
def get_materias_primas():
    materias_primas = MateriaPrima.query.all()
    return jsonify([materia_prima.serialize() for materia_prima in materias_primas])

# Rota para obter uma matéria-prima por ID
@app.route('/api/materia_prima/<int:materia_prima_id>', methods=['GET'])
def get_materia_prima_by_id(materia_prima_id):
    materia_prima = MateriaPrima.query.get(materia_prima_id)
    if materia_prima:
        return jsonify(materia_prima.serialize())
    else:
        return jsonify({'message': 'Matéria-prima não encontrada'}), 404

# Rota para excluir uma matéria-prima por ID
@app.route('/api/materia_prima/<int:materia_prima_id>', methods=['DELETE'])
def delete_materia_prima(materia_prima_id):
    materia_prima = MateriaPrima.query.get(materia_prima_id)
    if materia_prima:
        database.session.delete(materia_prima)
        database.session.commit()
        return jsonify({'message': 'Matéria-prima excluída com sucesso'})
    else:
        return jsonify({'message': 'Matéria-prima não encontrada'}), 404







#---------------------- FUNCOES prdouto ---------------------------------
# Rota para criar um novo produto
@app.route('/api/create_produto', methods=['POST'])
def create_produto():
    data = request.json
    id_lote = data.get('id_lote')
    preco_produto = data.get('preco_produto')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_lote or not preco_produto:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Cria o novo produto
    produto = Produto(
        ID_Lote=id_lote,
        Preco_Produto=preco_produto
    )

    # Adiciona o produto ao banco de dados
    database.session.add(produto)
    database.session.commit()

    return jsonify({'message': 'Produto criado com sucesso'})

# Rota para obter todos os produtos
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([produto.serialize() for produto in produtos])

# Rota para obter um produto por ID
@app.route('/api/produto/<int:produto_id>', methods=['GET'])
def get_produto_by_id(produto_id):
    produto = Produto.query.get(produto_id)
    if produto:
        return jsonify(produto.serialize())
    else:
        return jsonify({'message': 'Produto não encontrado'}), 404

# Rota para excluir um produto por ID
@app.route('/api/produto/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    produto = Produto.query.get(produto_id)
    if produto:
        database.session.delete(produto)
        database.session.commit()
        return jsonify({'message': 'Produto excluído com sucesso'})
    else:
        return jsonify({'message': 'Produto não encontrado'}), 404




#---------------------- FUNCOES producao ---------------------------------

# Rota para criar uma nova produção
@app.route('/api/create_producao', methods=['POST'])
def create_producao():
    data = request.json
    id_produto = data.get('id_produto')
    id_materia_prima = data.get('id_materia_prima')
    dt_fabricacao = data.get('dt_fabricacao')
    qtd_produzida = data.get('qtd_produzida')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_produto or not id_materia_prima or not dt_fabricacao or not qtd_produzida:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Cria a nova produção
    producao = Producao(
        ID_Produto=id_produto,
        ID_Materia_Prima=id_materia_prima,
        Dt_Fabricacao=dt_fabricacao,
        Qtd_Produzida=qtd_produzida
    )

    # Adiciona a produção ao banco de dados
    database.session.add(producao)
    database.session.commit()

    return jsonify({'message': 'Produção criada com sucesso'})

# Rota para obter todas as produções
@app.route('/api/producoes', methods=['GET'])
def get_producoes():
    producoes = Producao.query.all()
    return jsonify([producao.serialize() for producao in producoes])

# Rota para obter uma produção por ID
@app.route('/api/producao/<int:producao_id>', methods=['GET'])
def get_producao_by_id(producao_id):
    producao = Producao.query.get(producao_id)
    if producao:
        return jsonify(producao.serialize())
    else:
        return jsonify({'message': 'Produção não encontrada'}), 404

# Rota para excluir uma produção por ID
@app.route('/api/producao/<int:producao_id>', methods=['DELETE'])
def delete_producao(producao_id):
    producao = Producao.query.get(producao_id)
    if producao:
        database.session.delete(producao)
        database.session.commit()
        return jsonify({'message': 'Produção excluída com sucesso'})
    else:
        return jsonify({'message': 'Produção não encontrada'}), 404



#---------------------- FUNCOES pedido ---------------------------------

# Rota para criar um novo pedido
@app.route('/api/create_pedido', methods=['POST'])
def create_pedido():
    data = request.json
    id_mesa = data.get('id_mesa')
    id_produto = data.get('id_produto')
    id_cliente = data.get('id_cliente')
    id_funcionario = data.get('id_funcionario')
    dt_pedido = data.get('dt_pedido')
    forma_pagamento = data.get('forma_pagamento')
    desconto_produto = data.get('desconto_produto')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_mesa or not id_produto or not id_cliente or not id_funcionario or not dt_pedido or not forma_pagamento or not desconto_produto:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Cria o novo pedido
    pedido = Pedido(
        ID_Mesa=id_mesa,
        ID_Produto=id_produto,
        ID_Cliente=id_cliente,
        ID_Funcionario=id_funcionario,
        Dt_Pedido=dt_pedido,
        Forma_Pagamento=forma_pagamento,
        Desconto_Produto=desconto_produto
    )

    # Adiciona o pedido ao banco de dados
    database.session.add(pedido)
    database.session.commit()

    return jsonify({'message': 'Pedido criado com sucesso'})

# Rota para obter todos os pedidos
@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([pedido.serialize() for pedido in pedidos])

# Rota para obter um pedido por ID
@app.route('/api/pedido/<int:pedido_id>', methods=['GET'])
def get_pedido_by_id(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    if pedido:
        return jsonify(pedido.serialize())
    else:
        return jsonify({'message': 'Pedido não encontrado'}), 404

# Rota para excluir um pedido por ID
@app.route('/api/pedido/<int:pedido_id>', methods=['DELETE'])
def delete_pedido(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    if pedido:
        database.session.delete(pedido)
        database.session.commit()
        return jsonify({'message': 'Pedido excluído com sucesso'})
    else:
        return jsonify({'message': 'Pedido não encontrado'}), 404

#---------------------- FUNCOES PedidoProduto ---------------------------------
# Rota para criar uma nova associação entre pedido e produto
@app.route('/api/create_pedido_produto', methods=['POST'])
def create_pedido_produto():
    data = request.json
    id_produto = data.get('id_produto')
    id_pedido = data.get('id_pedido')
    qtde_produto = data.get('qtde_produto')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_produto or not id_pedido or not qtde_produto:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Cria a nova associação entre pedido e produto
    pedido_produto = PedidoProduto(
        ID_Produto=id_produto,
        ID_Pedido=id_pedido,
        Qtde_Produto=qtde_produto
    )

    # Adiciona a associação ao banco de dados
    database.session.add(pedido_produto)
    database.session.commit()

    return jsonify({'message': 'Associação entre pedido e produto criada com sucesso'})

# Rota para obter todas as associações entre pedidos e produtos
@app.route('/api/pedido_produtos', methods=['GET'])
def get_pedido_produtos():
    pedido_produtos = PedidoProduto.query.all()
    return jsonify([pedido_produto.serialize() for pedido_produto in pedido_produtos])

# Rota para obter uma associação entre pedido e produto por ID do pedido
@app.route('/api/pedido_produto/<int:pedido_id>', methods=['GET'])
def get_pedido_produto_by_pedido_id(pedido_id):
    pedido_produtos = PedidoProduto.query.filter_by(ID_Pedido=pedido_id).all()
    if pedido_produtos:
        return jsonify([pedido_produto.serialize() for pedido_produto in pedido_produtos])
    else:
        return jsonify({'message': 'Associação entre pedido e produto não encontrada'}), 404

# Rota para excluir uma associação entre pedido e produto por ID do produto e ID do pedido
@app.route('/api/pedido_produto/<int:produto_id>/<int:pedido_id>', methods=['DELETE'])
def delete_pedido_produto(produto_id, pedido_id):
    pedido_produto = PedidoProduto.query.filter_by(ID_Produto=produto_id, ID_Pedido=pedido_id).first()
    if pedido_produto:
        database.session.delete(pedido_produto)
        database.session.commit()
        return jsonify({'message': 'Associação entre pedido e produto excluída com sucesso'})
    else:
        return jsonify({'message': 'Associação entre pedido e produto não encontrada'}), 404


#---------------------- FUNCOES MateriaPrimaProduto ---------------------------------

# Rota para criar uma nova associação entre matéria-prima e produto
@app.route('/api/create_materia_prima_produto', methods=['POST'])
def create_materia_prima_produto():
    data = request.json
    id_produto = data.get('id_produto')
    id_materia_prima = data.get('id_materia_prima')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_produto or not id_materia_prima:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Cria a nova associação entre matéria-prima e produto
    materia_prima_produto = MateriaPrimaProduto(
        ID_Produto=id_produto,
        ID_Materia_Prima=id_materia_prima
    )

    # Adiciona a associação ao banco de dados
    database.session.add(materia_prima_produto)
    database.session.commit()

    return jsonify({'message': 'Associação entre matéria-prima e produto criada com sucesso'})

# Rota para obter todas as associações entre matérias-primas e produtos
@app.route('/api/materia_prima_produtos', methods=['GET'])
def get_materia_prima_produtos():
    materia_prima_produtos = MateriaPrimaProduto.query.all()
    return jsonify([materia_prima_produto.serialize() for materia_prima_produto in materia_prima_produtos])

# Rota para obter uma associação entre matéria-prima e produto por ID do produto
@app.route('/api/materia_prima_produto/<int:produto_id>', methods=['GET'])
def get_materia_prima_produto_by_produto_id(produto_id):
    materia_prima_produtos = MateriaPrimaProduto.query.filter_by(ID_Produto=produto_id).all()
    if materia_prima_produtos:
        return jsonify([materia_prima_produto.serialize() for materia_prima_produto in materia_prima_produtos])
    else:
        return jsonify({'message': 'Associação entre matéria-prima e produto não encontrada'}), 404

# Rota para excluir uma associação entre matéria-prima e produto por ID do produto e ID da matéria-prima
@app.route('/api/materia_prima_produto/<int:produto_id>/<int:materia_prima_id>', methods=['DELETE'])
def delete_materia_prima_produto(produto_id, materia_prima_id):
    materia_prima_produto = MateriaPrimaProduto.query.filter_by(ID_Produto=produto_id, ID_Materia_Prima=materia_prima_id).first()
    if materia_prima_produto:
        database.session.delete(materia_prima_produto)
        database.session.commit()
        return jsonify({'message': 'Associação entre matéria-prima e produto excluída com sucesso'})
    else:
        return jsonify({'message': 'Associação entre matéria-prima e produto não encontrada'}), 404




#---------------------- FUNCOES MateriaPrimaFornecedor ---------------------------------

# Rota para criar uma nova associação entre matéria-prima e fornecedor
@app.route('/api/create_materia_prima_fornecedor', methods=['POST'])
def create_materia_prima_fornecedor():
    data = request.json
    id_materia_prima = data.get('id_materia_prima')
    id_fornecedor = data.get('id_fornecedor')

    # Verifica se todos os campos necessários foram fornecidos
    if not id_materia_prima or not id_fornecedor:
        return jsonify({'message': 'Falta algum campo obrigatório'}), 400

    # Cria a nova associação entre matéria-prima e fornecedor
    materia_prima_fornecedor = MateriaPrimaFornecedor(
        ID_Materia_Prima=id_materia_prima,
        ID_Fornecedor=id_fornecedor
    )

    # Adiciona a associação ao banco de dados
    database.session.add(materia_prima_fornecedor)
    database.session.commit()

    return jsonify({'message': 'Associação entre matéria-prima e fornecedor criada com sucesso'})

# Rota para obter todas as associações entre matérias-primas e fornecedores
@app.route('/api/materia_prima_fornecedores', methods=['GET'])
def get_materia_prima_fornecedores():
    materia_prima_fornecedores = MateriaPrimaFornecedor.query.all()
    return jsonify([materia_prima_fornecedor.serialize() for materia_prima_fornecedor in materia_prima_fornecedores])

# Rota para obter uma associação entre matéria-prima e fornecedor por ID da matéria-prima
@app.route('/api/materia_prima_fornecedor/<int:materia_prima_id>', methods=['GET'])
def get_materia_prima_fornecedor_by_materia_prima_id(materia_prima_id):
    materia_prima_fornecedores = MateriaPrimaFornecedor.query.filter_by(ID_Materia_Prima=materia_prima_id).all()
    if materia_prima_fornecedores:
        return jsonify([materia_prima_fornecedor.serialize() for materia_prima_fornecedor in materia_prima_fornecedores])
    else:
        return jsonify({'message': 'Associação entre matéria-prima e fornecedor não encontrada'}), 404

# Rota para excluir uma associação entre matéria-prima e fornecedor por ID da matéria-prima e ID do fornecedor
@app.route('/api/materia_prima_fornecedor/<int:materia_prima_id>/<int:fornecedor_id>', methods=['DELETE'])
def delete_materia_prima_fornecedor(materia_prima_id, fornecedor_id):
    materia_prima_fornecedor = MateriaPrimaFornecedor.query.filter_by(ID_Materia_Prima=materia_prima_id, ID_Fornecedor=fornecedor_id).first()
    if materia_prima_fornecedor:
        database.session.delete(materia_prima_fornecedor)
        database.session.commit()
        return jsonify({'message': 'Associação entre matéria-prima e fornecedor excluída com sucesso'})
    else:
        return jsonify({'message': 'Associação entre matéria-prima e fornecedor não encontrada'}), 404
