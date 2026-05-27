class Usuario:
    def __init__(self, uid, nome, email, tipo):
        self.uid = uid
        self.nome = nome
        self.email = email
        self.tipo = tipo


class Horario:
    def __init__(self, id, data, hora, vagas):
        self.id = id
        self.data = data
        self.hora = hora
        self.vagas = vagas


class Reserva:
    def __init__(self, id, aluno_nome, horario_id):
        self.id = id
        self.aluno_nome = aluno_nome
        self.horario_id = horario_id