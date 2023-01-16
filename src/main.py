from parsers import BF_CSV_Parser

if __name__ == "__main__":
    bf80_caucasus = BF_CSV_Parser("data/Caucasus_80s_Objectives.csv")
    objectives = bf80_caucasus.objective_list 
    for obj in objectives:
        obj.print()
