import pandas as pd


def total_column(matrix):
    df = pd.DataFrame(matrix)
    return df.sum(axis=0)


def div_column_with_total_sum(matrix, total):
    df = pd.DataFrame(matrix)
    return df.div(total, axis=1)


def avg_row(matrix):
    df = pd.DataFrame(matrix)
    return df.mean(axis=1)


def mul_row(matrix, avg):
    df = pd.DataFrame(matrix)
    return df * avg.values.reshape(-1, 1)


def total_row(matrix):
    df = pd.DataFrame(matrix)
    return df.sum(axis=1)


def div_column(column1, column2):
    df1 = pd.DataFrame(column1)
    df2 = pd.DataFrame(column2)
    return df1/df2


def get_ri(n):
    """Trả về giá trị Random Index (RI) tương ứng với số tiêu chí"""
    ri_values = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
                 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    return ri_values.get(n, 1.49)  # Mặc định lấy giá trị RI cho n ≥ 10


def read_file():
    file_excel = input("Nhập đường dẩn tệp excel: ")
    file_excel = file_excel.replace("\\", "/")
    try:
        df = pd.read_excel(file_excel, index_col=0)
        matrix = df.map(lambda x: eval(str(x))).values
    except Exception as e:
        print("Có lỗi trong quá trình đọc tệp excel. Hãy kiểm tra lại tệp!")
        print("Lỗi: ", e)
        return
    try:
        total_matrix = total_column(matrix)
        div_total_matrix = div_column_with_total_sum(matrix, total_matrix)
        criteria_weights = avg_row(div_total_matrix)
        mul_avg_matrix = mul_row(matrix, criteria_weights)
        weighted_sum = total_row(mul_avg_matrix)
        consistency_vector = div_column(weighted_sum, criteria_weights)
        lamda_max = consistency_vector.mean()
        n = consistency_vector.size
        ri = get_ri(n)
        cr = (lamda_max - n)/(n - 1)/ri
        if cr.item() < 0.1:
            print(f"CR = {cr.item():.4f} nhỏ hơn 10%, chấm điểm phù hợp!")
        else:
            print(f"CR = {cr.item():.4f} lớn hơn 10%, chấm điểm không phù hợp!")
    except Exception as e:
        print("Có lỗi trong tính toán. Hãy kiểm tra lại tệp excel!")
        print("Lỗi: ", e)


path = "F:/my_project/python/AHP/Matrix.xlsx"
read_file()
