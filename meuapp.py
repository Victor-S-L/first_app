from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.tooltip import MDTooltip
from datetime import date
import sqlite3 as lite
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp


class JanelaGerenciadora(ScreenManager):

    def voltar(self):
        self.current = "janelaprincipal"
        self.transition.direction = 'right'


class JanelaPrincipal(Screen):
    pass


class Menu(Screen):
    pass


class Janela1(Screen):  # Adicionar Saldo

    def adicionar_receita(self):
        self.dialog = MDDialog(title='ERROR', text='Erro encontrado, repita a operação.',
                               buttons=[MDFlatButton(text='OK',
                                                     on_release=self.liberar)])
        try:
            categoria = 'Receita'
            valor = float(self.ids.caixa_texto.text)
            dia = str(date.today())
            obs = str(self.ids.caixa_texto2.text).title()
            if self.ids.cb_din.active:
                tipo1 = 'Dinheiro'

            elif self.ids.cb_transf.active:
                tipo1 = 'Transferência'

            else:
                tipo1 = 'N/C'

            if self.ids.cb_normal.active:
                tipo2 = 'Normal'

            elif self.ids.cb_extra.active:
                tipo2 = 'Extra'

            else:
                tipo2 = 'N/C'

            lista = [categoria, valor, tipo1, tipo2, dia, obs]

            self.ids.resposta.text = str(lista)

            con = lite.connect('banco.db')

            with con:
                cur = con.cursor()
                query = "INSERT INTO operacoes (categoria, valor, tipo1, tipo2, dia, obs) VALUES (?, ?, ?, ?, ?, ?)"
                cur.execute(query, lista)

        except ValueError:
            self.dialog.open()

    def liberar(self, obj):
        self.dialog.dismiss()

    def limpar(self):

        self.ids.caixa_texto.text = ''
        self.ids.caixa_texto2.text = ''
        #self.ids.resposta.text = ''
        self.ids.cb_transf.active = False
        self.ids.cb_din.active = False
        self.ids.cb_normal.active = False
        self.ids.cb_extra.active = False

    #def calcular(self):
    #    self.dialog = MDDialog(title='ERROR', text='Erro encontrado, repita a operação.',
    #                           buttons=[MDFlatButton(text='OK',
    #                                                 on_release=self.liberar)])
    #    try:
    #        v1 = float(self.ids.caixa_texto.text)
    #        v2 = v1 / 3.6
    #        self.ids.resposta.text = '{:0.2f}'.format(v2) + 'm/s'
    #
    #    except ValueError:
    #        self.dialog.open()
    #
    #def liberar(self, obj):
    #    self.dialog.dismiss()


class Janela2(Screen):  # Registrar Despesa

    def adicionar_despesa(self):
        self.dialog = MDDialog(title='ERROR', text='Erro encontrado, repita a operação.',
                               buttons=[MDFlatButton(text='OK',
                                                     on_release=self.liberar)])
        try:
            categoria = 'Despesa'
            numero = float(self.ids.caixa_texto.text)
            valor = numero * -1
            dia = str(date.today())
            obs = str(self.ids.caixa_texto2.text).title()
            if self.ids.cb_din.active:
                tipo1 = 'Dinheiro'

            elif self.ids.cb_cartao.active:
                tipo1 = 'Cartão'

            else:
                tipo1 = 'N/C'

            if self.ids.cb_fixa.active:
                tipo2 = 'Fixa'

            elif self.ids.cb_variavel.active:
                tipo2 = 'Variável'

            else:
                tipo2 = 'N/C'

            lista = [categoria, valor, tipo1, tipo2, dia, obs]

            self.ids.resposta.text = str(lista)

            con = lite.connect('banco.db')

            with con:
                cur = con.cursor()
                query = "INSERT INTO operacoes (categoria, valor, tipo1, tipo2, dia, obs) VALUES (?, ?, ?, ?, ?, ?)"
                cur.execute(query, lista)

        except ValueError:
            self.dialog.open()

    def liberar(self, obj):
        self.dialog.dismiss()

    def limpar(self):

        self.ids.caixa_texto.text = ''
        self.ids.caixa_texto2.text = ''
        #self.ids.resposta.text = ''
        self.ids.cb_cartao.active = False
        self.ids.cb_din.active = False
        self.ids.cb_fixa.active = False
        self.ids.cb_variavel.active = False

class Janela5(Screen): #tela de visualização de registros

    def extrato(self):

        con = lite.connect('banco.db')

        with con:
            cur = con.cursor()
            query = "SELECT * FROM operacoes"
            cur.execute(query)
            informacao = cur.fetchall()
        con.close()

        self.data_tables = MDDataTable(
            use_pagination=True,
            column_data=[
                ("Id", dp(30)),
                ("Categoria", dp(30)),
                ("Valor", dp(60)),
                ("Tipo 1", dp(30)),
                ("Tipo 2", dp(30)),
                ("Data", dp(30)),
                ("Observação", dp(30)),
            ],
            row_data=informacao,
        )
        box = self.ids.box
        box.add_widget(self.data_tables)
        return box

class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass

class MeuApp(MDApp):

    # criando a conexão

    con = lite.connect('banco.db')

    # criando tabela


    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE if not exists operacoes (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    " categoria TEXT, valor FLOAT, tipo1 TEXT, tipo2 TEXT, dia DATE, obs TEXT)")


    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Green'
        self.title = 'Gerenciador Financeiro'
        return Builder.load_file('menu.kv')

    def fechar(self):
        self.stop()





MeuApp().run()
