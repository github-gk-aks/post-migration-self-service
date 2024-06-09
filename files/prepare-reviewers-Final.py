import openpyxl
import csv

def read_excel(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    column_names = [cell.value for cell in sheet[1]]

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(row)

    return column_names, data

def prepare_replacements(column_names, data):
    repo_index = column_names.index('Repository')
    reviewers_index = [i for i, col_name in enumerate(column_names) if col_name.startswith('Reviewer')]

    replacements = {}

    for entry in data:
        repo_name = entry[repo_index]
        reviewers = [entry[i] for i in reviewers_index if entry[i] is not None]

        if repo_name not in replacements:
            replacements[repo_name] = []

        reviewer_str = ' '.join(reviewers)
        replacements[repo_name].append(reviewer_str)

    return replacements

def write_replacements_txt(replacements):
    with open('reviewers.txt', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        for repo_name, reviewers_list in replacements.items():
            for reviewers_str in reviewers_list:
                writer.writerow([repo_name] + reviewers_str.split())

if __name__ == "__main__":
    column_names, data = read_excel("Prepare_Reviewers.xlsx")
    replacements = prepare_replacements(column_names, data)
    write_replacements_txt(replacements)
