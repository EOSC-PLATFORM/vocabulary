
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
    listOfVocabularies = [tuple(('ID', 'Name', 'Description'))]
    for jsonObject in data:
        listOfVocabularies.append(tuple((jsonObject['id'],jsonObject['name'],jsonObject['description'])))

   # print(listOfVocabularies)
    return listOfVocabularies


def writeVocabulariesToFiles():
    for vocabularyTitle in vocabularyTitles:
        listOfVocabularies = getVocabularies(vocabularyTitle)
        # create a empty text file
        fileName = vocabularyTitle + '.rst'
        completeName = path + fileName
        fp = open(completeName, 'w', encoding="utf-8")
        fp.write(".. _"+vocabularyTitle.lower()+":\n\n")
        fp.write(vocabularyTitle.upper().replace('_',' ')+"\n")
        i = 0
        for i in range(0, len(vocabularyTitle)):
            fp.write("=")
        fp.write("\n\n")
        fp.write(tabulate(listOfVocabularies, headers='firstrow', tablefmt='rst'))

#        fp.write(''.join(str(x) for x in listOfVocabularies))
#        for line in listOfVocabularies:
#            print(*line)
#        fp.write(str(getVocabularies(vocabularyTitle)))
        fp.close()


if __name__ == '__main__':
    writeVocabulariesToFiles()