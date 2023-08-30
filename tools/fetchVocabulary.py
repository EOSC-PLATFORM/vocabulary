
import requests
import xmlschema
from tabulate import tabulate

path = "../_vocabularies/"

'''
getting types for the vocabularies from schema2.xsd, from  <xs:simpleType name="vocab">
'''
schema = xmlschema.XMLSchema("../schemas/schema2.xsd")
vocabularyTitles = schema.simple_types[5].enumeration

def getVocabularies(vocabularyTitle):
    print('https://api.eosc-portal.eu/vocabulary/byType/' + vocabularyTitle)
    response_API = requests.get('https://api.eosc-portal.eu/vocabulary/byType/' + vocabularyTitle)
    # print(response_API.status_code)
    data = response_API.json()
    listOfVocabularies = [tuple(( 'Name', 'Description', 'ID', 'ParentID'))]
    for jsonObject in data:
        listOfVocabularies.append(tuple((jsonObject['name'],jsonObject['description'],jsonObject['id'],jsonObject['parentId'])))

   # print(listOfVocabularies)
    return listOfVocabularies


def writeVocabulariesToFiles():
    for vocabularyTitle in vocabularyTitles:
        listOfVocabularies = getVocabularies(vocabularyTitle)
        # create a empty text file
        fileName = vocabularyTitle + '.rst'
        completeName = path + fileName
        fpr = open(completeName + '.raw', 'w', encoding="utf-8")
        fpr.write(tabulate(listOfVocabularies, headers='firstrow', tablefmt='rst'))
        fpr.close()
        fp = open(completeName, 'w', encoding="utf-8")
        fp.write(".. _"+vocabularyTitle.lower()+":\n\n")
        fp.write(vocabularyTitle.capitalize().replace('_',' ')+"\n")
        i = 0
        for i in range(0, len(vocabularyTitle)):
            fp.write("=")
        fp.write("\n\n")
        fp.write(".. table::\n")
        fp.write("   :class: datatable\n\n")

        fpr = open(completeName + '.raw', 'r', encoding="utf-8")
        for line in fpr:
            fp.write('   ' + line)
        fpr.close()
        fp.close()


if __name__ == '__main__':
    writeVocabulariesToFiles()