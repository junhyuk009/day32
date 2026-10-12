# day32_basic_logic.py
# 배송비 계산: streamlit, psycopg를 import하지 않는 순수 함수

VERSION = 'shipping-v1'
BASE_WEIGHT = 1000   # 기본 구간(g)
BASE_FEE = 3000      # 기본 요금(원)
STEP_FEE = 1000      # 추가 구간당 요금(원)

def calc_fee(weight):
    if weight <= BASE_WEIGHT:
        return BASE_FEE
    # 초과분을 1000g 단위로 올림 → 시작된 구간 수
    extra_steps = (weight - BASE_WEIGHT + BASE_WEIGHT - 1) // BASE_WEIGHT
    return BASE_FEE + extra_steps * STEP_FEE

def make_quote(title, weight):
    title = (title or '').strip()
    if not title or len(title) > 80:
        raise ValueError('견적 제목을 1~80자로 입력하세요. (공백만 입력할 수 없습니다)')
    if isinstance(weight, bool) or not isinstance(weight, int):
        raise ValueError('무게는 정수로 입력하세요.')
    if not 1 <= weight <= 20000:
        raise ValueError('무게는 1~20000g 사이로 입력하세요.')
    return {
        'title': title,
        'weight': weight,
        'fee': calc_fee(weight),
        'version': VERSION,
    }