class MultimeiosRouter:
    """Encaminha cada app para um dos três bancos físicos."""

    app_para_banco = {
        "alunos": "usuarios",
        "gestao": "admin_db",
        "acervo": "default",
    }

    def db_for_read(self, model, **hints):
        return self.app_para_banco.get(model._meta.app_label)

    def db_for_write(self, model, **hints):
        return self.app_para_banco.get(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        banco_1 = self.app_para_banco.get(obj1._meta.app_label)
        banco_2 = self.app_para_banco.get(obj2._meta.app_label)
        if banco_1 and banco_2:
            return banco_1 == banco_2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        banco_alvo = self.app_para_banco.get(app_label)
        if banco_alvo:
            return db == banco_alvo
        return False
