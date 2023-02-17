import streamlit as st
import requests
import datetime
import pandas as pd

# 本ファイルはStreamlitの画面を構築（定義）するファイルである
# 本ファイル実行時に sql_app.dbが作成される

key = st.sidebar.selectbox('Pages',['利用者','施設','予約'])

if key == '利用者':
    st.title('利用者登録画面')
    with st.form(key = 'users'):
        st.write('ユーザー画面')
        # user_id: int = random.randint(0,100)
        user_name: str = st.text_input('名前',max_chars = 15)
        data = {
            # 'user_id':user_id,
            'user_name':user_name
        }
        
        # Every form must have a submit button.
        submitted = st.form_submit_button('登録')

        if submitted:
            st.write('## 送信データ')
            # st.json(data)
            st.write('レスポンス結果')
            url = 'http://127.0.0.1:8000/users'
            res = requests.post(url, json = data)
            if res.status_code == 200:
                st.success('登録完了')
            st.json(res.json())

elif key == '施設':
    st.title('施設登録画面')
    with st.form(key = 'institutions'):
        st.write('施設画面')
        # institution_id: int = random.randint(0,100)
        institution_name: str = st.text_input('名前',max_chars = 15)
        institution_capacity: int = st.number_input('定員',step = 10)
        institution_rank: int = st.number_input('施設レベル',step=1)
        institution_starttime = st.time_input('開始',value = datetime.time(hour=9,minute=0))
        institution_endtime = st.time_input('終了',value = datetime.time(hour=20,minute=0))
        
        data = {
            # 'institution_id':institution_id,
            'institution_name':institution_name,
            'institution_capacity':institution_capacity,
            'institution_rank':institution_rank,
            'institution_starttime':datetime.time(
                hour=institution_starttime.hour,
                minute=institution_starttime.minute
                ).isoformat(),
            'institution_endtime':datetime.time(
                hour=institution_endtime.hour,
                minute=institution_endtime.minute
                ).isoformat()       
        }
        
        # Every form must have a submit button.
        submitted = st.form_submit_button('登録')
        
        if submitted:
            st.write('## 送信データ')
            st.json(data)
            st.write('レスポンス結果')
            url = 'http://127.0.0.1:8000/institutions'
            res = requests.post(url, json = data)
            if res.status_code == 200:
                st.success('施設登録完了')
            st.json(res.json())

elif key == '予約':
    st.title('施設予約画面')
    
    # ユーザー一覧取得
    url = 'http://127.0.0.1:8000/users'
    # shemas.pyのUser型の要素を持つリストが返ってくる
    res = requests.get(
        url
    )
    users = res.json()
    # st.json(users)
    # {key:value} = {user_name:user_id}
    user_dict = {}
    for user in users:
        user_dict[user['user_name']]=user['user_id']
    # st.write(user_dict)
    
    # 施設一覧取得
    url = 'http://127.0.0.1:8000/institutions'
    # shemas.pyのInstitution型の要素を持つリストが返ってくる
    res = requests.get(
        url
    )
    institutions = res.json()
    # st.json(institutions)
    # {key:value} = {institution_name:institution_id}
    institution_dict = {}
    for institution in institutions:
        institution_dict[institution['institution_name']]={
            'institution_id':institution['institution_id'],
            'institution_capacity':institution['institution_capacity']
            }
    # st.write(institution_dict)
    
    st.write('## 施設一覧')
    df_institutions =  pd.DataFrame(institutions)
    df_institutions.columns = ['施設名','収容人数','施設ランク','始業時間','終業時間','施設ID']
    # st.table(df_institutions)
    
    # 予約一覧取得
    url = 'http://127.0.0.1:8000/bookings'
    # shemas.pyのbooking型の要素を持つリストが返ってくる
    res = requests.get(
        url
    )
    bookings = res.json()
    st.write('## 予約一覧')
    df_bookings =  pd.DataFrame(bookings)
    # st.write(df_bookings)
    
    user_id_dict = {}
    for user in users:
        user_id_dict[user['user_id']]=user['user_name']
    # st.write(user_id_dict)
    
    institution_id_dict = {}
    for institution in institutions:
        institution_id_dict[institution['institution_id']]=institution['institution_name']
    # st.write(institution_id_dict)

    
    # 値変換メソッド：ID⇨名前
    to_user_name = lambda x: user_id_dict[x]
    to_institution_name = lambda x: institution_id_dict[x]
    to_time = lambda x:datetime.time.fromisoformat(x).strftime('%H:%M')
    
    df_bookings['user_id'] = df_bookings['user_id'].map(to_user_name)
    df_bookings['institution_id'] = df_bookings['institution_id'].map(to_institution_name)
    df_bookings['start'] = df_bookings['start'].map(to_time)
    df_bookings['end'] = df_bookings['end'].map(to_time)

    df_bookings.columns = ['利用者名','施設名','予約人数','日付','開始時刻','終了時刻','予約ID']
    st.table(df_bookings)

    
    with st.form(key = 'bookings'):
        st.write('予約画面')
        # booking_id: int = random.randint(0,100)
        user_name = st.selectbox('予約者',user_dict.keys())
        institution_name = st.selectbox('施設名',institution_dict.keys())
        riservation_number: int = st.number_input('予約人数',step = 10,min_value=1)
        date = st.date_input('日付',value=datetime.date.today())
        start = st.time_input('開始',value = datetime.time(hour=9,minute=0))
        end = st.time_input('終了',value = datetime.time(hour=20,minute=0))
        
        data = {
            # 'booking_id':booking_id,
            # 'user_id':user_id,
            # 'institution_id':institution_id,
            'riservation_number':riservation_number,
            'date':datetime.date(
              year=date.year,
              month=date.month,
              day=date.day
              ).isoformat(),
            'start':datetime.time(
                hour=start.hour,
                minute=start.minute
                ).isoformat(),
            'end':datetime.time(
                hour=end.hour,
                minute=end.minute
                ).isoformat()       
        }
        
        # Every form must have a submit button.
        submitted = st.form_submit_button('登録')
        
        if submitted:
            user_id: int = user_dict[user_name]
            institution_id: int = institution_dict[institution_name]['institution_id']
            institution_capacity: int = institution_dict[institution_name]['institution_capacity']
            
            data = {
            'user_id':user_id,
            'institution_id':institution_id,
            'riservation_number':riservation_number,
            'date':datetime.date(
              year=date.year,
              month=date.month,
              day=date.day
              ).isoformat(),
            'start':datetime.time(
                hour=start.hour,
                minute=start.minute
                ).isoformat(),
            'end':datetime.time(
                hour=end.hour,
                minute=end.minute
                ).isoformat()       
            }
            # 予約人数チェック（定員以下であること）
            if riservation_number > institution_capacity:
                st.error('## 予約人数が定員オーバーです。')
                st.error('## 予約人数を変更してください。')
            elif start >= end:
                st.error('## 利用開始時刻が終了時刻より後になっています。')
            elif start < datetime.time(hour=9, minute=0) or end > datetime.time(hour=20, minute=0):
                st.error('## 利用可能時刻は9:00-20:00です。')            
            else:
                # 予約完了
                # st.write('## 送信データ')
                # st.json(data)
                # st.write('レスポンス結果')
                url = 'http://127.0.0.1:8000/bookings'
                res = requests.post(url, json = data)
                if res.status_code == 200:
                    st.success('予約完了')
                elif res.status_code == 404 and res.json()['detail'] == 'Already booked':
                    st.error('既に予約が入っています。')