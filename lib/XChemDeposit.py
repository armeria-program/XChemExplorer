# last edited: 16/05/2017, 15:00

import sys
import os
import glob

from PyQt4 import QtGui, QtCore, QtWebKit

from lxml import etree

sys.path.append(os.getenv('XChemExplorer_DIR')+'/lib')
import XChemLog
import XChemDB
import XChemToolTips
import XChemWarnings
import XChemScript
import XChemMain
from XChemUtils import pdbtools
from XChemUtils import smilestools


class templates:

    def data_template_cif(self,depositDict):

        taxonomy_dict=XChemMain.NCBI_taxonomy_ID()
        for key in taxonomy_dict:
            if taxonomy_dict[key]==depositDict['Source_organism_scientific_name']:
                pdbx_gene_src_ncbi_taxonomy_id=key
            if taxonomy_dict[key]==depositDict['Expression_system_scientific_name']:
                pdbx_host_org_ncbi_taxonomy_id=key

#        structure_author_name=''
#        for name in depositDict['structure_author_name'].split(';'):
#            structure_author_name+='<structure_author_name=  %s>\n' %name

        audit_author_name=''
        # one name must be within quotation, last name and first initial must be separated by comma and space
        for name in depositDict['structure_author_name'].split(';'):
            if name.replace(' ','') == '':
                continue
            if name[name.find(',')+1:name.find(',')+2] != ' ':
                name=name.replace(',',', ')
            audit_author_name+="'{0!s}'\n".format(name)

        primary_citation_author_name=''
        # one name must be within quotation, last name and first initial must be separated by comma and space
        for name in depositDict['primary_citation_author_name'].split(';'):
            if name.replace(' ','') == '':
                continue
            if name[name.find(',')+1:name.find(',')+2] != ' ':
                name=name.replace(',',', ')
            primary_citation_author_name+="primary '{0!s}'\n".format(name)

        molecule_one_letter_sequence=';'
        counter=1
        for aa in depositDict['molecule_one_letter_sequence']:
            if counter < 70:
                molecule_one_letter_sequence+=aa
            if counter == 70:
                molecule_one_letter_sequence+='\n'+aa
                counter = 0
            counter+=1

        data_template_cif = (
            'data_UNNAMED\n'
            '#\n'
            '_pdbx_database_status.entry_id                       UNNAMED\n'
            "_pdbx_database_status.dep_release_code_coordinates   '%s'\n"                       %depositDict['Release_status_for_coordinates']+
            "_pdbx_database_status.dep_release_code_sequence      '{0!s}'\n".format(depositDict['Release_status_for_sequence'])+
            '#\n'
            '_pdbx_deposit_group.group_id	   UNNAMED\n'
            '_pdbx_deposit_group.group_description  "%s"\n'                                     %depositDict['group_description']+
            '_pdbx_deposit_group.group_title        "{0!s}"\n'.format(depositDict['group_title'])+
            '_pdbx_deposit_group.group_type         "{0!s}"\n'.format(depositDict['group_type'])+
            '#\n'
            '_exptl_crystal_grow.crystal_id      1\n'
            "_exptl_crystal_grow.method          '%s'\n"                                        %depositDict['crystallization_method']+
            '_exptl_crystal_grow.pH              {0!s}\n'.format(depositDict['crystallization_pH'])+
            '_exptl_crystal_grow.temp            {0!s}\n'.format(depositDict['crystallization_temperature'])+
            '_exptl_crystal_grow.pdbx_details    "{0!s}"\n'.format(depositDict['crystallization_details'])+
            '#\n'
            '_diffrn.id                     1\n'
            '_diffrn.ambient_temp           %s\n'                                               %depositDict['data_collection_temperature']+
            '_diffrn.crystal_id             1\n'
            '#\n'
            '_diffrn_source.diffrn_id                       1\n'
            '_diffrn_source.source                          %s\n'                               %depositDict['radiation_source']+
            '_diffrn_source.type                            "{0!s}"\n'.format(depositDict['radiation_source_type'])+
            '_diffrn_source.pdbx_wavelength_list            {0!s}\n'.format(depositDict['radiation_wavelengths'])+
            '#\n'
            '_diffrn_detector.detector               %s\n'                                      %depositDict['radiation_detector']+
            "_diffrn_detector.type                   '{0!s}'\n".format(depositDict['radiation_detector_type'])+
            '_diffrn_detector.pdbx_collection_date   {0!s}\n'.format(depositDict['data_collection_date'])+
            '_diffrn_detector.diffrn_id              1\n'
            '#\n'
            '_diffrn_radiation.diffrn_id                        1\n'
            '_diffrn_radiation.wavelength_id                    1\n'
            "_diffrn_radiation.pdbx_diffrn_protocol             'SINGLE WAVELENGTH'\n"
            '#\n'
            '_diffrn_radiation_wavelength.id           1\n'
            '_diffrn_radiation_wavelength.wavelength   %s\n'                                    %depositDict['radiation_wavelengths']+
            '#\n'
            '#\n'
            'loop_\n'
            '_entity.id\n'
            '_entity.type\n'
            '_entity.src_method\n'
            '_entity.pdbx_description\n'
            '_entity.pdbx_mutation\n'
            '1 polymer     man "%s" %s\n'                                                          %(depositDict['Source_organism_gene'],depositDict['fragment_name_one_specific_mutation'])+
            '#\n'
            'loop_\n'
            '_entity_poly.entity_id\n'
            '_entity_poly.type\n'
            '_entity_poly.pdbx_seq_one_letter_code\n'
            '_entity_poly.pdbx_strand_id\n'
            '_entity_poly.pdbx_seq_db_id\n'
            '_entity_poly.pdbx_seq_db_name\n'
            '1 "polypeptide(L)"\n'
            +molecule_one_letter_sequence+'\n'
            ';\n'
            '%s %s UNP\n'                                        %(depositDict['protein_chains'],depositDict['molecule_one_letter_sequence_uniprot_id'])+
            '#\n'
            'loop_\n'
            '_entity_src_gen.entity_id\n'
            '_entity_src_gen.gene_src_strain\n'
            '_entity_src_gen.pdbx_gene_src_scientific_name\n'
            '_entity_src_gen.pdbx_gene_src_ncbi_taxonomy_id\n'
            '_entity_src_gen.pdbx_host_org_scientific_name\n'
            '_entity_src_gen.pdbx_host_org_ncbi_taxonomy_id\n'
            '1 ? "%s" %s  "%s" %s\n'                %(depositDict['Source_organism_scientific_name'],pdbx_gene_src_ncbi_taxonomy_id,depositDict['Expression_system_scientific_name'],pdbx_host_org_ncbi_taxonomy_id)+
            '#\n'
            'loop_\n'
            '_pdbx_contact_author.id                  \n'
            "_pdbx_contact_author.address_1           \n"
            '_pdbx_contact_author.address_2           \n'
            '_pdbx_contact_author.city                \n'
            "_pdbx_contact_author.state_province      \n"
            '_pdbx_contact_author.postal_code         \n'
            '_pdbx_contact_author.email               \n'
            '_pdbx_contact_author.name_first          \n'
            '_pdbx_contact_author.name_last           \n'
            '_pdbx_contact_author.country             \n'
            '_pdbx_contact_author.phone               \n'
            '_pdbx_contact_author.role                \n'
            '_pdbx_contact_author.organization_type   \n'
            "1 '%s' '%s' '%s' '%s' '%s' %s %s '%s' '%s' '%s' '%s' %s\n" %(depositDict['contact_author_PI_address'],depositDict['contact_author_PI_organization_name'],depositDict['contact_author_PI_city'],depositDict['contact_author_PI_State_or_Province'],depositDict['contact_author_PI_Zip_Code'],depositDict['contact_author_PI_email'],depositDict['contact_author_PI_first_name'],depositDict['contact_author_PI_last_name'],depositDict['contact_author_PI_Country'],depositDict['contact_author_PI_phone_number'],depositDict['contact_author_PI_role'],depositDict['contact_author_PI_organization_type'])+
            "2 '{0!s}' '{1!s}' '{2!s}' '{3!s}' '{4!s}' {5!s} {6!s} '{7!s}' '{8!s}' '{9!s}' '{10!s}' {11!s}\n".format(depositDict['contact_author_address'], depositDict['contact_author_organization_name'], depositDict['contact_author_city'], depositDict['contact_author_State_or_Province'], depositDict['contact_author_Zip_Code'].replace(' ',''), depositDict['contact_author_email'], depositDict['contact_author_first_name'], depositDict['contact_author_last_name'], depositDict['contact_author_Country'], depositDict['contact_author_phone_number'], depositDict['contact_author_role'], depositDict['contact_author_organization_type'])+
            '#\n'
            'loop_\n'
            '_audit_author.name\n'
            +audit_author_name+
#            "'%s, %s.'\n" %(depositDict['contact_author_last_name'],depositDict['contact_author_first_name'][0])+
            '#\n'
            '_citation.id                        primary\n'
            "_citation.title                     '%s'\n"   %depositDict['group_title']+
            "_citation.journal_abbrev            'To Be Published'\n"
            '#\n'
            'loop_\n'
            '_citation_author.citation_id\n'
            '_citation_author.name\n'
            +primary_citation_author_name+
#        "primary 'Krojer, T.'\n"
#        "primary 'Von Delft, F.'\n"
            '#\n'
            '_struct.entry_id                     UNNAMED\n'
            '_struct.title\n'
            ';%s\n'                                                         %depositDict['title']+
            ';\n'
            '#\n'
            '_struct_keywords.entry_id        UNNAMED\n'
            '_struct_keywords.text            "%s"\n'                       %depositDict['structure_keywords']+
            '#\n'
            '_pdbx_struct_assembly_depositor_info.id                   1\n'
            "_pdbx_struct_assembly_depositor_info.method_details       PISA\n"
            '_pdbx_struct_assembly_depositor_info.oligomeric_count     %s\n'        %depositDict['biological_assembly_chain_number']+
            '#\n'
            '#\n'
            )

        return data_template_cif


