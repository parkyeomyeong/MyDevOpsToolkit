info

---

- 배경 : 현황 프로그램 제작할때 복잡한 헤더구조를 html로 만든 후 엑셀로도 똑같이 만들어야 하는데 이때 소요시간이 굉장히 오래걸리는 문제
  (4\*105 행 기준 하나당 30분) 따라서 html 헤더구조가 있으면 자동으로 엑셀 헤더를 만들 수 있는 Java Object 리스트를 파라메터로 제작해주는 기능 개발(엑셀 헤더 함수는 이미 공통함수로 파라메터 를 넣으면 제작하도록 개발 완료)
- FROM : html table header
- TO : Aphach POI Lib을 이용한 Excel 헤더 생성 함수

## Sudo Code

1. Html의 table > header 구조를 입력받아 헤더 총 가로 \* 세로 길이 구하기
2. 총 가로 \* 세로 길이대로 2차원 배열 맵을 생성
3. tr 기준으로 한 row씩 순차적으로 Header 구조를 맵에 적용하며 각 헤더 요소를 아래와 같이 저장
   > (value, row_start, row_end, column_start, column_end)
4. tr 개수대로 3 번 반복
5. 저장된 배열 데이터를 자바에서 사용할 Object 2차원 배열로 변형하여 출력
