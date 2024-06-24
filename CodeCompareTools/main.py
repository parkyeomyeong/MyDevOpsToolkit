import filecmp
import os
import re
import subprocess

# 검사 제외할 파일
EXCLUDE_FILES = [".factorypath", 
                 ".svn",
                 "wc.db", 
                 "pom.xml", 
                 ".classpath",
                 "org.eclipse.wst.common.component",
                 "DerpApplication.java", 
                 "application-dev.properties", 
                 "application.properties", 
                 "logback.xml", 
                 "dextuploadx5-configuration.js", 
                 "dextuploadnj.config",
                 "DEXTUploadNJExtensionConfiguration.java",
                 "MemberUtil.java",
                 "MemberServiceImpl.java"
                 ]

# 디렉토리 경로 설정(절대경로)
dev_directory = r'<Your Dev Project Path>'
prod_directory = r'<Your Was Project Path>'

# VS Code 실행 파일의 절대 경로
vscode_path = r"C:\Users\<UserName>\AppData\Local\Programs\Microsoft VS Code\Code.exe"

def compare_directories(dir1, dir2, dif_files, dif_files_dir, count_in_progress, total_count):
    dcmp = filecmp.dircmp(dir1, dir2)
    # 현 경로에 있는 모든 폴더, 파일 검색
    all_items = dcmp.common + dcmp.left_only + dcmp.right_only

    count_in_progress[0] += len(all_items)
    for item in all_items:
        #예외목록에 있는 파일이라면 건너뛰기
        if item in EXCLUDE_FILES : continue 
        #두개 파일 절대경로 
        item_path1 = os.path.join(dir1, item)
        item_path2 = os.path.join(dir2, item)
        
        # file이라면 다른지 검사하고 dir라면 재귀 호출
        if os.path.isfile(item_path1) and os.path.isfile(item_path2) :
            # 경로에 target이 있다면 건너뛰기(Spring에서는 빌드된 파일이므로 필요없음)
            if "target" in item_path1 or "target" in item_path2 : continue
            # 두 파일이 다른지 검사
            if not filecmp.cmp(item_path1, item_path2, shallow=False):
                dif_files.append(item)
                dif_files_dir.append([item_path1, item_path2])
        elif os.path.isdir(item_path1) and os.path.isdir(item_path2):
            compare_directories(item_path1, item_path2, dif_files, dif_files_dir, count_in_progress, total_count)
        
    percentage = (count_in_progress[0] / total_count[0]) * 100
    print(f"\rProgress: {percentage:.2f}%", end='', flush=True)

def count_total_files_in_directories(dir1, dir2, total_count):

    # 두 경로 안에 있는 
    dcmp = filecmp.dircmp(dir1, dir2)
    all_items = dcmp.common + dcmp.left_only + dcmp.right_only

    total_count[0] += len(all_items)

    for item in all_items:
        #예외목록에 있는 파일이라면 건너뛰기
        if item in EXCLUDE_FILES : continue 
        #두개 파일 절대경로 
        item_path1 = os.path.join(dir1, item)
        item_path2 = os.path.join(dir2, item)
        
        # file이라면 다른지 검사하고 dir라면 재귀 호출
        if os.path.isdir(item_path1) and os.path.isdir(item_path2):
            count_total_files_in_directories(item_path1, item_path2, total_count)

def main_function():
    dif_files = []
    dif_files_dir = []
    compare_dif_files = []
    count_in_progress, total_count = [0], [0]

    print("검사 시작!")
    count_total_files_in_directories(dev_directory, prod_directory, total_count)

    compare_directories(dev_directory, prod_directory, dif_files, dif_files_dir, count_in_progress, total_count)
    print()
    print("검사 종료!")

    total_count = 0
    for file_dir in dif_files_dir : 
        match1 = re.search(r'derp_dev(.*)', file_dir[0])
        match2 = re.search(r'derp(.*)', file_dir[1])

        if match1 and match2:
            #위 정규표현식대로 찾은 그룹이 여러개면 n을 넣으면 되는데 하나일때는 1 
            if match1.group(1) == match2.group(1):
                # print(match1.group(1))
                compare_dif_files.append(match1.group(1))
                total_count += 1
            # else :
                # print(match1.group(1), match2.group(1))

    # print(f"총 다른 개수 : {total_count}")
    return compare_dif_files, total_count

if __name__ == "__main__":

    file_pairs = []
    compare_dif_files, total_count = main_function()

    for dif_file in compare_dif_files: 
        #개발서버 -> 운영서버로 적용하기 위한 list생성 작업
        file_pairs.append((dev_directory+dif_file, prod_directory+dif_file))
        print(dif_file)
    print(f"총 다른 개수 : {total_count}")

    # 내용이 다른 파일이 없으면 그대로 종료
    if total_count == 0: exit(0)

    ## VSC에서 서로다른 파일들을 순서대로 비교하기 위한 반복문
    for file1, file2 in file_pairs:
        command = [vscode_path, '--diff', file1, file2]
        try:
            # 비교 명령어를 VS Code에 전달하여 파일 비교 새 탭 띄우기
            subprocess.run(command, check=True)

            total_count -= 1
            # 파일 비교 후 다음명령어 입력
            if input(f"다음 파일을 비교하려면 Enter, 종료하려면 x를 누르세요.  남은 파일 수 {total_count}").strip().lower() == 'x':
                print("종료되었습니다.")
                break

            print(f'Compared \n{file1} and \n{file2}')
        except subprocess.CalledProcessError as e:
            print(f'Error comparing {file1} and {file2}: {e}')
    