class synchronise_check_depositTable(object):
    def __init__(self,deposit_dict,database,xce_logfile):
        self.deposit_dict=deposit_dict
        self.database=database
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)

        # types:
        # - apo         -> RefinementOutcome 1,2
        # - pending     -> RefinementOutcome 3,4
        # - bound       -> RefinementOutcome 5,6

        self.structureType = {  'apo':      [" '1%' ", " '1%' "],
                                'pending':  [" '3%' ", " '4%' "],
                                'bound':    [" '5%' ", " '7%' "]    }   # RefinementOutcome 7 does not exist;
                                                                        # just a dummy not to break sqlite query
        self.db_dict = {}
        self.condition_dict = {}


    def synchronise(self):

        # 1.) add all samples with successful data collection in mainTable but which are not
        #     in depsitTable to depositTable
        self.addMissingCrystalRecords()

        # 2.) assign structure type in depositTable based on RefinementOutcome in mainTable
        self.assignStructureType()

        # 3.) update/ insert depositTable based on entries in respectve deposit_dict
        self.updateDepositTable()

    def check(self):
        canStart = False
        missingEntries = self.db.execute_statement("select CrystalName from depositTable ""
                                                   "where group_deposition_title is null or "
                                                   "      group_deposition_title is '' "        )
        if missingEntries is not []:
            self.Logfile.insert('all records are complete depositTable; can continue with mmcif generation')
            canStart = True
        else:
            self.Logfile.error(XChemWarnings.incompleteDepsitTable())
        return canStart


    def addMissingCrystalRecords(self):
        # UNDER CONSTRUCTON
        xtalsToAdd = self.db.execute_statement('select CrystalName from mainTable where CrystalName not exists in depositTable')
        self.db.update_insert_any_table()

    def assignStructureType(self):
        for type in self.structureType:
            xtals = self.db.execute_statement('select CrystalName from mainTable where '
                                                'RefinementOutcome like %s or ' %self.structureType[type][0] +
                                                'RefinementOutcome like %s'     %self.structureType[type][1]    )
            for sample in xtals:
                self.db_dict['StructureType'] = type
                self.condition_dict['CrystalName'] = sample
                self.Logfile.insert('{0!s} setting StructureType to {1!s} in depositTable'.format(sample,type))
                self.db.update_insert_any_table('depositTable',db_dict,condition_dict)

    def updateDepositTable(self):
        for xtal in self.deposit_dict:
            self.condition_dict['CrystalName'] = xtal
            db_dict=self.translateBeamlines(self.deposit_dict[xtal])
            self.Logfile.insert('{0!s}: updating depositTable'.format(xtal))
            self.db.update_insert_any_table('depositTable',db_dict,condition_dict)



    def translateBeamlines(self,db_dict):
        dls_beamlines=['i02','i03','i04','i04-1','i23','i24']
        dls_beamline_dict = {   'i02':      ['DIAMOND BEAMLINE I02',    'DECTRIS PILATUS 6M'],
                                'i03':      ['DIAMOND BEAMLINE I03',    'DECTRIS PILATUS 6M'],
                                'i04':      ['DIAMOND BEAMLINE I04',    'DECTRIS PILATUS 6M'],
                                'i04-1':    ['DIAMOND BEAMLINE I04-1',  'DECTRIS PILATUS 6M'],
                                'i23':      ['DIAMOND BEAMLINE I23',    'DECTRIS PILATUS 12M'],
                                'i24':      ['DIAMOND BEAMLINE I24',    'DECTRIS PILATUS 6M'] ,     }

        if db_dict['radiation_source_type'] in dls_beamlines:
            db_dict['radiation_source_type']=    dls_beamline_dict[db_dict['radiation_source_type']][0]
            db_dict['radiation_detector_type']=  dls_beamline_dict[db_dict['radiation_source_type']][1]
            db_dict['radiation_detector']=       'PIXEL'
            db_dict['radiation_source']=         'SYNCHROTRON'
        return db_dict




class prepare_mmcif_files_for_deposition(QtCore.QThread):

    def __init__(self,database,xce_logfile,overwrite_existing_mmcif,projectDir,xtalList):
        QtCore.QThread.__init__(self)
        self.database=database
        self.db=XChemDB.data_source(database)
        self.overwrite_existing_mmcif=overwrite_existing_mmcif
        self.projectDir=projectDir

        self.data_template_dict={}
        self.data_template_apo='data_template_apo.cif'
        self.data_template_bound='data_template_bound.cif'
