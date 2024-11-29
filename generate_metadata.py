import re
import os
import glob
import argparse

def find_files(path) -> list | None:
    try:
        files = glob.glob(os.path.join(path, "*entity*.h"), recursive=True)
        for f in files:
            print(f"File Found: {f}\n")

        return files
    except TypeError | ValueError:
        print("Invalid value passed to os.path.join or glob.")
    except OSError as e:
        print(f"OS error occurred: {e}")
    except RuntimeError as e:
        print(f"Runtime error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

def find_entities(file_path) -> list[str] | None:
    with open(file_path) as file:
            c_code = file.read()

    entities = re.findall(r"typedef struct\s+\{(.*?)\}\s+(\w+);", c_code, re.S)
    
    return entities

def get_field_descriptors(fields : list[str], entity_name : str) -> list | None:
    field_descriptors = []

    for field in fields:
        field_type = field[0]
        field_name = field[1]
        comment = field[3] or ""

        is_primary_key = 1 if "PK" in comment else 0
        is_nullable = 0 if "NOT NULL" in comment else 1

        field_descriptors.append(
            f'    {{"{field_name}", "{field_type}", offsetof({entity_name}, {field_name}), {is_nullable}, {is_primary_key}}}'
        )

    return field_descriptors

def make_table_descriptor(entity_name : str) -> str :
    return f"""
TableDescriptor {entity_name.lower()}_table = {{
    "{entity_name}",
    {entity_name.lower()}_fields,
    sizeof({entity_name.lower()}_fields) / sizeof(FieldDescriptor)
}};
    """

def make_field_descriptor(entity_name : str, field_descriptors : list) -> str : 
    field_array = f"FieldDescriptor {entity_name.lower()}_fields[] = {{\n"
    field_array += ",\n".join(field_descriptors)
    field_array += "\n};\n"

    return field_array
    
def generate_metadata(path : str) -> str:
    files = find_files(path)
    if not files:
        print("No entity files founded in the directory")
        return
    
    all_metadata = []

    for file_path in files:
        entities = find_entities(file_path) 

        if not entities:
            print(f"No entities found in the file: {file_path}")
            continue

        for entity_body, entity_name in entities:
            fields = re.findall(r"(\w+)\s+(\w+)(\[[\d]+\])?;(\s*//.*)?", entity_body)
            
            field_descriptors = get_field_descriptors(fields, entity_name)
            table = make_table_descriptor(entity_name)
            table_fields = make_field_descriptor(entity_name, field_descriptors)
            all_metadata.append(table_fields + table)
    
    return "\n".join(all_metadata)

def main():
    output_file = "metadata.c"

    parser = argparse.ArgumentParser(description="Process a value for the script.")
    parser.add_argument("-d", "--dir",type=str, help="The entities directory path to generate metadata.")
    args = parser.parse_args()

    input_directory = args.dir

    print(generate_metadata(input_directory))


if __name__ == "__main__":
    main()
