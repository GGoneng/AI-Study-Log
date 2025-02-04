# --------------------------------------------------------------------
# Flask Framework에서 WebServer 구동 파일
# - 파일명 : app.py 
# --------------------------------------------------------------------
# 모듈 로딩 -----------------------------------------------------------
from .models.ProjectModule import *
from flask import Flask, render_template, request, redirect, url_for
import pymysql
from datetime import datetime

# 전역변수 ------------------------------------------------------------
# Flask Web Server 인스턴스 생성
APP=Flask(__name__)

# DB 연결 함수
def get_db_connection():
    return pymysql.connect(
        host='172.20.146.27',
        user='younghun',
        password='1234',
        db='quasar_copy',
        charset='utf8'
    )

conn = get_db_connection()

# 라우팅 기능 함수 ----------------------------------------------------
# Flask Web Server 인스턴스 변수명.route("URL")
# http://127.0.0.1:5000/
@APP.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')  # 사용자 입력 아이디
        password = request.form.get('password')  # 사용자 입력 비밀번호
        user_type = request.form.get('role')  # 사용자 유형 (개인/기관)

        if not user_type:  # 사용자 유형 선택 여부 확인
            return render_template('login.html', message="사용자 유형을 선택해주세요.")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 사용자 유형에 따른 쿼리
            if user_type == '개인':  # 개인
                query = "SELECT Member_Password FROM Member WHERE Member_ID = %s"
            elif user_type == '기관':  # 기관
                query = "SELECT Password FROM Office WHERE Office_ID = %s"
            else:
                return render_template('login.html', message="사용자 유형을 선택해주세요.")

            # 쿼리 실행
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                stored_password = result[0]
                if stored_password == password:  # 비밀번호 일치
                    if user_type == '개인':
                        return redirect(url_for('customer_mainpage'))
                    elif user_type == '기관':
                        return redirect(url_for('admin_mainpage'))
                else:
                    return render_template('login.html', message="비밀번호가 잘못되었습니다.")
            else:
                return render_template('login.html', message="ID가 잘못되었습니다.")

        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return render_template('login.html', message="데이터베이스 오류가 발생했습니다.")

    return render_template('login.html')

# http://127.0.0.1:5000/find_id
@APP.route('/find_id', methods=['GET','POST'])
def find_id():
    message = None # 기본값 설정
    if request.method == 'POST':
        # 폼 데이터 수집
        resident1 = request.form.get('resident1')
        resident2 = request.form.get('resident2')
        phone_prefix = request.form.get('phone_prefix')
        phone2 = request.form.get('phone2')
        phone3 = request.form.get('phone3')

        # 주민등록번호 및 전화번호 조합
        resident_number = f"{resident1}-{resident2}"
        phone_number = f"{phone_prefix}-{phone2}-{phone3}"

        # DB 검색
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT member_id FROM member
                WHERE registration_number = %s AND member_phone_number = %s
            """
            cursor.execute(query, (resident_number, phone_number))
            result = cursor.fetchone() # 결과 가져오기

            cursor.close()
            conn.close()

            if result:
                # 아이디를 찾은 경우
                message=f"아이디는 '{result[0]}'입니다."                
            else:
                # 아이디를 찾지 못한 경우
                message="입력된 정보와 일치하는 아이디가 없습니다. 다시 입력해주세요."

        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
    return render_template('/find_id.html', message=message)

# http://127.0.0.1:5000/find_pw
@APP.route('/find_pw', methods=['GET','POST'])
def find_pw():
    message = None # 기본값 설정
    if request.method == 'POST':
        # 폼 데이터 수집
        member_id = request.form.get('username')
        resident1 = request.form.get('resident1')
        resident2 = request.form.get('resident2')
        phone_prefix = request.form.get('phone_prefix')
        phone2 = request.form.get('phone2')
        phone3 = request.form.get('phone3')

        # 주민등록번호 및 전화번호 조합
        member = f"{member_id}"
        resident_number = f"{resident1}-{resident2}"
        phone_number = f"{phone_prefix}-{phone2}-{phone3}"

        # DB 검색
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT member_password FROM member
                WHERE member_id = %s AND registration_number = %s AND member_phone_number = %s
            """
            cursor.execute(query, (member, resident_number, phone_number))
            result = cursor.fetchone() # 결과 가져오기

            cursor.close()
            conn.close()

            if result:
                # 비밀번호를 찾은 경우
                message=f"비밀번호는 '{result[0]}'입니다."                
            else:
                # 비밀번호를 찾지 못한 경우
                message="잘못된 정보입니다. 다시 입력해주세요."

        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
    return render_template('/find_pw.html', message=message)