#        self.structureType=structureType
#        self.depositLog=XChemLog.depositLog('deposit.log')
#        self.depositLog.text('starting preparation of mmcif files for deposition')
#        self.success=0
#        self.successDict={}
        self.failureDict={}
#        self.n_toDeposit=0
#        self.counter=1

        self.xce_logfile=xce_logfile
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.Logfile.insert('preparing mmcif files for deposition ================>')

        self.xtalList = xtalList        # list comes from samples checked in deposition table in xce


    def run(self):

        progress=0
        progress_step = XChemMain.getProgressSteps(len(toDeposit))
        self.emit(QtCore.SIGNAL('update_progress_bar'), progress)

        for xtal in self.xtalList:

            self.Logfile.insert('{0!s}: reading general and deposition information from database'.format(xtal))
            deposit_dict = self.db.get_deposit_dict_for_sample(xtal)
            db_dict = self.db.get_db_dict_for_sample(xtal)


            #
            # check if mmcif files exist or need to be overwritten
            #

            if self.overwrite_existing_mmcif:
                self.remove_existing_mmcif_files(xtal)
            else:
                if self.mmcif_files_exist():
                    self.Logfile.warning('{0!s}: mmcif files exist; skipping to next sample'.format(xtal))
                    continue

            #
            # pre-checks for each sample
            #

            pre_checks_passed, eventMTZlist = self.make_pre_checks(xtal,deposit_dict,db_dict)
            if pre_checks_passed:
                self.Logfile.insert('{0!s}: pre-checks were OK, moving on'.format(xtal)
            else:
                self.Logfile.error('{0!s}: cannot start preparing mmcif file; check messages above!'.format(xtal))
                self.update_failureDict(xtal,deposit_dict,'pre-checks failed; for details see logfile')
                continue

            #
            # prepare data_template file for each sample
            #

            self.prepare_data_template_file(xtal,deposit_dict)


            #
            # make MODEL mmcif files
            #

            self.make_model_mmcif_file(xtal,db_dict,deposit_dict)
            if not model_mmcif_exists(xtal):
                continue
            self.update_model_mmcif_header()

            #
            # make SF mmcif files
            #

            self.make_sf_mmcif_file(xtal,db_dict,deposit_dict,eventMTZlist)


            progress += progress_step
            self.emit(QtCore.SIGNAL('update_progress_bar'), progress)

        #
        # prepare SUMMARY
        #





    def update_failureDict(self,xtal,deposit_dict,errorMsg):
        if xtal not in self.failureDict:
            self.failureDict[xtal] = []
        self.failureDict[xtal].append['{0!s}: {1!s} - {2!s}'.format(xtal,deposit_dict['StructureType'],errorMsg)]


    def make_pre_checks(self,xtal,deposit_dict,db_dict):
        self.Logfile.insert('{0!s} -> {1!s}: checking files for deposition ----------------->'.format(xtal,deposit_dict['StructureType']))
        checksOK = True

        checksOK = self.ligand_CIF_found(xtal,deposit_dict,db_dict,checksOK)

        checksOK = self.mtzfree_found(xtal,db_dict,checksOK)

        checksOK = self.dimple_files_found(xtal,deposit_dict,db_dict,checksOK)

        checksOK = self.refinement_files_found(xtal,deposit_dict,db_dict,checksOK)

        checksOK = self.occupancies_of_ligand_bound_structures(xtal,deposit_dict,db_dict,checksOK)

        checksOK = self.aimless_log_found(xtal,db_dict,checksOK)

        checksOK,eventMTZlist = self.pandda_related_issues(xtal,deposit_dict,db_dict,checksOK)

        return checksOK,eventMTZlist


    def occupancies_of_ligand_bound_structures(self,xtal,deposit_dict,db_dict,checksOK):
        if deposit_dict['StructureType'] == 'ligand_bound':
            self.Logfile.insert('{0!s} is ligand bound structure; checking occupanies of PDB file...'.format(xtal))
            if os.path.isfile(db_dict['RefinementPDB_latest']):
                errorMsg=pdbtools(db_dict['RefinementPDB_latest']).check_occupancies()
                if errorMsg[0] != '':
                    self.Logfile.error('{0!s}: problem with occupancies in REFINE PDB file'.format(xtal))
                    checksOK = False
            else:
                self.Logfile.error('{0!s}: cannot find REFINE PDB file for ligand bound structure'.format(xtal))
                checksOK = False
        return checksOK


    def refinement_files_found(self,xtal,deposit_dict,db_dict,checksOK):
        if deposit_dict['StructureType'] == 'ligand_bound':
            self.Logfile.insert('{0!s} is ligand bound structure; checking refinement file...'.format(xtal))
            if not os.path.isfile(db_dict['RefinementPDB_latest']):
                self.Logfile.error('{0!s}: cannot find REFINE PDB file for ligand bound structure'.format(xtal))
                checksOK = False
            if not os.path.isfile(db_dict['RefinementMTZ_latest']):
                self.Logfile.error('{0!s}: cannot find REFINE MTZ file for ligand bound structure'.format(xtal))
                checksOK = False
        return checksOK

    def mtzfree_found(self,xtal,db_dict,checksOK):
        if not os.path.isfile(db_dict['RefinementMTZfree']):
            self.Logfile.error('{0!s}: cannot find FREE MTZ file for apo structure'.format(xtal))
            checksOK = False
        return checksOK

    def aimless_log_found(self,xtal,db_dict,checksOK):
        if not os.path.isfile(db_dict['DataProcessingPathToLogfile']):
            self.Logfile.error('{0!s}: cannot find AIMLESS logfile'.format(xtal))
            checksOK = False
        return checksOK

    def dimple_files_found(self,xtal,deposit_dict,db_dict,checksOK):
        if deposit_dict['StructureType'] == 'apo':
            self.Logfile.insert('{0!s} is apo structure; checking files from initial refinement file...'.format(xtal))
            if not os.path.isfile(db_dict['DimplePathToPDB']):
                self.Logfile.error('{0!s}: cannot find DIMPLE PDB file for apo structure'.format(xtal))
                checksOK = False
            if not os.path.isfile(db_dict['DimplePathToMTZ']):
                self.Logfile.error('{0!s}: cannot find DIMPLE MTZ file for apo structure'.format(xtal))
                checksOK = False
        return checksOK

    def ligand_CIF_found(self,xtal,deposit_dict,db_dict,checksOK):
        if deposit_dict['StructureType'] == 'ligand_bound':
            self.Logfile.insert('{0!s} is ligand bound structure; checking presence of ligand cif file...'.format(xtal))
            if os.path.isfile(db_dict['RefinementCIF']):
                self.Logfile.insert('{0!s} found cif file!'.format(xtal))
            else:
                checksOK = False
                self.Logfile.error('{0!s}: cannot find ligand CIF file'.format(xtal))
        return checksOK

    def remove_existing_mmcif_files(self,xtal):
        os.chdir(os.path.join(self.projectDir,xtal))
        for data_template in glob.glob('data_template*'):
            self.Logfile.insert('{0!s}: removing {1!s}'.format(xtal,data_template))
            os.system('/bin/rm '+data_template)
        for mmcif in glob.glob('*.mmcif'):
            self.Logfile.insert('{0!s}: removing {1!s}'.format(xtal,mmcif))
            os.system('/bin/rm '+mmcif)
        self.Logfile.insert('{0!s}: updating depositTable'.format(xtal))
        self.db.update_insert_any_table('depositTable',{'mmCIF_model_file':'','mmCIF_SF_file':''},{'CrystalName':xtal})

    def pandda_related_issues(self,xtal,deposit_dict,db_dict,checksOK):
        eventMTZlist = []
        if deposit_dict['StructureType'] == 'ligand_bound':
            self.Logfile.insert('{0!s} is ligand bound structure; checking PanDDA information...'.format(xtal))
            # get ligands in PDB file
            ligandList = []
            if os.path.isfile(db_dict['RefinementPDB_latest']):
                ligandList = pdbtools(db_dict['RefinementPDB_latest']).find_ligands()
            else:
                self.Logfile.error('{0!s}: cannot find REFINE PDB file for ligand bound structure'.format(xtal))
                checksOK = False

            # get sample information for panddaTable
            panddaTable = self.db.get_db_list_for_sample_in_panddaTable(xtal)

            if ligandList is not []:
                for ligand in ligandList:
                    ligandID = ligand[0]+'-'+ligand[1]+'-'+ligand[2]
                    for entry in panddaTable:
                        databaseID = entry['PANDDA_site_ligand_id']
                        if ligandID == databaseID:
                            if not os.path.isfile(entry['PANDDA_site_event_map']):
                                self.Logfile.error('{0!s}: cannot find event map for {1!s}'.format(xtal,ligand))
                                checksOK = False
                            if not os.path.isfile(entry['PANDDA_site_event_map_mtz']):
                                self.Logfile.error('{0!s}: cannot find mtz file of event map for {1!s}'.format(xtal,ligand))
                                checksOK = False
                            eventMTZlist.append(entry['PANDDA_site_event_map_mtz'])

            if len(eventMTZlist) != len(ligandList):
                self.Logfile.error('{0!s}: not all ligands in PDB file are in the pandda table'.format(xtal))
                checksOK = False

        return checksOK,eventMTZlist


    def prepare_data_template_file(self,xtal,deposit_dict):
        os.chdir(os.path.join(self.projectDir,xtal))
        self.Logfile.insert('{0!s}: writing data_template.cif file to {1!s}'.format(xtal,os.getcwd()))
        data_template=templates().data_template_cif(deposit_dict)
        f=open(os.path.join(self.projectDir,xtal,self.data_template_apo),'w')
        f.write(data_template)
        f.close()

    def make_model_mmcif_file(self,xtal,db_dict,deposit_dict):
        cmd = XChemScript.pdb_extract(xtal,
                                      db_dict['RefinementProgram'],
                                      db_dict['RefinementPDB_latest'],
                                      db_dict['DataProcessingLOGfileName'],
                                      deposit_dict['data_integration_software'],
                                      deposit_dict['phasing_software']      )
        self.Logfile.insert('{0!s}: running pdb_extract -> {1!s}'.format(xtal,cmd))
        XChemScript.run_script_locally(cmd)

    def model_mmcif_exists(self,xtal):
        mmcifFound = False
        if os.path.isfile(os.path.join(self.projectDir,xtal,xtal+'.mmcif')) \
                and os.path.getsize(os.path.join(self.projectDir,xtal,xtal+'.mmcif')) > 20000: # even if pdb_extract files will it create a small file
            self.Logfile.insert('{0!s}: model mmcif file successfully created'.format(xtal))
            mmcifFound = True
        else:
            self.Logfile.error('{0!s}: model mmcif file was NOT created; skipping'.format(xtal))
        return mmcifFound

    def update_model_mmcif_header(self):
        cross_validation='?'
        starting_model='?'
        low_reso_list=[]        #
        softwareLine = 100000000
        foundSoftware=False
        softwareEntry=[]
        for n,line in enumerate(open(mmcif)):
            if foundSoftware:
                if line.split()[0] == '#':
                    softwareLine=n
                    foundSoftware=False
                try:
                    softwareEntry.append(int(line.split()[0]))
                except ValueError:
                    pass

            elif '_refine.pdbx_ls_cross_valid_method' in line and len(line.split()) == 2:
                cross_validation=line.split()[1]
            elif '_refine.pdbx_starting_model' in line and len(line.split()) == 2:
                starting_model=line.split()[1]
            elif '_reflns.d_resolution_low' in line and len(line.split()) == 2:
                low_reso_list.append(line.split()[1])
            elif '_refine.ls_d_res_low' in line and len(line.split()) == 2:
                low_reso_list.append(line.split()[1])
            elif '_software.language' in line:
                foundSoftware=True

        tmpText=''
        for n,line in enumerate(open(mmcif)):
            if '_refine.pdbx_ls_cross_valid_method' in line and cross_validation == '?':
                tmpText+='_refine.pdbx_ls_cross_valid_method               THROUGHOUT \n'

            elif '_refine.pdbx_starting_model' in line and starting_model == '?':
                tmpText+='_refine.pdbx_starting_model                      {0!s} \n'.format(self.data_template_dict['pdbx_starting_model'])

            elif '_refine.pdbx_method_to_determine_struct' in line:
                tmpText+="_refine.pdbx_method_to_determine_struct          'FOURIER SYNTHESIS'\n"

            elif '_reflns.d_resolution_low' in line and len(line.split()) == 2:
                tmpText+='_reflns.d_resolution_low             {0!s}\n'.format(min(low_reso_list))

            elif '_refine.ls_d_res_low' in line and len(line.split()) == 2:
                tmpText+='_refine.ls_d_res_low                             {0!s}\n'.format(min(low_reso_list))

            elif n == softwareLine:
                print 'software',softwareEntry
                tmpText+=   (   "{0!s} {1!s} ? ? program ? ? 'data reduction' ? ?\n".format(str(max(softwareEntry)+1), self.data_template_dict['data_integration_software'])+
                                '{0!s} {1!s} ? ? program ? ? phasing ? ?\n'.format(str(max(softwareEntry)+2), self.data_template_dict['phasing_software'])+
                                '#\n'   )

            else:
                tmpText+=line

        f=open(mmcif,'w')
        f.write(tmpText)
        f.close()
        if os.path.isfile(mmcif):
            self.Logfile.insert('mmcif file successfully updated')


    def make_sf_mmcif_file(self,xtal,db_dict,deposit_dict,eventMTZlist):
        mtzin = db_dict['RefinementMTZ_latest'] + ' ' + db_dict['RefinementMTZfree'] + ' '
        if deposit_dict['StructureType'] == 'ligand_bound':
            for event in eventMTZlist:
                mtzin+=event+' '



#----------------------------------------------------------------




                # first get all meta-data for deposition, i.e. data_template file
                wavelength=self.prepare_data_template_for_xtal(xtal,compoundID,pdb)

                # make model mmcif
                self.make_model_mmcif(xtal,pdb,log,refSoft)

                # make SF mmcif
                self.make_sf_mmcif(xtal,mtzFinal,mtzData,eventMtz)

                # report any problems that came up
                mmcif=self.check_mmcif_files_and_update_db(xtal,n_eventMtz,wavelength)

                # add ligand cif file to mmcif
                if self.structureType=='ligand_bound':
                    self.add_ligand_cif_file(mmcif,cif)

                self.Logfile.insert('finished preparation of mmcif files')


            else:
                self.Logfile.insert(XChemToolTips.deposition_pandda_site_not_ready(xtal))

            progress += progress_step
            self.emit(QtCore.SIGNAL('update_progress_bar'), progress)

        self.summary()

#    def updateFailureDict(self,xtal,error):
#        if xtal not in self.failureDict:
#            self.failureDict[xtal]=[]
#        self.failureDict[xtal].append(error)


    def summary(self):
        self.depositLog.summary(self.n_toDeposit,self.success,self.failureDict,self.structureType,self.successDict)

    def prepare_data_template_for_xtal(self,xtal,compoundID,pdb):

        #############################################################################################
        #
        #
        #
        # IMPORTANT: all these issues need to be resolved when information is saved to depositTable
        #
        #
        #
        #############################################################################################

        # check if file exists
        if self.overwrite_existing_mmcif:
            os.chdir(os.path.join(self.projectDir,xtal))
            data_template_dict=self.db.get_deposit_dict_for_sample(xtal)

            # edit title
            data_template_dict['group_title']=data_template_dict['group_deposition_title'].replace('$ProteinName',data_template_dict['Source_organism_gene']).replace('$CompoundName',compoundID)
            self.Logfile.insert('group deposition title for '+xtal+': '+data_template_dict['group_title'])
            self.depositLog.text('group title: '+data_template_dict['group_title'])
            if self.structureType=='ligand_bound':
                title=data_template_dict['structure_title'].replace('$ProteinName',data_template_dict['Source_organism_gene']).replace('$CompoundName',compoundID)
                data_template_dict['group_title']='PanDDA analysis group deposition of models with modelled events (e.g. bound ligands)'
            if self.structureType=='apo':
                title=data_template_dict['structure_title_apo'].replace('$ProteinName',data_template_dict['Source_organism_gene']).replace('$CompoundName',compoundID).replace('$n',str(self.counter))
                data_template_dict['group_title']='PanDDA analysis group deposition of models of ground state datasets'
                self.counter+=1
            data_template_dict['group_description']=data_template_dict['group_description'].replace('$ProteinName',data_template_dict['Source_organism_gene'])
            data_template_dict['title']=data_template_dict['group_title']+' -- '+title
            self.Logfile.insert('deposition title for '+xtal+': '+data_template_dict['title'])
            self.depositLog.text('title: '+data_template_dict['title'])
            if ('$ProteinName' or '$CompoundName') in data_template_dict['title']:
                self.updateFailureDict(xtal,'title not correctly formatted')

            # mutations
            mutations=data_template_dict['fragment_name_one_specific_mutation']
            if mutations.lower().replace(' ','').replace('none','').replace('null','') == '':
                data_template_dict['fragment_name_one_specific_mutation']='?'
            else:
                data_template_dict['fragment_name_one_specific_mutation']='"'+mutations.replace(' ','')+'"'

            # get protein chains
            data_template_dict['protein_chains']=''
            chains=pdbtools(pdb).GetProteinChains()
            for item in chains:
                data_template_dict['protein_chains']+=item+','
            data_template_dict['protein_chains']=data_template_dict['protein_chains'][:-1]

            data_template_dict['group_type'] = ''
            if self.structureType=='ligand_bound':
                self.Logfile.insert('creating {0!s} file for ligand bound structure of {1!s}'.format(self.data_template_bound, xtal))
                data_template_dict['group_type'] = 'changed state'
                data_template=templates().data_template_cif(data_template_dict)
                site_details=self.make_site_description(xtal)
                data_template+=site_details
                f=open(os.path.join(self.projectDir,xtal,self.data_template_bound),'w')
            elif self.structureType=='apo':
                self.Logfile.insert('creating {0!s} file for apo structure of {1!s}'.format(self.data_template_apo, xtal))
                data_template_dict['group_type'] = 'ground state'
                data_template=templates().data_template_cif(data_template_dict)
                site_details=self.make_site_description(xtal)
                data_template+=site_details
                f=open(os.path.join(self.projectDir,xtal,self.data_template_apo),'w')

            self.data_template_dict=data_template_dict
            f.write(data_template)
            f.close()

            wavelength=data_template_dict['radiation_wavelengths']
            return wavelength



    def make_model_mmcif(self,xtal,pdb,log,refSoft):
        if os.path.isfile(pdb) and os.path.isfile(log):
            os.chdir(os.path.join(self.projectDir,xtal))

            if self.structureType=='ligand_bound':
                out=xtal+'-bound'
                data_template=self.data_template_bound
                refSoft='PHENIX'
            elif self.structureType=='apo':
                out=xtal+'-apo'
                data_template=self.data_template_apo
                refSoft='REFMAC'

            refSoft=pdbtools(pdb).GetRefinementProgram()

            if os.path.isdir('/dls'):
                pdb_extract_init='source /dls/science/groups/i04-1/software/pdb-extract-prod/setup.sh\n'
                pdb_extract_init+='/dls/science/groups/i04-1/software/pdb-extract-prod/bin/pdb_extract'
            else:
                pdb_extract_init='source '+os.path.join(os.getenv('XChemExplorer_DIR'),'pdb_extract/pdb-extract-prod/setup.sh')+'\n'
                pdb_extract_init+=+os.path.join(os.getenv('XChemExplorer_DIR'),'pdb_extract/pdb-extract-prod/bin/pdb_extract')

            Cmd = ( pdb_extract_init+
#                    ' -r PHENIX'
                    ' -r {0!s}'.format(refSoft)+
#                    ' -iLOG initial.log'
                    ' -iPDB {0!s}'.format(pdb)+
#                    ' -i %s'            %self.data_template_dict['data_integration_software']+
#                    ' -p %s'            %self.data_template_dict['phasing_software']+
                    ' -e MR'
                    ' -s AIMLESS'
                    ' -iLOG %s'         %log+
                    ' -iENT {0!s}'.format(data_template)+
                    ' -o {0!s}.mmcif > {1!s}.mmcif.log'.format(out, out)       )

            self.Logfile.insert('running pdb_extract: '+Cmd)
            os.system(Cmd)

            # can we add here the ligand.cif?
#    '''pdb_extract -r REFMAC -iLOG initial.log -iPDB initial.pdb -e MR -s AIMLESS -iLOG aimless.log -iENT data_template.cif -o NUDT22A-x0315-model.cif'''


    def make_sf_mmcif(self,xtal,mtzFinal,mtzData,eventMtz):
        if os.path.isfile(mtzFinal):
            os.chdir(os.path.join(self.projectDir,xtal))

            mtzin = mtzFinal+' '+mtzData+' '
            if self.structureType=='ligand_bound':
                out=xtal+'-bound'
                for event in eventMtz:
                    mtzin+=event+' '

            elif self.structureType=='apo':
                out=xtal+'-apo'

            if os.path.isdir('/dls'):
                pdb_extract_init='source /dls/science/groups/i04-1/software/pdb-extract-prod/setup.sh\n'
                pdb_extract_init+='/dls/science/groups/i04-1/software/pdb-extract-prod/bin/sf_convert'
            else:
                pdb_extract_init='source '+os.path.join(os.getenv('XChemExplorer_DIR'),'pdb_extract/pdb-extract-prod/setup.sh')+'\n'
                pdb_extract_init+=+os.path.join(os.getenv('XChemExplorer_DIR'),'pdb_extract/pdb-extract-prod/bin/sf_convert')

            Cmd = ( pdb_extract_init+
                    ' -o mmcif'
                    ' -sf %s' %mtzin+
                    ' -out {0!s}_sf.mmcif  > {1!s}.sf_mmcif.log'.format(out, out) )

#            Cmd = ( os.path.join(os.getenv('XChemExplorer_DIR'),'pdb_extract/sf-convert-v1.204-prod-src/bin/sf_convert')+
#                    ' -o mmcif'
#                    ' -sf %s' %mtzin+
#                    ' -out %s_sf.mmcif > %s.sf_mmcif.log' %(xtal,xtal) )

            self.Logfile.insert('running sf_convert: '+Cmd)
            os.system(Cmd)
            os.system('/bin/rm sf_format_guess.text mtzdmp.log SF_4_validate.cif sf_information.cif')


    def check_mmcif_files_and_update_db(self,xtal,n_eventMtz,wavelength):
        os.chdir(os.path.join(self.projectDir,xtal))
        foundFiles=True

        mmcif=''
        if os.path.isfile(self.out+'.mmcif') and os.path.getsize(self.out+'.mmcif') > 20000 :
            self.Logfile.insert('found '+self.out+'.mmcif')
            mmcif=os.path.join(self.projectDir,xtal,self.out+'.mmcif')
            cross_validation='?'
            starting_model='?'
            low_reso_list=[]
            softwareLine = 100000000
            foundSoftware=False
            softwareEntry=[]
            for n,line in enumerate(open(mmcif)):
                if foundSoftware:
                    if line.split()[0] == '#':
                        softwareLine=n
                        foundSoftware=False

                    try:
                        softwareEntry.append(int(line.split()[0]))
                    except ValueError:
                        pass

                elif '_refine.pdbx_ls_cross_valid_method' in line and len(line.split()) == 2:
                    cross_validation=line.split()[1]
                elif '_refine.pdbx_starting_model' in line and len(line.split()) == 2:
                    starting_model=line.split()[1]
                elif '_reflns.d_resolution_low' in line and len(line.split()) == 2:
                    low_reso_list.append(line.split()[1])
                elif '_refine.ls_d_res_low' in line and len(line.split()) == 2:
                    low_reso_list.append(line.split()[1])
                elif '_software.language' in line:
                    foundSoftware=True

            tmpText=''
            for n,line in enumerate(open(mmcif)):
                if '_refine.pdbx_ls_cross_valid_method' in line and cross_validation == '?':
                    tmpText+='_refine.pdbx_ls_cross_valid_method               THROUGHOUT \n'

                elif '_refine.pdbx_starting_model' in line and starting_model == '?':
                    tmpText+='_refine.pdbx_starting_model                      {0!s} \n'.format(self.data_template_dict['pdbx_starting_model'])

                elif '_refine.pdbx_method_to_determine_struct' in line:
                    tmpText+="_refine.pdbx_method_to_determine_struct          'FOURIER SYNTHESIS'\n"

                elif '_reflns.d_resolution_low' in line and len(line.split()) == 2:
                    tmpText+='_reflns.d_resolution_low             {0!s}\n'.format(min(low_reso_list))

                elif '_refine.ls_d_res_low' in line and len(line.split()) == 2:
                    tmpText+='_refine.ls_d_res_low                             {0!s}\n'.format(min(low_reso_list))

                elif n == softwareLine:
                    print 'software',softwareEntry
                    tmpText+=   (   "{0!s} {1!s} ? ? program ? ? 'data reduction' ? ?\n".format(str(max(softwareEntry)+1), self.data_template_dict['data_integration_software'])+
                                    '{0!s} {1!s} ? ? program ? ? phasing ? ?\n'.format(str(max(softwareEntry)+2), self.data_template_dict['phasing_software'])+
                                    '#\n'   )

                else:
                    tmpText+=line

            f=open(mmcif,'w')
            f.write(tmpText)
            f.close()
            if os.path.isfile(mmcif):
                self.Logfile.insert('mmcif file successfully updated')

#        else:
#            self.Logfile.error('cannot find '+self.out+'.mmcif; something went wrong!')
#            self.depositLog.text('cannot find '+self.out+'.mmcif; something went wrong! => ERROR')
#            self.updateFailureDict(xtal,'cannot find '+self.out+'.mmcif')
#            foundFiles=False

        if os.path.isfile(self.out+'_sf.mmcif') and os.path.getsize(self.out+'_sf.mmcif') > 20000 :
            self.Logfile.insert('found '+self.out+'_sf.mmcif')
            mmcif_sf=os.path.join(self.projectDir,xtal,self.out+'_sf.mmcif')

            # now check if really all event maps are in mmcif file
            if self.structureType=='ligand_bound':
                n_eventMTZ_found=-2     # set to -2 since first two data blocks are initial/final.mtz and data.mtz
                for line in open(mmcif_sf):
                    if line.startswith('_refln.crystal_id'):
                        n_eventMTZ_found+=1
                if n_eventMTZ_found != n_eventMtz:
                    self.Logfile.error('{0!s} event map mtz files were specified as input, but only {1!s} ended up in the mmcif file'.format(str(n_eventMtz), str(n_eventMTZ_found)))
                    self.depositLog.text('{0!s} event map mtz files were specified as input, but only {1!s} ended up in the mmcif file => ERROR'.format(str(n_eventMtz), str(n_eventMTZ_found)))
                    self.updateFailureDict(xtal,'{0!s} event mtz in input; only {1!s} in mmcif SF file'.format(str(n_eventMtz), str(n_eventMTZ_found)))
                    foundFiles=False
                else:
                    self.Logfile.insert('{0!s} event map mtz files were specified as input, {1!s} ended up in the mmcif file, all well so far...'.format(str(n_eventMtz), str(n_eventMTZ_found)))

            self.Logfile.insert('editing wavelength information in SF mmcif file; changing wavelength to {0!s}'.format(wavelength))

            apo = [     "data from inital refinement with DIMPLE, initial.mtz",
                        "data from original reflection, data.mtz"]
            bound = [   "data from final refinement with ligand, final.mtz",
                        "data from original reflection, data.mtz",
                        "data for ligand evidence map (PanDDA event map), event_map1.mtz",
                        "data for ligand evidence map (PanDDA event map), event_map2.mtz",
                        "data for ligand evidence map (PanDDA event map), event_map3.mtz",
                        "data for ligand evidence map (PanDDA event map), event_map4.mtz",
                        "data for ligand evidence map (PanDDA event map), event_map5.mtz",
                        "data for ligand evidence map (PanDDA event map), event_map6.mtz",
                        "data for ligand evidence map (PanDDA event map), event_map7.mtz"       ]

            tmpText=''
            block=-1
            cif_block_found=0
            for line in open(mmcif_sf):
                if line.startswith('_cell.length_a'):
                    block+=1
                # need to do this because the data.mtz block could have missing screw axis
                if line.startswith('_symmetry.space_group_name_H-M') and cif_block_found == 1:
                    tmpText+=symmLine
                    cif_block_found+=1
                    continue
                if line.startswith('_symmetry.space_group_name_H-M') and cif_block_found == 0:
                    symmLine=line
                    cif_block_found+=1

                if line.startswith('_cell.angle_gamma'):
                    tmpText+=line
                    if self.structureType == 'apo':
                        addLines = (    '#\n'
                                        '_diffrn.id                  1\n'
                                        '_diffrn.details             "%s"\n' %apo[block]    )
                    if self.structureType == 'ligand_bound':
                        addLines = (    '#\n'
                                        '_diffrn.id                  1\n'
                                        '_diffrn.details             "%s"\n' %bound[block]    )
                    tmpText+=addLines
                    continue
                if line.startswith('_diffrn_radiation_wavelength.wavelength'):
                    tmpText+='_diffrn_radiation_wavelength.wavelength   {0!s}\n'.format(wavelength)
                else:
                    tmpText+=line
            f=open(mmcif_sf,'w')
            f.write(tmpText)
            f.close()
            if os.path.isfile(mmcif_sf):
                self.Logfile.insert('mmcif SF file successfully updated')
            else:
                self.Logfile.error('something went wrong during the update')
                self.depositLog.text('something went wrong during the update => ERROR')
                self.updateFailureDict(xtal,'error during mmcif SF update')
                foundFiles=False

        else:
            self.Logfile.error('cannot find '+self.out+'_sf.mmcif; something went wrong!')
            self.depositLog.text('cannot find '+self.out+'_sf.mmcif; something went wrong! => ERROR')
            self.updateFailureDict(xtal,'cannot find '+self.out+'_sf.mmcif')
            foundFiles=False

        if foundFiles:
            self.Logfile.insert('updating database with file locations for {0!s}.mmcif and {1!s}_sf.mmcif'.format(self.out, self.out))
            self.successDict[xtal]=[self.out+'mmcif',os.path.getsize(self.out+'.mmcif'),self.out+'_sf.mmcif',os.path.getsize(self.out+'_sf.mmcif')]
            self.success+=1
            self.db.execute_statement("update depositTable set mmCIF_model_file='{0!s}',mmCIF_SF_file='{1!s}' where CrystalName is '{2!s}' and StructureType is '{3!s}'".format(mmcif, mmcif_sf, xtal, self.structureType))
        else:
            self.Logfile.insert('could not find %s.mmcif and/or %s_sf.mmcif; removing empty files...')
            os.system('/bin/rm {0!s}.mmcif 2> /dev/null'.format(self.out))
            os.system('/bin/rm {0!s}_sf.mmcif 2> /dev/null'.format(self.out))

        return mmcif


    def add_ligand_cif_file(self,mmcif,ligand_cif):
        self.Logfile.insert('adding ligand cif file to {0!s}'.format(mmcif))
        tmpText=''
        for line in open(mmcif):
            tmpText+=line
        for line in open(ligand_cif):
            tmpText+=line
        f=open(mmcif,'w')
        f.write(tmpText)
        f.close()

    def make_site_description(self,xtal):
        mmcif_text='_pdbx_entry_details.nonpolymer_details\n;'

        general=self.db.execute_statement("select CompoundSMILES from mainTable where CrystalName is '{0!s}'".format(xtal))
        smiles=str(general[0][0])

        if self.structureType=='apo':
            self.Logfile.insert('SMILES string of soaked compound: {0!s}'.format(smiles))
            if smiles.lower() != 'none' or smiles.lower() != "null":
                self.Logfile.insert('adding _pdbx_entry_details.nonpolymer_details to mmcif')
                mmcif_text+='smiles string of soaked compound: {0!s}\n;\n'.format(smiles)
            else:
                mmcif_text=''

        if self.structureType=='ligand_bound':

            sqlite = (  "select "
                        " PANDDA_site_index,"
                        " PANDDA_site_x,"
                        " PANDDA_site_y,"
                        " PANDDA_site_y,"
                        " PANDDA_site_name,"
                        " PANDDA_site_confidence, "
                        " PANDDA_site_comment,"
                        " PANDDA_site_occupancy,"
                        " PANDDA_site_B_average,"
                        " PANDDA_site_B_ratio_residue_surroundings,"
                        " PANDDA_site_RSCC,"
                        " PANDDA_site_RSR,"
                        " PANDDA_site_RSZD,"
                        " PANDDA_site_rmsd "
                        "from panddaTable "
                        "where CrystalName is '%s' and PANDDA_site_ligand_placed is 'True' order by PANDDA_site_index ASC" %xtal)
#        panddaSites=self.db.execute_statement("select PANDDA_site_index,PANDDA_site_x,PANDDA_site_y,PANDDA_site_y,PANDDA_site_name,PANDDA_site_confidence from panddaTable where CrystalName is '%s' and PANDDA_site_ligand_placed is 'True' order by PANDDA_site_index ASC" %xtal)
            panddaSites=self.db.execute_statement(sqlite)

            root = etree.Element(xtal)
            child1 = etree.SubElement(root, "used_for_statistical_map")
            child1.text = 'yes'
            child2 = etree.SubElement(root, "smiles_of_compound_added")
            child2.text = '{0!s}'.format(smiles)

            site_descpription_complete=True
            for site in panddaSites:
                SiteIndex=  str(site[0]).replace(' ','')
                x_coord=    str(site[1])
                y_coord=    str(site[2])
                z_coord=    str(site[3])
                label=      str(site[4])
                confidence= str(site[5])
                comment=    str(site[6])
                occupancy=  str(site[7])
                Baverage=   str(site[8])
                Bratio=     str(site[9])
                RSCC=       str(site[10])
                RSR=        str(site[11])
                RSZD=       str(site[12])
                RMSD=       str(site[13])

                if 'none' in (SiteIndex.lower() or x_coord.lower() or y_coord.lower() or z_coord.lower() or confidence.lower() or occupancy.lower() or Bratio.lower() or Baverage.lower() or RSZD.lower() or RMSD.lower() or RSCC.lower() or RSR.lower()):
                    site_descpription_complete=False

                child = etree.SubElement(root, "site"+SiteIndex)
                childa = etree.SubElement(child, "label")
                childa.text = '{0!s}'.format(label)
                childx = etree.SubElement(child, "coordinate")
                childx.text = '{0!s} {1!s} {2!s}'.format(x_coord, y_coord, z_coord)
                childy = etree.SubElement(child, "smiles")
                childy.text = '{0!s}'.format(smiles)
                childz = etree.SubElement(child, "confidence")
                childz.text = '{0!s}'.format(confidence)
                childb = etree.SubElement(child, "comment")
                childb.text = '{0!s}'.format(comment)
                childc = etree.SubElement(child, "occupancy")
                childc.text = '{0!s}'.format(occupancy)
                childd = etree.SubElement(child, "B_average")
                childd.text = '{0!s}'.format(Baverage)
                childe = etree.SubElement(child, "B_ratio")
                childe.text = '{0!s}'.format(Bratio)
                childf = etree.SubElement(child, "RSCC")
                childf.text = '{0!s}'.format(RSCC)
                childg = etree.SubElement(child, "RSR")
                childg.text = '{0!s}'.format(RSR)
                childh = etree.SubElement(child, "RSZD")
                childh.text = '{0!s}'.format(RSZD)
                childi = etree.SubElement(child, "RMSD")
                childi.text = '{0!s}'.format(RMSD)

#        # pretty string
            s = etree.tostring(root, pretty_print=True)
            mmcif_text+=s+';\n'

            self.depositLog.site_xml(xtal,s)

            if not site_descpription_complete:
                self.updateFailureDict(xtal,'site description incomplete')

        return mmcif_text





class prepare_for_group_deposition_upload(QtCore.QThread):

    def __init__(self,database,xce_logfile,depositDir):
        QtCore.QThread.__init__(self)
        self.database=database
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)
        self.depositDir=depositDir



    def run(self):

        TextIndex=''
        os.chdir(self.depositDir)

        # ligand bound structures
        toDeposit=self.db.execute_statement("select CrystalName,mmCIF_model_file,mmCIF_SF_file from depositTable where StructureType is 'ligand_bound';")
        for item in sorted(toDeposit):
            xtal=str(item[0])
            mmcif=str(item[1])
            mmcif_sf=str(item[2])
            if os.path.isfile(mmcif) and os.path.isfile(mmcif_sf):
                self.Logfile.insert('copying {0!s} to {1!s}'.format(mmcif, self.depositDir))
                os.system('/bin/cp {0!s} .'.format(mmcif))
                self.Logfile.insert('copying {0!s} to {1!s}'.format(mmcif_sf, self.depositDir))
                os.system('/bin/cp {0!s} .'.format(mmcif_sf))
            else:
                self.Logfile.insert('cannot find apo mmcif file for '+xtal+' => ERROR')

            text = (    'label: {0!s}-ligand_bound\n'.format(xtal)+
                        'description: ligand_bound structure of {0!s}\n'.format(xtal)+
                        'model: {0!s}\n'.format(mmcif[mmcif.rfind('/')+1:])+
                        'sf: {0!s}\n\n'.format(mmcif_sf[mmcif_sf.rfind('/')+1:])          )
            TextIndex+=text

        f = open('index.txt','w')
        f.write(TextIndex)
        f.close()

        self.Logfile.insert('preparing tar archive...')
        os.system('tar -cvf ligand_bound_structures.tar *bound* index.txt')
        self.Logfile.insert('bzipping archive...')
        os.system('bzip2 ligand_bound_structures.tar')
        self.Logfile.insert('removing all bound mmcif files and index.txt file from '+self.depositDir)
        os.system('/bin/rm -f *bound*mmcif index.txt')
        self.Logfile.insert('done!')



        # apo structures
        TextIndex=''
        toDeposit=self.db.execute_statement("select CrystalName,mmCIF_model_file,mmCIF_SF_file from depositTable where StructureType is 'apo';")
        for item in sorted(toDeposit):
            xtal=str(item[0])
            mmcif=str(item[1])
            mmcif_sf=str(item[2])
            if os.path.isfile(mmcif) and os.path.isfile(mmcif_sf):
                self.Logfile.insert('copying {0!s} to {1!s}'.format(mmcif, self.depositDir))
                os.system('/bin/cp {0!s} .'.format(mmcif))
                self.Logfile.insert('copying {0!s} to {1!s}'.format(mmcif_sf, self.depositDir))
                os.system('/bin/cp {0!s} .'.format(mmcif_sf))
            else:
                self.Logfile.insert('cannot find apo mmcif file for '+xtal+' => ERROR')

            text = (    'label: {0!s}-apo\n'.format(xtal)+
                        'description: apo structure of {0!s}\n'.format(xtal)+
                        'model: {0!s}\n'.format(mmcif[mmcif.rfind('/')+1:])+
                        'sf: {0!s}\n\n'.format(mmcif_sf[mmcif_sf.rfind('/')+1:])          )
            TextIndex+=text

        f = open('index.txt','w')
        f.write(TextIndex)
        f.close()

        self.Logfile.insert('preparing tar archive...')
        os.system('tar -cvf apo_structures.tar *apo* index.txt')
        self.Logfile.insert('bzipping archive...')
        os.system('bzip2 apo_structures.tar')
        self.Logfile.insert('removing all apo mmcif files and index.txt file from '+self.depositDir)
        os.system('/bin/rm -f *apo*mmcif index.txt')
        self.Logfile.insert('done!')




