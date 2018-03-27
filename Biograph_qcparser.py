#!/usr/bin/env python
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# PyWAD is open-source software and consists of a set of plugins written in python for the WAD-Software medical physics quality control software. 
# The WAD Software can be found on https://github.com/wadqc
# 
# The pywad package includes plugins for the automated analysis of QC images for various imaging modalities. 
# PyWAD has been originaly initiated by Dennis Dickerscheid (AZN), Arnold Schilham (UMCU), Rob van Rooij (UMCU) and Tim de Wit (AMC) 
#
# Description:
# This plugin parses the daily QC report (XML format) generated by the Siemens biograph TOF PET-CT.
# To send the data from the scanner to dcm4chee a separate tool that has to be installed on the scanner has been developed by Rob van Rooij and Dennis Dickerscheid.
from __future__ import print_function

__version__ = '01062015'
__author__ = 'DD'



try:
    from pydicom import tag
except ImportError:
    from dicom import tag

import xml.etree.ElementTree as ET
import lxml.etree as etree
'''
def print_xml(xmlroot):
   for child in xmlroot:
        print('=='*20)
        print(child.tag, child.attrib, child.text)
        
        for subchild in child:
            print('\t', subchild.tag, subchild.attrib, subchild.text)

            for value in subchild:
                print('\t\t', value.tag, value.attrib, value.text)
                for subvalue in value:
                    print('\t\t\t', subvalue.tag, subvalue.attrib, subvalue.text)

                    for subsubvalue in subvalue:
                        print('\t\t\t\t', subsubvalue.tag, subsubvalue.attrib, subsubvalue.text)
'''
def parseqcreport(data,results,action):

    try:
        params = action['params']
    except KeyError:
        params = {}

       
    tag_je_moeder = params.get('use_private_tag').split(',')

    #print p
    relevantfile = data.getAllInstances()[0] #data.getAllInstances()[0] oude code

    
    xmltext = relevantfile[tag.Tag(tag_je_moeder)]

    root = etree.fromstring(xmltext.value)
    #print_xml(root)

    #Sections:
    #Title
    title = root.find('aTitle')
    #Scandate
    scandate = root.find('bScandate')

    #Phantomparameters
    phantompars = root.find('cPhantomParameters')
    
    Isotope = phantompars.find('aIsotope').text
    results.addString('Isotope',Isotope)

    AssayActivity = phantompars.find('bAssayActivity').find('aValue').text
    #+phantompars.find('bAssayActivity').find('bMeasure').text
    results.addFloat('AssayActivity',AssayActivity)

    AssayDatetime = phantompars.find('cAssayDateTime').text
    results.addString('AssayDateTime',AssayDatetime)

    Volume = phantompars.find('dVolume').find('aValue').text
    results.addFloat('Volume',Volume)

    CalibrationFactor = phantompars.find('eCalibrationFactor').text
    results.addFloat('CalibrationFactor',CalibrationFactor)

    #Inputforcomputation
    compinput = root.find('dInputforComputation')



    SWversion = compinput.find('eICSSWVersion').text
    results.addString('Software version',SWversion)
    Gantrytype =compinput.find('fSystemType').text
    results.addString('Gantry type',Gantrytype)
    DailySinogram = compinput.find('aDailySinoLocation').text
    results.addString('Sinogram location',DailySinogram)
    ProposedECFval = compinput.find('bProposedECFValue').find('aValue').text
    results.addFloat('Proposed ECF',ProposedECFval)

    LastPartialSetup = compinput.find('cLastSuccessfulSetup').find('LastSetupDateTime').text
    results.addString('Last partial setup',LastPartialSetup)
    LastPartialSetupState = compinput.find('cLastSuccessfulSetup').find('LastSetupState').text
    results.addString('Last partial setup state',LastPartialSetupState)

    LastFullSetup = compinput.find('hLastSuccessfulSetup').find('LastSetupDateTime').text
    results.addString('Last full setup',LastPartialSetup)
    LastFullSetupState = compinput.find('hLastSuccessfulSetup').find('LastSetupState').text
    results.addString('Last full setup state',LastPartialSetupState)


    Partialsetupenabled = compinput.find('gPartialSetupEnabled').text
    results.addString('Partial setup enabled',Partialsetupenabled)
    ICSname =compinput.find('dICSName').text
    results.addString('ICS name',ICSname)
    

    #Results
    sectionresults = root.find('eResults')

    SystemQualityResults = sectionresults.find('aSystemQualityResults').text
    results.addString('System Quality Results',SystemQualityResults)
    QCPhantomActivity = sectionresults.find('aPhantomAgeResult').text
    results.addString('QC Phantom Activity',QCPhantomActivity)
    

    #DetailedQCreport
    detres = root.find('fDetailedSystemQualityReport').find('aItem')

    BlockNoise = detres.find('aBlockNoise').find('cBlkValue').find('aValue').text
    results.addFloat('Block Noise',BlockNoise)
    BlockEfficiency =detres.find('bBlockEfficiency').find('cBlkValue').find('aValue').text
    results.addFloat('Block Efficiency',BlockEfficiency)
    MeasuredRandoms = detres.find('cMeasureRandoms').find('cBlkValue').find('aValue').text
    results.addFloat('Measured Randoms',MeasuredRandoms)
    ScannerEfficiency = detres.find('dScannerEfficiency').find('cBlkValue').find('aValue').text
    results.addFloat('Scanner Efficiency',ScannerEfficiency)
    ScatterRatio = detres.find('eScatterRatio').find('cBlkValue').find('aValue').text
    results.addFloat('Scatter Ratio',ScatterRatio)
    ECF = detres.find('fECF').find('cBlkValue').find('aValue').text
    results.addFloat('ECF',ECF)
    ImagePlaneEfficiency = detres.find('gPlaneEff').find('cBlkValue').find('aValue').text
    results.addFloat('Plane efficiency',ImagePlaneEfficiency)
    BlockTimingOffset = detres.find('hTimeAlignment').find('cBlkValue').find('aValue').text
    results.addFloat('BlockTimingOffset',BlockTimingOffset)
    BlockTimingWidth = detres.find('iTAFWHM').find('cBlkValue').find('aValue').text
    results.addFloat('BlockTimingWidth',BlockTimingWidth)
    TimeAlignmentResidual =  detres.find('lTAResidual').find('cBlkValue').find('aValue').text
    results.addFloat('Time alignment residual',TimeAlignmentResidual)

from wad_qc.module import pyWADinput
if __name__ == "__main__":
    data, results, config = pyWADinput()

    print(config)
    for name,action in config['actions'].items():
        if name == 'parse':
            parseqcreport(data, results, action)

    results.write()
