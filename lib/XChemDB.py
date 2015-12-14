import sqlite3
import os,sys
import csv

# committed on: 05/12/2015

sys.path.append(os.getenv('XChemExplorer_DIR')+'/lib')
from XChemUtils import parse

class data_source:

    def __init__(self,data_source_file):

        self.data_source_file=data_source_file
        print self.data_source_file
        #   [column_name in DB, column_name shown in XCE, SQLite column type (Integer,Text,PKEY...)]

        self.column_list=[
            # SQLite column name                    XCE column name                             SQLite type
            # from Lab36
            ['ID',                                   'ID',                                      'INTEGER PRIMARY KEY'],
            ['LabVisit',                             'LabVisit',                                'TEXT'],
            ['LibraryPlate',                         'LibraryPlate',                            'TEXT'],
            ['SourceWell',                           'SourceWell',                              'TEXT'],
            ['LibraryName',                          'LibraryName',                             'TEXT'],
            ['CompoundSMILES',                       'Smiles',                                  'TEXT'],
            ['CompoundCode',                         'Compound ID',                             'TEXT'],
            ['CrystalPlate',                         'CrystalPlate',                            'TEXT'],
            ['CrystalWell',                          'CrystalWell',                             'TEXT'],
            ['EchoX',                                'EchoX',                                   'TEXT'],
            ['EchoY',                                'EchoY',                                   'TEXT'],
            ['DropVolume',                           'DropVolume',                              'TEXT'],
            ['ProteinName',                          'ProteinName',                             'TEXT'],
            ['BatchNumber',                          'BatchNumber',                             'TEXT'],
            ['CompoundStockConcentration',           'CompoundStockConcentration',              'TEXT'],
            ['CompoundConcentration',                'CompoundConcentration',                   'TEXT'],
            ['SolventFraction',                      'SolventFraction',                         'TEXT'],
            ['SoakTransferVol',                      'SoakTransferVol',                         'TEXT'],
            ['SoakStatus',                           'SoakStatus',                              'TEXT'],
            ['SoakTimestamp',                        'SoakTimestamp',                           'TEXT'],
            ['CryoStockFraction',                    'CryoStockFraction',                       'TEXT'],
            ['CryoFraction',                         'CryoFraction',                            'TEXT'],
            ['CryoWell',                             'CryoWell',                                'TEXT'],
            ['CryoTransferVolume',                   'CryoTransferVolume',                      'TEXT'],
            ['CryoStatus',                           'CryoStatus',                              'TEXT'],
            ['CryoTimestamp',                        'CryoTimestamp',                           'TEXT'],
            ['SoakingTime',                          'SoakingTime',                             'TEXT'],
            ['HarvestStatus',                        'HarvestStatus',                           'TEXT'],
            ['CrystalName',                          'Sample ID',                               'TEXT'],
            ['Puck',                                 'Puck',                                    'TEXT'],
            ['PuckPosition',                         'PuckPosition',                            'TEXT'],
            ['PinBarcode',                           'PinBarcode',                              'TEXT'],
            ['MountingResult',                       'MountingResult',                          'TEXT'],
            ['MountingArrivalTime',                  'MountingArrivalTime',                     'TEXT'],
            ['MountedTimestamp',                     'MountedTimestamp',                        'TEXT'],
            ['MountingTime',                         'MountingTime',                            'TEXT'],
            ['ispybStatus',                          'ispybStatus',                             'TEXT'],
            ['DataCollectionVisit',                  'DataCollectionVisit',                     'TEXT'],
            # from XChemExplorer
            ['CompoundName',                         'Compound Name',                           'TEXT'],
            ['CrystalTag',                           'Tag',                                     'TEXT'],
            ['CrystalForm',                          'Crystal\nForm',                           'TEXT'],
            ['DataCollectionBeamline',               'DataCollectionBeamline',                  'TEXT'],
            ['DataCollectionDate',                   'DataCollectionDate',                      'TEXT'],
            ['DataCollectionOutcome',                'DataCollection\nOutcome',                   'TEXT'],
            ['DataCollectionRun',                    'DataCollectionRun',                       'TEXT'],
            ['DataCollectionComment',                'DataCollectionComment',                   'TEXT'],
            ['DataProcessingProgram',                'DataProcessingProgram',                   'TEXT'],
            ['DataProcessingSpaceGroup',             'DataProcessing\nSpaceGroup',                'TEXT'],
            ['DataProcessingUnitCell',               'DataProcessingUnitCell',                  'TEXT'],
            ['DataProcessingResolutionOverall',      'DataProcessingResolutionOverall',         'TEXT'],
            ['DataProcessingResolutionLow',          'DataProcessingResolutionLow',             'TEXT'],
            ['DataProcessingResolutionHigh',         'DataProcessing\nResolutionHigh',            'TEXT'],
            ['DataProcessingRmergeOverall',          'DataProcessingRmergeOverall',             'TEXT'],
            ['DataProcessingRmergeLow',              'DataProcessingRmergeLow',                 'TEXT'],
            ['DataProcessingRmergeHigh',             'DataProcessingRmergeHigh',                'TEXT'],
            ['DataProcessingIsigOverall',            'DataProcessingIsigOverall',               'TEXT'],
            ['DataProcessingIsigLow',                'DataProcessingIsigLow',                   'TEXT'],
            ['DataProcessingIsigHigh',               'DataProcessingIsigHigh',                  'TEXT'],
            ['DataProcessingCompletenessOverall',    'DataProcessingCompletenessOverall',       'TEXT'],
            ['DataProcessingCompletenessLow',        'DataProcessingCompletenessLow',           'TEXT'],
            ['DataProcessingCompletenessHigh',       'DataProcessingCompletenessHigh',          'TEXT'],
            ['DataProcessingMultiplicityOverall',    'DataProcessingMultiplicityOverall',       'TEXT'],
            ['DataProcessingMultiplicityLow',        'DataProcessingMultiplicityLow',           'TEXT'],
            ['DataProcessingMultiplicityHigh',       'DataProcessingMultiplicityHigh',          'TEXT'],
            ['DataProcessingPathToLogfile',          'DataProcessingPathToLogfile',             'TEXT'],
            ['PANDDAstuff',                          'PANDDAstuff',                             'TEXT'],
            ['RefinementRcryst',                     'Refinement\nRcryst',                        'TEXT'],
            ['RefinementRfree',                      'Refinement\nRfree',                         'TEXT'],
            ['RefinementLigandCC',                   'RefinementLigandCC',                      'TEXT'],
            ['RefinementRmsdBonds',                  'RefinementRmsdBonds',                     'TEXT'],
            ['RefinementRmsdAngles',                 'RefinementRmsdAngles',                    'TEXT'],
            ['RefinementOutcome',                    'Refinement\nOutcome',                       'TEXT'],
            ['RefinementMTZfree',                    'RefinementMTZfree',                       'TEXT'],
            ['RefinementCIF',                        'RefinementCIF',                           'TEXT'],
            ['RefinementPDB_latest',                 'RefinementPDB_latest',                    'TEXT'],
            ['RefinementMTZ_latest',                 'RefinementMTZ_latest',                    'TEXT'],
            ['RefinementComment',                    'RefinementComment',                       'TEXT'],
            ['AssayIC50',                            'AssayIC50',                               'TEXT']
        ]

    def create_missing_columns(self):
        existing_columns=[]
        connect=sqlite3.connect(self.data_source_file)
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM mainTable")
        for column in cursor.description:
            existing_columns.append(column[0])
        for column in self.column_list:
            if column[0] not in existing_columns:
                cursor.execute("alter table mainTable add column '"+column[0]+"' '"+column[2]+"'")
                connect.commit()

    def return_column_list(self):
        return self.column_list


    def create_empty_data_source_file(self):

        connect=sqlite3.connect(self.data_source_file)     # creates sqlite file if non existent
        with connect:
            cursor = connect.cursor()
            cursor.execute("CREATE TABLE mainTable("+self.column_list[0][0]+' '+self.column_list[0][2]+")")
            for i in range(1,len(self.column_list)):
                cursor.execute("alter table mainTable add column '"+self.column_list[i][0]+"' '"+self.column_list[i][2]+"'")
            connect.commit()

    def get_all_samples_in_data_source_as_list(self):
        connect=sqlite3.connect(self.data_source_file)     # creates sqlite file if non existent
        cursor = connect.cursor()
        cursor.execute("SELECT CrystalName FROM mainTable")
        existing_samples_in_db=[]
        samples = cursor.fetchall()
        for sample in samples:
            existing_samples_in_db.append(str(sample[0]))
        return existing_samples_in_db

    def check_if_sample_exists_in_data_source(self,sampleID):
        sample_exists=False
        existing_samples_in_db=self.get_all_samples_in_data_source_as_list()
        if sampleID in existing_samples_in_db:
            sample_exists=True
        return sample_exists

    def import_csv_file(self,csv_file):
        connect=sqlite3.connect(self.data_source_file)     # creates sqlite file if non existent
        cursor = connect.cursor()
        available_columns=[]
        cursor.execute("SELECT * FROM mainTable")
        for column in cursor.description:           # only update existing columns in data source
            available_columns.append(column[0])
        with open(csv_file,'rb') as csv_import: # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            csv_dict = csv.DictReader(csv_import) # comma is default delimiter
            for line in csv_dict:
                sampleID=line['CrystalName']
                if str(sampleID).replace(' ','')=='':
                    continue
                if self.check_if_sample_exists_in_data_source(sampleID):
                    update_string=''
                    for key,value in line.iteritems():
                        if key=='ID' or key=='CrystalName':
                            continue
                        if key not in available_columns:
                            continue
                        if not str(value).replace(' ','')=='':  # ignore if nothing in csv field
                            update_string+=str(key)+'='+"'"+str(value)+"'"+','
                    cursor.execute("UPDATE mainTable SET "+update_string[:-1]+" WHERE CrystalName="+"'"+sampleID+"'")
                else:
                    column_string=''
                    value_string=''
                    for key,value in line.iteritems():
                        if key=='ID':
                            continue
                        if key not in available_columns:
                            continue
                        if not str(value).replace(' ','')=='':  # ignore if nothing in csv field
                            value_string+="'"+value+"'"+','
                            column_string+=key+','
                    print sampleID
                    print          "INSERT INTO mainTable ("+column_string[:-1]+") VALUES ("+value_string[:-1]+");"
                    cursor.execute("INSERT INTO mainTable ("+column_string[:-1]+") VALUES ("+value_string[:-1]+");")

        connect.commit()

    def update_data_source(self,sampleID,data_dict):
        connect=sqlite3.connect(self.data_source_file)
        cursor = connect.cursor()
        update_string=''
        for key in data_dict:
            value=data_dict[key]
            if key=='ID' or key=='CrystalName':
                continue
            if not str(value).replace(' ','')=='':  # ignore empty fields
                update_string+=str(key)+'='+"'"+str(value)+"'"+','
        if update_string != '':
            cursor.execute("UPDATE mainTable SET "+update_string[:-1]+" WHERE CrystalName="+"'"+sampleID+"'")
            connect.commit()

    def update_insert_not_null_fields_only(self,sampleID,data_dict):
        connect=sqlite3.connect(self.data_source_file)
        cursor = connect.cursor()
        cursor.execute('Select CrystalName FROM mainTable')
        available_columns=[]
        cursor.execute("SELECT * FROM mainTable")
        for column in cursor.description:           # only update existing columns in data source
            available_columns.append(column[0])
        if self.check_if_sample_exists_in_data_source(sampleID):
            for key in data_dict:
                value=data_dict[key]
                print value
                if key=='ID' or key=='CrystalName':
                    continue
                if not str(value).replace(' ','')=='':  # ignore empty fields
                    update_string=str(key)+'='+"'"+str(value)+"'"
                    cursor.execute("UPDATE mainTable SET "+update_string+" WHERE CrystalName="+"'"+sampleID+"' and "+str(key)+" is null;")
        else:
            column_string='CrystalName'+','
            value_string="'"+sampleID+"'"+','
            for key in data_dict:
                value=data_dict[key]
                if key=='ID':
                    continue
                if key not in available_columns:
                    continue
                if not str(value).replace(' ','')=='':  # ignore if nothing in csv field
                    value_string+="'"+value+"'"+','
                    column_string+=key+','
            print          "INSERT INTO mainTable ("+column_string[:-1]+") VALUES ("+value_string[:-1]+");"
            cursor.execute("INSERT INTO mainTable ("+column_string[:-1]+") VALUES ("+value_string[:-1]+");")
        connect.commit()

    def get_value_from_field(self,sampleID,column):
        cursor.execute("SELECT "+column+" FROM  mainTable WHERE CrystalName='"+sampleID+"';")
        return cursor.fetchone()

    def export_to_csv_file(self,csv_file):
        connect=sqlite3.connect(self.data_source_file)
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM mainTable")
        header=()
        for column in cursor.description:
            header+=(column[0],)
        rows = cursor.fetchall()
        csvWriter = csv.writer(open(csv_file, "w"))
        csvWriter.writerows([header]+rows)