class import_PDB_IDs(QtCore.QThread):
    def __init__(self,pdbCodes,database,xce_logfile):
        QtCore.QThread.__init__(self)
        self.pdbCodes=pdbCodes
        self.database=database
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)

    def run(self):

        for line in self.pdbCodes.split('\n'):
            if len(line.split('/')) == 2 and '-ligand_bound' in line:
                xtal=line[:line.rfind('-ligand_bound')].replace(' ','')
                pdbID=line.split('/')[1].replace(' ','')
                self.Logfile.insert('setting PDB ID for '+xtal+' to '+pdbID)
                sqlite="UPDATE mainTable SET Deposition_PDB_ID='{0!s}',RefinementOutcome='6 - Deposited' where CrystalName is '{1!s}';".format(pdbID, xtal)
                self.db.execute_statement(sqlite)


class compare_smiles_in_db_with_ligand_in_pdb(QtCore.QThread):
    def __init__(self,projectDir,database,xce_logfile):
        QtCore.QThread.__init__(self)
        self.projectDir=projectDir
        self.database=database
        self.Logfile=XChemLog.updateLog(xce_logfile)
        self.db=XChemDB.data_source(database)
        self.ErrorDict={}

    def update_ErrorDict(self,xtal,message):
        if xtal not in self.ErrorDict:
            self.ErrorDict[xtal]=[]
        self.ErrorDict[xtal].append(message)

    def run(self):

        os.chdir(self.projectDir)

        progress_step=1
        if len(glob.glob('*')) != 0:
            progress_step=100/float(len(glob.glob('*')))
        else:
            progress_step=1
        progress=0
        self.emit(QtCore.SIGNAL('update_progress_bar'), progress)


        for xtal in sorted(glob.glob('*')):
            if os.path.isfile(os.path.join(xtal,'refine.pdb')):
                smiles=self.db.execute_statement("select CompoundSmiles,CompoundCode from mainTable where CrystalName is '{0!s}'".format(xtal))
                try:
                    LigandSmiles=str(smiles[0][0])
                    LigandCode=str(smiles[0][1])
                    elementDict_smiles=smilestools(LigandSmiles).ElementDict()
                except IndexError:
                    self.Logfile.error("{0!s}: something is seems to be wrong with the CompoundCode or SMILES string: {1!s}".format(xtal, str(smiles)))
                    continue

                pdb=pdbtools(os.path.join(xtal,'refine.pdb'))
                ligandList=pdb.ligand_details_as_list()
                for ligand in ligandList:
                    resname     = ligand[0]
                    chainID     = ligand[1]
                    resseq      = ligand[2]
                    altLoc      = ligand[3]
                    elementDict_ligand=pdb.ElementDict(resname,chainID,resseq,altLoc)
                    for element in elementDict_ligand:
                        if elementDict_ligand[element] != elementDict_smiles[element]:
                            self.Logfile.error('{0!s}: {1!s} {2!s} {3!s} {4!s} contains different number of atoms than smiles in DB: {5!s} -> {6!s}'.format(xtal, resname, chainID, resseq, altLoc, LigandSmiles, LigandCode))
                            self.update_ErrorDict(xtal, '{0!s} {1!s} {2!s} {3!s} contains different number of atoms than smiles in DB'.format(resname, chainID, resseq, altLoc))
                            break


            progress += progress_step
            self.emit(QtCore.SIGNAL('update_progress_bar'), progress)

        self.emit(QtCore.SIGNAL('show_error_dict'), self.ErrorDict)
