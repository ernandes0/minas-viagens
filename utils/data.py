import pandas as pd

class Data:

    def __init__(self):
        self.DATA_DIARIA_URL = ('data/ft_diarias_scdp.csv.parquet')
        self.DATA_ORGAO_URL = ('data/dm_orgao_scdp.csv')
        self.DATA_ESTADO_URL = ('data/dm_estado.csv')

    def get_data_diaria(self):
        data = pd.read_parquet(self.DATA_DIARIA_URL, sep = ';', engine = 'fastparquet')
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace = True)
        return data

    def get_data_orgao(self):
        data = pd.read_csv(self.DATA_ORGAO_URL, sep = ';')
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace = True)
        return data
    
    def get_data_estado(self):
        data = pd.read_csv(self.DATA_ESTADO_URL, sep = ';')
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace = True)
        return data
    
    def get_data_join_diaria_orgao(self):
        df1 = Data().get_data_orgao()
        df2 = Data().get_data_diaria()
        df3 = Data().get_data_estado()
        rdf = pd.merge(df1, df2[['id_orgao', 'id_favorecido', 'id_estado_destino','id_tipo_viagem', 'dt_inicio_trecho', 'dt_fim_trecho','vr_diaria']], how = "left", on = 'id_orgao')
        rdf.rename(columns = {'id_estado_destino':'id_estado', 'nome': 'nome_orgao'}, inplace = True)
        result = pd.merge(rdf, df3[['id_estado', 'nome']], how = 'left', on = 'id_estado')
        result.loc[:, ['id_orgao','id_favorecido', 'cd_orgao', 'id_estado', 'id_tipo_viagem']] = result.loc[:,['id_orgao','id_favorecido', 'cd_orgao', 'id_estado', 'id_tipo_viagem']].astype('Int64')
        return result