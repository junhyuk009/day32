# day32_basic.py
# 주제: 배송비 견적 기록

import uuid
import psycopg
import streamlit as st
from util.print_util import pp
from day32_basic_logic import make_quote
from day32_basic_db import save_quote, list_quotes

DB_CONN_MSG = 'DB에 연결할 수 없습니다. 네트워크와 DATABASE_URL을 확인하세요.'

def show_list():
    try:
        rows = list_quotes()
        st.subheader('최신 견적 100건')
        if rows:
            st.dataframe(rows, hide_index=True)
        else:
            st.info('저장된 견적이 없습니다.')
    except psycopg.OperationalError as oe:
        pp('목록 연결 오류: ', str(oe))
        st.error(DB_CONN_MSG)
    except psycopg.Error as pe:
        pp('목록 조회 오류: ', type(pe).__name__, str(pe))
        st.error('목록 조회 실패. shipping_quotes 테이블을 확인하세요.')
    except OSError:
        st.error('sql 폴더를 확인하세요.')

def main():
    st.set_page_config(page_title='배송비 견적 기록', layout='wide')
    st.title('배송비 견적 기록')

    # 없을 때만 초기화
    if 'request_key' not in st.session_state:
        st.session_state['request_key'] = str(uuid.uuid4())
    if 'result' not in st.session_state:
        st.session_state['result'] = None
    if 'saved_id' not in st.session_state:
        st.session_state['saved_id'] = None

    with st.form('shipping'):
        title = st.text_input('견적 제목', max_chars=80)
        weight = st.number_input('배송 무게(g)', min_value=1, max_value=20000, value=1, step=1)
        submitted = st.form_submit_button('요금 계산')

    if submitted:
        try:
            st.session_state['result'] = make_quote(title, weight)
            st.session_state['request_key'] = str(uuid.uuid4())  # 새 견적 = 새 키
            st.session_state['saved_id'] = None
        except ValueError as ve:
            st.session_state['result'] = None
            st.warning(str(ve))

    result = st.session_state['result']
    if result is not None:
        st.metric('예상 요금', f"{result['fee']:,}원")
        st.caption(f"{result['title']} · {result['weight']:,}g · {result['version']}")

        saved = st.session_state['saved_id'] is not None
        if st.button('견적 저장', disabled=saved):
            try:
                rid = save_quote(result, st.session_state['request_key'])
                if rid is None:
                    st.info('이미 저장한 견적입니다.')
                else:
                    st.session_state['saved_id'] = rid
                    pp('견적 저장 완료: ', rid)
                    st.rerun()  # 버튼 비활성화와 결과 표시를 바로 반영
            except ValueError as ve:
                st.warning(str(ve))
            except psycopg.OperationalError as oe:
                pp('저장 연결 오류: ', str(oe))
                st.error(DB_CONN_MSG)
            except psycopg.Error as pe:
                pp('저장 오류: ', type(pe).__name__, str(pe))
                st.error('저장 실패. 권한/테이블을 확인하고 재시도하세요.')
            except OSError:
                st.error('sql 폴더를 확인하세요.')

    # 요구사항 4: 저장 성공 후 요금, ID, 최신 100건 표시
    if st.session_state['saved_id'] is not None and result is not None:
        st.success(f"저장 완료 · ID {st.session_state['saved_id']} · 요금 {result['fee']:,}원")
        show_list()

if __name__ == '__main__':
    main()