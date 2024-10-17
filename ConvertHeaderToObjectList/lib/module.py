from bs4 import BeautifulSoup

def calculate_table_size(html):
    soup = BeautifulSoup(html, 'html.parser')
    header_rows = soup.find('thead').find_all('tr')
    
    total_columns = 0
    total_rows = len(header_rows)
    
    for row in header_rows:
        row_columns = 0
        for cell in row.find_all(['th']):
            colspan = int(cell.get('colspan', 1))
            row_columns += colspan
        total_columns = max(total_columns, row_columns)
    
    return total_columns, total_rows

def parse_html_table(html):
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')
    header_data = []

    col_len, row_len = calculate_table_size(html)
    
    visited_map = [[False]*col_len for _ in range(row_len)]

    # 테이블 헤더 추출
    thead = soup.find('thead')
    if thead:
        rows = thead.find_all('tr')
        for row_index, row in enumerate(rows):
            cur_column = 0
            # header만 추출
            cells = row.find_all(['th'])
            for cell in cells:
                value = cell.get_text(strip=True)
                colspan = int(cell.get('colspan', 1))
                rowspan = int(cell.get('rowspan', 1))
                
                # 현재 column 위치에 헤더값 넣을 수 있는지 확인 및 피벗뛰기
                while visited_map[row_index][cur_column] == True:
                    cur_column += 1 #이미 방문한 적이 있다는 건 위 행에서 rowspan을 썻다는 의미이므로 건너 뛰기
                    if cur_column >= col_len : raise ValueError(f"{row_index+1}행 {value}열이 범위를 초과 했습니다!")  # 예외 발생

                start_col = cur_column

                # rowspan, colspan 대로 헤더 사용체크 하기
                for r in range(row_index, row_index + rowspan):
                    visited_map[r][cur_column:cur_column+colspan] = [True]*colspan
                cur_column += colspan

                end_col = cur_column

                # 헤더 정보를 추가
                header_data.append([value, row_index, row_index+rowspan-1, start_col, end_col-1])

    return header_data