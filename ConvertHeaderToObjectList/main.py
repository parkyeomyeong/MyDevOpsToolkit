from bs4 import BeautifulSoup
from lib.module import parse_html_table

# HTML 테이블 예시
html = '''
<table id="tb_proc" class="display" style="width:100%;overflow-x:auto;">
    <thead>
        <tr class="w3-theme-l1">
            <th style="text-align:center;font-weight:normal" colspan="11">의뢰기본정보</th>
            <th style="text-align:center;font-weight:normal" colspan="7">담당자정보</th>
            <th style="text-align:center;font-weight:normal" colspan="4" rowspan="2">종합 리드타임 정보</th>
            <th style="text-align:center;font-weight:normal" colspan="84">구간별 상세 리드타임 정보</th>
        </tr>
        <tr class="w3-theme-l1">
            <th style="text-align:center;font-weight:normal" rowspan="3">의뢰번호</th>
            <th style="text-align:center;font-weight:normal" colspan="4">상품정보 (홍보는 대표품번 정보)</th>
            <th style="text-align:center;font-weight:normal" rowspan="3">진행상태</th>
            <th style="text-align:center;font-weight:normal" rowspan="3">디자인유형</th>
            <th style="text-align:center;font-weight:normal" rowspan="3">의뢰구분</th>
            <th style="text-align:center;font-weight:normal" rowspan="3">의뢰명(품명/가품명)</th>
            <th style="text-align:center;font-weight:normal" colspan="2">패키지디자인 전용</th>
            <th style="text-align:center;font-weight:normal" colspan="2">영업회사</th>
            <th style="text-align:center;font-weight:normal" colspan="5">디자인회사</th>
            <th style="text-align:center;font-weight:normal" colspan="4" rowspan="2">의뢰 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="3" rowspan="2">RRP의뢰서검증 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="3" rowspan="2">표시기준확인 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="4" rowspan="2">의뢰 확인/접수 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="3">카피작업 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="4" rowspan="2">디자인진행 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="3" rowspan="2">시안 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="7" rowspan="2">내용확인 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="3" rowspan="2">RRP디자인검수 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="3" rowspan="2">적합성검증(매장진열) 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="3" rowspan="2">적합성검증(표시사항) 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="3" rowspan="2">OPA 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="32">최종컨펌 구간</th>
            <th style="text-align:center;font-weight:normal" colspan="9">발주 구간</th>
        </tr>
        <tr class="w3-theme-l1">
            <th style="text-align:center;font-weight:normal" rowspan="2">바이어회사</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">상품바코드</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">품번</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">디즈니여부</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">난이도</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">지침서여부</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">부서</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">담당자</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">회사</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">부서</th>
            <th style="text-align:center;font-weight:normal" colspan="2">대표담당자</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">카피담당자</th>
            <!-- 종합 리드타임 정보 -->
            <th style="text-align:center;font-weight:normal" rowspan="2">의뢰일</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">완료요청일</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">컨펌요청일</th>
            <th style="text-align:center;font-weight:normal" rowspan="2">경과일수</th>
            <!-- 카피작업구간-->
            <!-- <th style="text-align:center;font-weight:normal" colspan="3">진행단계</th> -->
            <th style="text-align:center;font-weight:normal" colspan="3">완료단계</th>
            <!-- 최종컨펌구간 -->
            <th style="text-align:center;font-weight:normal" colspan="2">전체</th>
            <th style="text-align:center;font-weight:normal" colspan="3">디자인팀장</th>
            <th style="text-align:center;font-weight:normal" colspan="3">카피팀장</th>
            <th style="text-align:center;font-weight:normal" colspan="3">디자인부서장</th>
            <th style="text-align:center;font-weight:normal" colspan="3">디자인부문장</th>
            <th style="text-align:center;font-weight:normal" colspan="3">영업팀장</th>
            <th style="text-align:center;font-weight:normal" colspan="3">영업부서장</th>
            <th style="text-align:center;font-weight:normal" colspan="3">영업부문장</th>
            <th style="text-align:center;font-weight:normal" colspan="3">상품개발팀장</th>
            <th style="text-align:center;font-weight:normal" colspan="3">상품개발부서장</th>
            <th style="text-align:center;font-weight:normal" colspan="3">상품개발부문장</th>
            <!-- 발주구간 -->
            <th style="text-align:center;font-weight:normal" colspan="3">발주요청</th>
            <th style="text-align:center;font-weight:normal" colspan="3">발주승인</th>
            <th style="text-align:center;font-weight:normal" colspan="3">발주</th>
        </tr>
        <tr class="w3-theme-l1">
            <th style="text-align:center;font-weight:normal" >사원명</th>
            <th style="text-align:center;font-weight:normal" >직급</th>
            <th style="text-align:center;font-weight:normal" >의뢰일</th>
            <th style="text-align:center;font-weight:normal" >의뢰회사</th>
            <th style="text-align:center;font-weight:normal" >의뢰부서</th>
            <th style="text-align:center;font-weight:normal" >의뢰자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >확인일</th>
            <th style="text-align:center;font-weight:normal" >확인자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >확인일</th>
            <th style="text-align:center;font-weight:normal" >확인자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >확인일</th>
            <th style="text-align:center;font-weight:normal" >확인부서</th>
            <th style="text-align:center;font-weight:normal" >확인자</th>
            <!-- <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >카피진행일</th>
            <th style="text-align:center;font-weight:normal" >진행자</th> -->
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >카피완료일</th>
            <th style="text-align:center;font-weight:normal" >완료자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >진행일</th>
            <th style="text-align:center;font-weight:normal" >진행부서</th>
            <th style="text-align:center;font-weight:normal" >진행자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >완료일</th>
            <th style="text-align:center;font-weight:normal" >완료자</th>
            <th style="text-align:center;font-weight:normal" >전체LT</th>
            <th style="text-align:center;font-weight:normal" >요청일</th>
            <th style="text-align:center;font-weight:normal" >완료일</th>
            <th style="text-align:center;font-weight:normal" >디자인LT</th>
            <th style="text-align:center;font-weight:normal" >영업LT</th>
            <th style="text-align:center;font-weight:normal" >MD-LT</th>
            <th style="text-align:center;font-weight:normal" >TQC-LT</th>
            <!-- <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >완료일</th>
            <th style="text-align:center;font-weight:normal" >완료자</th> -->
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >검수일</th>
            <th style="text-align:center;font-weight:normal" >검수자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >검증일</th>
            <th style="text-align:center;font-weight:normal" >검증자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >검증일</th>
            <th style="text-align:center;font-weight:normal" >검증자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >승인일</th>
            <th style="text-align:center;font-weight:normal" >승인자</th>
            <!-- 최종컨펌구간 -->
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >최종컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th><!-- 카피팀장 추가 -->
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >컨펌일</th>
            <th style="text-align:center;font-weight:normal" >컨펌자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <!-- 발주구간 -->
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >요청일</th>
            <th style="text-align:center;font-weight:normal" >요청자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >승인일</th>
            <th style="text-align:center;font-weight:normal" >승인자</th>
            <th style="text-align:center;font-weight:normal" >LT</th>
            <th style="text-align:center;font-weight:normal" >발주일</th>
            <th style="text-align:center;font-weight:normal" >발주자</th>
        </tr>
    </thead>
</table>
'''

def main():
    # 프로그램의 주요 로직
    header_data = parse_html_table(html)

    for data in header_data:
        print(data)

if __name__ == "__main__":
    main()