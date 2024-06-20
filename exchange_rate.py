import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib

from io import BytesIO # 텍스트 파일 제외한 모든 데이터 파일은 바이트파일 객체로 바꾼 뒤 작업해야 함
# io - input output 입출력

# 코드 실행에 오류는 없지만 자꾸 콘솔 찍으면 warning 떠서 안 나오게 하는 코드
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')




def ex_rate(): # main.py에서 호출하려고 함수로 만든다

    # 함수 만들기
    def get_exchange(currency_code):

        #currency_code='USD'
        last_page_num = 10
        df = pd.DataFrame() # 데이터 프레임 만들기

        for page_no in range(1,last_page_num +1): # 3페이지

            url=f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{currency_code}KRW&page={page_no}"
            dfs = pd.read_html(url, encoding='cp949', header=1) # html로 데이터 가져온다
            # header=1 헤더 2줄 나오는데 2번째 줄만 필요

            # print(dfs[0]) # 여러 페이지니까 리스트로
            # df = pd.concat([df, dfs[0]]) # 여러 데이터 이어주자

            # 예외처리
            if dfs[0].empty: # dfs 비어있을 때
                if (page_no == 1):
                    print(f"통화코드가({currency_code}) 잘못 지정되었습니다")
                else: 
                    print(f'{page_no}마지막 페이지 입니다')
                break

            df = pd.concat([df, dfs[0]], ignore_index=False)
        
        return df
        print(df)

    currency_name_dict = {'미국달러':'USD', '유럽연합 유로':'EUR', '일본 엔':'JPY', '중국 위안':'CNY', '홍콩 달러': 'HKD'}
    # currency_name = st.sidebar.selectbox('통화선택', currency_name_dict.keys())
    # clicked = st.side.button('환율 데이터 가져오기')

    currency_name = st.selectbox('통화선택', currency_name_dict.keys())
    clicked = st.button('환율 데이터 가져오기')

    if clicked: # 화면에서 버튼 클릭되면
        currency_code = currency_name_dict[currency_name] # 클릭된 키의 값을 가져옴
        df_exchange = get_exchange(currency_code)
        
        print(df_exchange)

        # 원하는 열만 선택
        df_exchange_rate = df_exchange[['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]
        df_exchange_rate2 = df_exchange_rate.set_index('날짜')
        

        # 날짜 열의 데이터 변경 
        df_exchange_rate2.index = pd.to_datetime(df_exchange_rate2.index, format='%Y_%m_%d_%H:%M:%S', errors="ignore") 
        # 인덱스(날짜 열)를 날짜 데이터로 바꿔서 인덱스로 하겠다. 그리고 날짜 포맷 형식도. 
        # 근데 뭔가 오류 나서 errors="ignore"

        # '%Y_%m_%d_%H:%M:%S'  '%Y-%m-%d'


    

        #환율 데이터 표시
        st.subheader(f'{currency_name} 환율 데이터')
        st.dataframe(df_exchange_rate2)
        # st.dataframe(df_exchange.head(20)) 20만 표시

        df_exchange_rate2.info()


        # 차트(선 그래프) 그리기
        matplotlib.rcParams['font.family']='Malgun Gothic' # 한글 나오게 설정
        ax = df_exchange_rate2['매매기준율'].plot(figsize=(15,5), grid=True)
        ax.set_title('환율(매매기준율) 그래프', fontsize=25)
        ax.set_xlabel('기간', fontsize=10)
        ax.set_ylabel(f'원화/ {currency_name}', fontsize=10)
        plt.xticks(fontsize=10) # x축 눈금값의 폰트 크키
        plt.yticks(fontsize=10) # y축 눈금값의 폰트 크키
        fig = ax.get_figure() # fig 객체 가져오기
        st.pyplot(fig)


        # 파일 다운로드 CSV, Excel 파일
        st.text('**환율 데이터 파일 다운로드**')

        # dataframe 데이터를 csv 데이터 변환 (cvs는 텍스트 파일이라 바이너리 객체로 바꿀 필요 x)
        csv_data = df_exchange_rate.to_csv()

        # dataframe 데이터를 엑셀 데이터 변환 ---> 엑셀파일은 바이너리 파일(객체)로 바꾼뒤 엑셀로 
        excel_data = BytesIO() # 메모리 버퍼(임시장소)에 바이너리 객체 생성
        df_exchange_rate.to_excel(excel_data)  # 엑셀 형식으로 버퍼에 쓰기

        col = st.columns(2) # 2개의 세로단 생성
        with col[0]:
            st.download_button('CSV 파일 다운로드', csv_data, file_name='exchange_rate_data.csv') # csv파일은 한글 깨진다
        with col[1]:
            st.download_button('엑셀 파일 다운로드', excel_data, file_name='exchange_rate_data.xlsx')
        


    else: 
        pass