# http://127.0.0.1:5000/customer_gohome
@APP.route("/customer_gohome")
def customer_gohome():
    return APP.redirect("/customer_mainpage.html")

# http://127.0.0.1:5000/admin_gohome
@APP.route("/admin_gohome")
def admin_gohome():
    return APP.redirect("/admin_mainpage.html")

# http://127.0.0.1:5000/manager_mainpage
@APP.route("/admin_mainpage", methods=["GET", "POST"])
def admin_mainpage():

    '''
    # DB 연결
    '''

    # 거주자 정보 가져오기
    cur = conn.cursor()
    query = "SELECT dong, ho, water_condition FROM managed_entity"
    cur.execute(query)
    status = cur.fetchall()
    cur.close()
    # print("Fetched status data:", status) # 데이터 확인
    
    # 팝업창 띄울 샘플만들기
    cur2 = conn.cursor()
    query2 = """
        SELECT
            ho,
            managed_entity_name,
            phone_number,
            water_condition
        FROM 
            managed_entity;
        """
    cur2.execute(query2)
    popup = cur2.fetchall()
    cur2.close()

    # 오른쪽 박스에 요약 나타내기
    cur3 = conn.cursor()
    query3 = """ 
        SELECT 
            water_condition, COUNT(*) AS count
        FROM managed_entity
        WHERE dong = 101
        GROUP BY water_condition
        """
    cur3.execute(query3)
    rightbox = cur3.fetchall()
    cur3.close()

    # 위험 상태 정보 가져오기
    cur4 = conn.cursor()
    query4 = """
        SELECT ho
        FROM managed_entity
        """
    cur4.execute(query4)
    danger_result = cur4.fetchall()
    cur4.close()

    '''
    # 동 선택 부분
    '''

    # 기본적으로 101동이 선택됨
    selected_building = "101"
    if request.method == "POST":
        # POST 요청에서 선택된 동을 가져옴
        selected_building = request.form.get("building", "101")

    # 동별 상태
    building_status = {
        "101": "danger",
        "102": "normal",
        "103": "normal",
        "104": "normal",
        "105": "normal",
        "106": "normal",
        "107": "normal",
        "108": "normal",
        "109": "caution",
        "110": "normal",
    }

    # 각 동별 데이터
    floors_data = {
        "101": {
            # "1-5": [["normal", "normal"], ["normal", "danger"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            # "6-10": [["normal", "normal"], ["danger", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            # "11-15": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "danger"], ["normal", "normal"]],
            # "16-20": [["normal", "normal"], ["caution", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            # "21-25": [["danger", "danger"], ["normal", "normal"], ["danger", "normal"], ["normal", "normal"], ["normal", "normal"]],
        },
        "102": {
            "1-5": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "6-10": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "11-15": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "16-20": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "21-25": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
        },
        "103": {
            "1-5": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "6-10": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "11-15": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "16-20": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "21-25": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
        },
        "104": {
            "1-5": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "6-10": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "11-15": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "16-20": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "21-25": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
        },
        "105": {
            "1-5": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "6-10": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "11-15": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "16-20": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "21-25": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
        },
        "106": {
            "1-5": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "6-10": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "11-15": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "16-20": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "21-25": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
        },
        "107": {
            "1-5": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "6-10": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "11-15": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "16-20": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "21-25": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
        },
        "108": {
            "1-5": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "6-10": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "11-15": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "16-20": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "21-25": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
        },
        "109": {
            "1-5": [["normal", "normal"], ["normal", "caution"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "6-10": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "11-15": [["normal", "normal"], ["caution", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "16-20": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "21-25": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
        },
        "110": {
            "1-5": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "6-10": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "11-15": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "16-20": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
            "21-25": [["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"], ["normal", "normal"]],
        }
    }

    # floors_ho는 고정된 값
    floors_ho = {
        "1-5": [["101", "102"], ["201", "202"], ["301", "302"], ["401", "402"], ["501", "502"]],
        "6-10": [["601", "602"], ["701", "702"], ["801", "802"], ["901", "902"], ["1001", "1002"]],
        "11-15": [["1101", "1102"], ["1201", "1202"], ["1301", "1302"], ["1401", "1402"], ["1501", "1502"]],
        "16-20": [["1601", "1602"], ["1701", "1702"], ["1801", "1802"], ["1901", "1902"], ["2001", "2002"]],
        "21-25": [["2101", "2102"], ["2201", "2202"], ["2301", "2302"], ["2401", "2402"], ["2501", "2502"]],
    }

    '''
    # 거주자 샘플 데이터
    '''

    # resident_data = {
    #     "2101": {
    #         "member_id": "user001",
    #         "member_address": "서울특별시 강남구 도곡동",
    #         "member_phone_number": "010-1234-5678",
    #     },
    #     "2102": {
    #         "member_id": "user002",
    #         "member_address": "부산광역시 해운대구 우동",
    #         "member_phone_number": "010-9876-5432",
    #     },
    # }

    # DB 사용
    resident_data = {
        str(row[0]): {  # ho 값을 키로 사용
            "managed_entity_name": row[1],
            "phone_number": row[2],
            "water_condition": row[3],
        }
        for row in popup
    }
    
    # 선택된 동의 floors 데이터 가져오기
    floors = floors_data.get(selected_building, {})

    # # 데이터 필터링 (동에 맞는 데이터만 로드)
    # filtered_status = [
    #     row for row in status if row[0] == int(selected_building)
    # ]

    # 데이터 추가 (1층부터 25층까지)
    for floor_group in range(1, 26, 5):  # 5층 단위로 그룹화
        group_key = f"{floor_group}-{floor_group + 4}"
        floors_data["101"][group_key] = []
        if group_key not in floors_ho:
            floors_ho[group_key] = []

        for i in range(floor_group, floor_group + 5):  # 각 그룹 내 1층씩 처리
            floor_rooms = []
            floor_hos = []  # 각 층의 호수 리스트
            for j in range(1, 3):  # 방 2개씩
                ho = i * 100 + j  # 호수 계산 (101, 102, ..., 2502)
                room_status = next(
                    (row[2] for row in status if int(row[0]) == 101 and int(row[1]) == ho),
                    "normal"
                )
                floor_rooms.append(room_status)
                floor_hos.append(str(ho))
            
            # 층 데이터 추가
            floors_data["101"][group_key].append(floor_rooms)
            floors_ho[group_key].append(floor_hos)

    # combined_floors 생성 (필터링된 데이터 활용)
    # floors와 floors_ho를 개별적으로 분리
    combined_floors = {
        floor_number: [
            {"status": status, "ho": ho}
            for status_list, ho_list in zip(floor_status, floor_ho)
            for status, ho in zip(status_list, ho_list)
        ]
        for floor_number, (floor_status, floor_ho) in zip(floors.keys(), zip(floors.values(), floors_ho.values()))
    }

    '''
    오른쪽 박스 상태별 데이터
    '''
    # summary 만들기
    summary = {
        "danger": 0,
        "caution": 0,
        "normal": 0
    }
    for condition, count in rightbox:
        summary[condition] = count

    # 위험 상태 정보
    danger_info = {
        "ho": danger_result[0]
    } if danger_result else None

    return render_template(
        "admin_mainpage.html",
        building_status=building_status,
        combined_floors=combined_floors,
        selected_building=selected_building, # 선택된 동번호 전달
        floors=floors, # 층별 정보 전달
        resident_data=resident_data, # 거주자 데이터 전달
        floors_ho = floors_ho, # 호수 정보 전달
        status = status, # from DB
        summary = summary, # 전체 동 summary
        danger_info = danger_info # 위험 상태 가져오기
    )

# http://127.0.0.1:5000/customer_mainpage
@APP.route("/customer_mainpage")
def customer_mainpage():
    cur1 = conn.cursor()
    query1 = "SELECT * FROM water"
    cur1.execute(query1)
    rows1 = cur1.fetchall()
    cur1.close()

    cur2 = conn.cursor()
    query2 = "SELECT * FROM electric"
    cur2.execute(query2)
    rows2 = cur2.fetchall()
    cur2.close()

    water_model_path = r"C:\Users\KDP-2\OneDrive\바탕 화면\Python\기업 프로젝트\MyWEB\models\water_best_model_0.91.pth"
    electric_model_path = r"C:\Users\KDP-2\OneDrive\바탕 화면\Python\기업 프로젝트\MyWEB\models\electric_autoencoder_model.pth"

    # water_scaler_path = r"C:\Users\KDP-50\OneDrive\바탕 화면\KDT_DYH\15.Company_project\MyWEB\models\water_robust_scaler.pkl"
    # electric_scaler_path = r"C:\Users\KDP-50\OneDrive\바탕 화면\KDT_DYH\15.Company_project\MyWEB\models\electric_min_max_scaler.pkl"

    L = []
   # 데이터 추출

    output1 = rows1[-59:-31]
    output1 = [row[5] for row in output1]
    
    output2 = rows2[-59:-31]
    output2 = [row[5] for row in output2]

    ElecErrorMargin = []

    for elec in output2:
        if elec <= 1.4:
            ElecErrorMargin.append(0.1)
        elif elec <= 1.6:
            ElecErrorMargin.append(0.13)
        elif elec <= 2:
            ElecErrorMargin.append(0.15)

    # waterTS = preprocessing(output1, water_scaler_path)
    # electricTS = preprocessing(output2, electric_scaler_path)

    # water_df = pd.DataFrame(output1)
    # elec_df = pd.DataFrame(output2)

    water_ts = torch.FloatTensor([output1])
    elec_ts = torch.FloatTensor([output2])

    water_model = load_water_model(water_model_path)
    electric_model = load_electric_model(electric_model_path)

    predict_electric = electric_model(elec_ts).squeeze(0).tolist()

    # updated_water_value = rows1[-31:-30]
    # updated_water_value = [row[5] for row in updated_water_value]

    # updated_elec_value = rows2[-31:-30]
    # updated_elec_value = [row[5] for row in updated_elec_value]

    return render_template("/customer_mainpage.html", output = predict_electric, output1 = output1, output2 = output2, ElecErrorMargin = ElecErrorMargin)

# http://127.0.0.1:5000/register
@APP.route("/register")
def register():
    return render_template("/register.html")


# http://127.0.0.1:5000/customer_membership
@APP.route("/customer_membership", methods=['GET', 'POST'])
def customer_membership():
    if request.method == 'POST':
        # 폼 데이터 수집
        
        userid = request.form.get('userid') # 보호자 id
        password = request.form.get('password') # 보호자 pw
        guardian_name = request.form.get('guardian-name') # 보호자 이름
        address = request.form.get('address') # 보호자 주소
        
        phone_prefix = request.form.get('phone_prefix')
        phone2 = request.form.get('phone2')
        phone3 = request.form.get('phone3')

        guardian_resident1 = request.form.get('guardian-resident1')
        guardian_resident2 = request.form.get('guardian-resident2')
        guardian_resident_number = f"{guardian_resident1}-{guardian_resident2}"

        guardian_phone_number = f"{phone_prefix}-{phone2}-{phone3}"

        # 주민등록번호 및 전화번호 조합 (피보호자)
        name = request.form.get('name')
        resident1 = request.form.get('resident1')
        resident2 = request.form.get('resident2')

        phone_prefix2 = request.form.get('phone_prefix2')
        phone4 = request.form.get('phone4')
        phone5 = request.form.get('phone5')

        resident_number = f"{resident1}-{resident2}"
        phone_number = f"{phone_prefix2}-{phone4}-{phone5}"

        # DB 저장
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO member (
                    member_id,
                    member_password,
                    registration_number,
                    member_address,
                    member_phone_number,
                    managed_entity_name,
                    managed_entity_registration_number,
                    managed_entity_phone_number,
                    member_name
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                userid, 
                password, 
                resident_number, 
                address, 
                phone_number, 
                name, 
                guardian_resident_number,
                guardian_phone_number,
                guardian_name
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('customer_membership'))
        
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")

    return render_template("/customer_membership.html")

# http://127.0.0.1:5000/admin_membership
@APP.route("/admin_membership", methods=['GET', 'POST'])
def admin_membership():
    if request.method == 'POST':
        # 폼 데이터 수집
        username = request.form.get('username')
        password = request.form.get('password')
        apt_name = request.form.get('apt-name')
        apt_address = request.form.get('apt-address')
        apt_code = request.form.get('apt-codes')

        # DB 저장
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # office 테이블에 삽입
            query_office = """
                INSERT INTO office (
                office_id,
                password,
                apartment_name,
                apartment_address,
                managed_code
            )
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query_office, 
                           (username, password, apt_name, apt_address, apt_code))

            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('admin_membership'))
        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
        
    return render_template("/admin_membership.html")


# http://127.0.0.1:5000/board_admin
@APP.route("/board_admin")
def board_admin():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        query = "SELECT board_id, board_title, board_author, board_date FROM board ORDER BY board_date DESC"
        cursor.execute(query)
        boards = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("board_admin.html", boards=boards)

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return "데이터베이스 오류가 발생했습니다.", 500

# http://127.0.0.1:5000/board_customer
@APP.route("/board_customer")
def board_customer():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 게시글 리스트 가져오기
        query = "SELECT board_id, board_title, board_author, board_date FROM board ORDER BY board_date DESC"
        cursor.execute(query)
        boards = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("board_customer.html", boards=boards)

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return "데이터베이스 오류가 발생했습니다.", 500

@APP.route('/board_content/<int:board_id>')
def board_content(board_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 해당 게시물의 상세 내용 가져오기
        query = """
            SELECT board_title, board_author, board_date, board_content
            FROM board
            WHERE board_id = %s
        """
        cursor.execute(query, (board_id,))
        board = cursor.fetchone()

        cursor.close()
        conn.close()

        if board:
            # 날짜 포맷을 처리하여 템플릿에 넘기기
            board['board_date'] = board['board_date'].strftime('%Y-%m-%d')  # 날짜 형식을 '%Y-%m-%d'로 변경
            return render_template('board_content.html', board=board)
        else:
            return "게시글을 찾을 수 없습니다.", 404

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return "데이터베이스 오류가 발생했습니다.", 500

# http://127.0.0.1:5000/notice_admin
@APP.route("/notice_admin")
def notice_admin():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT announcement_title, announcement_date, announcement_id FROM announcement ORDER BY announcement_date DESC")
    announcement = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('notice_admin.html', announcement=announcement)

# http://127.0.0.1:5000/notice_customer
@APP.route('/notice_customer', methods=['GET'])
def notice_customer():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 공지사항 리스트 가져오기
        cursor.execute("SELECT * FROM announcement ORDER BY announcement_date DESC")
        announcements = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template("notice_customer.html", announcement=announcements)

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return "데이터베이스 오류가 발생했습니다.", 500

# http://127.0.0.1:5000/write_board_admin
@APP.route('/write_board_admin', methods=['GET', 'POST'])
def write_board_admin():
    if request.method == 'POST':
        title = request.form.get('board_title')  # 제목
        content = request.form.get('board_content')  # 내용

        # 필수 입력값 확인
        if not title or not content:
            return "제목과 내용을 입력하세요.", 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 데이터 삽입 쿼리 (board_id는 자동 증가, board_author는 '관리자', board_date는 현재 날짜)
            query = """
                INSERT INTO board (board_title, board_author, board_date, board_content)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (title, "관리자", datetime.now().date(), content))  # 관리자로 작성자 설정
            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('board_admin'))

        except Exception as e:
            print(f"Database error: {e}")
            return "데이터베이스 오류가 발생했습니다.", 500

    return render_template('write_board_admin.html')

# http://127.0.0.1:5000/write_board_customer
@APP.route('/write_board_customer', methods=['GET', 'POST'])
def write_board_customer():
    if request.method == 'POST':
        # 폼 데이터 처리
        title = request.form.get('board_title')  # 제목
        content = request.form.get('board_content')  # 내용

        # 필수 입력값 확인
        if not title or not content:
            return "제목과 내용을 입력하세요.", 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 데이터 삽입 쿼리 (board_id는 자동 증가, board_author는 '고객', board_date는 현재 날짜)
            query = """
                INSERT INTO board (board_title, board_author, board_date, board_content)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (title, "개인", datetime.now().date(), content))  # 고객으로 작성자 설정
            conn.commit()

            cursor.close()
            conn.close()

            # 게시글 작성 후 게시판 목록 페이지로 리다이렉트
            return redirect(url_for('board_customer'))

        except Exception as e:
            print(f"Database error: {e}")
            return "데이터베이스 오류가 발생했습니다.", 500

    # GET 요청의 경우 게시판 글쓰기 폼 렌더링
    return render_template('write_board_customer.html')

# http://127.0.0.1:5000/write_notice
@APP.route('/write_notice', methods=['GET', 'POST'])
def write_notice():
    if request.method == "POST":
        title = request.form.get("announcement_title")
        content = request.form.get("announcement_content")
        date = datetime.now().date()  # 현재 시간 자동 입력
        author = "관리자"  # 글쓴이를 "관리자"로 설정

        if not title or not content:
            return "제목과 내용을 모두 입력해야 합니다.", 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 공지사항 저장 쿼리 실행 (announcement_id는 자동으로 처리되므로 제외)
            query = """
                INSERT INTO announcement (announcement_title, announcement_content, announcement_date, announcement_author)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (title, content, date, author))  # "관리자" 값을 포함
            conn.commit()

            cursor.close()
            conn.close()

            # 저장 후 공지사항 리스트 페이지로 리다이렉트
            return redirect(url_for("notice_admin"))

        except pymysql.MySQLError as e:
            print(f"Database error: {e}")
            return "데이터베이스 오류가 발생했습니다.", 500

    # GET 요청 시 공지사항 작성 페이지 렌더링
    return render_template("write_notice.html")

@APP.route('/notice_content/<int:announcement_id>')
def notice_content(announcement_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT announcement_content, announcement_date, announcement_title, announcement_author FROM announcement WHERE announcement_id = %s", (announcement_id,))
    announcement_content = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('notice_content.html', content=announcement_content)


# 조건부 실행 ---------------------------------------------------------
if __name__ == '__main__':
    
    APP.run()