import sys, os
import datetime as dt
import locale, sqlite3

locale.setlocale(locale.LC_ALL, 'pt_BR')

class PontoBD:
    cam = 'src\\db'
    list_table =["""
    create table if not exists ponto(
        id_ponto integer primary key autoincrement
        ,data date
        ,hora text
        ,tipo text
        ,forma text
    );
    """,
    """
    create table if not exists time_worked(
        data date
        ,horas texto
    );
    """]

    def __init__(self):
        PontoBD.criaPastaBD()
        self.conn = sqlite3.connect(PontoBD.cam+'\\dados.db')
        self.conn.isolation_level = None
        self.batida = dt.datetime.now()
        
        for table in PontoBD.list_table:
            self.executeCommand(table) 
        
    @classmethod
    def criaPastaBD(cls):
        if not os.path.isdir(cls.cam):
            os.mkdir(cls.cam)
    
    def executeCommand(self, query):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
        except self.conn.Error as error:
            print(error)
            self.conn.rollback()
    def getQuery(self, query):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
        except self.conn.Error as error:
            raise Exception(error)
        results = cursor.fetchall()
        
        colunas = [col[0] for col in cursor.description]
        result_dict = {}

        for a, col in enumerate(colunas):
            result_dict[col] = []
            [result_dict[col].append(reg[a]) for reg in results]
        
        return result_dict

    def ponto(self):
        ponto = {}
        ponto['data'] = self.batida.date()
        ponto['hora'] = self.batida.strftime('%H:%M')

        if self.batida.hour < 12:
            ponto['tipo'] = 'entrada'
            validacao = f"select data from ponto where tipo = '{ponto['tipo']}' and data = '{ponto['data']}'"
            test = self.getQuery(validacao)
            if len(test['data']) != 0:
                return -1
        else:
            ponto['tipo'] = 'saida'
            validacao = f"select data from ponto where tipo = ''{ponto['tipo']}' ' and data = '{ponto['data']}'"
            test = self.getQuery(validacao)
            if len(test['data']) != 0:
                return -1
        insert = """
        insert into ponto(data, hora, tipo, forma) values ('{data}', '{hora}', '{tipo}', 'sistema')
        """.format(**ponto)

        self.executeCommand(insert)
        return 0
    
    def horas(self):
        valid_date = """
        select distinct data from ponto p
        left join time_worked tw
        on p.data = tw.data
        where
            tw.data is null
        """
        pontos = self.executeCommand(valid_date)

        if len(pontos['data']) == 0:
            return -1
        
        for data in pontos['data']:
            bd_query = f"select data, hora, tipo from ponto where dia = '{data}' order by tipo"
            bd = self.getQuery(bd_query)

            if ('saida' in bd['tipo']) and ('entrada' in bd['tipo']):
                time_worked = {}
                time_worked['data'] = bd['data'][0]

                hora_1 = bd['data'][0] + " "+ bd['hora'][0]
                d1 = dt.datetime.strptime(hora_1, '%Y-%m-%d %H:%M')

                hora_2 = bd['data'][1] + " "+ bd['hora'][1]
                d2 = dt.datetime.strptime(hora_2, '%Y-%m-%d %H:%M')

                time_worked['horas'] = str(d2-d1)[:-3]

                insert = """
                insert into time_worked(data, horas) values('{data}', '{horas}')
                """.format(**time_worked)

                self.executeCommand(insert)
        return 0
    def inserPonto(self, data, hora, tipo):
        pass
    def close(self):
        self.conn.close()

class Relatorio(PontoBD):
    def __init__(self):
        super().__init__(PontoBD)