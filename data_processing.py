import spacy
import json
import glob



def create_dic(text):
    analed_text = nlp(text)

    morph_seperated = []

    for morph in analed_text:
        morph_seperated.append(str(morph.text))

    ents = []

    for ent in analed_text.ents:
        ents.append(str(ent))

    masked_texts = []
    masked_all_texts = text


    for ent in ents:
        masked_texts.append(str(text.replace(str(ent), "[MASK]")))

    for ent in ents:
        masked_all_texts = str(masked_all_texts.replace(str(ent), "[MASK]"))




    data = dict()
    data["original"] = text
    data["morphs"] = morph_seperated
    data["entity"] = ents
    data["masked"] = masked_texts
    data["masked_all"] = masked_all_texts


    return data



if __name__ == "__main__":

    path = "cnn/stories/*"

    file_list = glob.glob(path)



    data = dict()

    file_num = 0
    file_len = len(file_list)

    print("file_len is " + str(file_len))

    for file_name in file_list:
        print("--------------------------------------------------------------------------------------------")
        print(str(file_num) + "/" + str(file_len))
        if file_num == 2000:
            break

        f = open(file_name,"r")

        source_num = 0
        target_num = 0

        text = f.readline()

        nlp = spacy.load("en_core_web_sm")



        source = dict()

        target = dict()


        while text:
            text = text.replace('\n', '')
            if "@highlight"in text:
                break

            elif text:
                func_return = create_dic(text)
                source[str(source_num)] = func_return
                source_num+=1
                text = f.readline()

            else:
                text = f.readline()



        while text:
            text = text.replace('\n', '')
            if "@highlight" in text:
                text = f.readline()


            elif text:
                func_return = create_dic(text)
                target[str(target_num)] = func_return
                target_num += 1
                text = f.readline()

            else:
                text = f.readline()
        temp_list = [source, target]

        data[str(file_num)] = temp_list
        file_num += 1

        print(data)



    with open("data.json","w+",encoding="utf-8") as j:
        json.dump(data, j, indent="\t")

    with open("data.json","r") as j:
        json_data = json.load(j)

    print(json.dumps(json_data,indent="\t"))


