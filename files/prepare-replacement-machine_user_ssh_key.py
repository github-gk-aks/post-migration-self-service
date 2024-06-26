import openpyxl
import csv

def read_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Assuming your columns are in the order: Repository, File, Search String, Replace String
    data = [(row[0].value, row[1].value, row[2].value, row[3].value) for row in sheet.iter_rows(min_row=2)]

    return data

def prepare_replacements(data):
    replacements = {}

    for entry in data:
        repo_name, file_path, search, replace = entry

        if repo_name not in replacements:
            replacements[repo_name] = []

        replacements[repo_name].append((file_path, file_path, search, replace))

    return replacements

def write_replacements_txt(replacements):
    with open('replacements_machine_user_ssh_key.txt ', 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        for repo_name, entries in replacements.items():
            for entry in entries:
                writer.writerow([repo_name] + list(entry))

if __name__ == "__main__":
    data = read_excel("reponames_from_digital_emu_MACHINE_USER_SSH_KEY.xlsx")
    replacements = prepare_replacements(data)
    write_replacements_txt(replacements)