#        print cursor.description
#        print header


    def load_samples_from_data_source(self):
        header=[]
        data=[]
        connect=sqlite3.connect(self.data_source_file)
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM mainTable")
        for column in cursor.description:
            header.append(column[0])
        data = cursor.fetchall()
        return ([header,data])



    def get_data_dict_to_save_autoprocessing_results_to_data_source(self,sample,outcome,logfile):
        if logfile != None:
            aimless_results=parse().GetAimlessLog(logfile)
            data_dict =  {
                'DataCollectionBeamline':               'n/a',
                'DataCollectionDate':                   'n/a',
                'DataCollectionOutcome':                outcome,
                'DataCollectionRun':                    aimless_results['Run'],
                'DataCollectionComment':                'n/a',
                'DataProcessingProgram':                aimless_results['AutoProc'],
                'DataProcessingSpaceGroup':             aimless_results['SpaceGroup'],
                'DataProcessingUnitCell':               aimless_results['UnitCell'],
                'DataProcessingResolutionOverall':      aimless_results['ResolutionLow']+'-'+aimless_results['ResolutionHigh'],
                'DataProcessingResolutionLow':          aimless_results['ResolutionLow'],
                'DataProcessingResolutionHigh':         aimless_results['ResolutionHigh'],
                'DataProcessingRmergeOverall':          aimless_results['RmergeOverall'],
                'DataProcessingRmergeLow':              aimless_results['RmergeLow'],
                'DataProcessingRmergeHigh':             aimless_results['RmergeHigh'],
                'DataProcessingIsigOverall':            aimless_results['IsigOverall'],
                'DataProcessingIsigLow':                aimless_results['IsigLow'],
                'DataProcessingIsigHigh':               aimless_results['IsigHigh'],
                'DataProcessingCompletenessOverall':    aimless_results['CompletenessOverall'],
                'DataProcessingCompletenessLow':        aimless_results['CompletenessLow'],
                'DataProcessingCompletenessHigh':       aimless_results['CompletenessHigh'],
                'DataProcessingMultiplicityOverall':    aimless_results['MultiplicityOverall'],
                'DataProcessingMultiplicityLow':        aimless_results['MultiplicityLow'],
                'DataProcessingMultiplicityHigh':       aimless_results['MultiplicityHigh'],
                'DataProcessingPathToLogfile':          logfile    }
        else:
            data_dict=  {
                'DataCollectionBeamline':              'n/a',
                'DataCollectionDate':                  'n/a',
                'DataCollectionOutcome':               outcome,
                'DataCollectionRun':                   'n/a',
                'DataCollectionComment':               'n/a',
                'DataProcessingProgram':               'n/a',
                'DataProcessingSpaceGroup':            'n/a',
                'DataProcessingUnitCell':              'n/a',
                'DataProcessingResolutionOverall':     'n/a',
                'DataProcessingResolutionLow':         'n/a',
                'DataProcessingResolutionHigh':        'n/a',
                'DataProcessingRmergeOverall':         'n/a',
                'DataProcessingRmergeLow':             'n/a',
                'DataProcessingRmergeHigh':            'n/a',
                'DataProcessingIsigOverall':           'n/a',
                'DataProcessingIsigLow':               'n/a',
                'DataProcessingIsigHigh':              'n/a',
                'DataProcessingCompletenessOverall':   'n/a',
                'DataProcessingCompletenessLow':       'n/a',
                'DataProcessingCompletenessHigh':      'n/a',
                'DataProcessingMultiplicityOverall':   'n/a',
                'DataProcessingMultiplicityLow':       'n/a',
                'DataProcessingMultiplicityHigh':      'n/a',
                'DataProcessingPathToLogfile':         'n/a'    }

        return data_dict



    def get_samples_for_coot(self,RefinementOutcome):
        # 0: sampleID
        # 1: compoundID
        # 2: dataset outcome
        sample_list_for_coot=[]
        colums_for_coot=[['RefinementOutcome',  None],
                         ['CrystalName',        None],
                         ['CompoundCode',       None]]
        connect=sqlite3.connect(self.data_source_file)
        cursor = connect.cursor()

        cursor.execute("SELECT CrystalName,CompoundCode FROM mainTable WHERE %s;" % RefinementOutcome )

        sample_list_for_coot= cursor.fetchall()
        return sample_list_for_coot



