import fitz
import re
import json

# PDF 파일 열기
path = r"C:\Users\wjg\Desktop\해파리\24.08.22+해파리+주간보고(16차).pdf"
doc = fitz.open(path)

# 추출한 텍스트를 담을 변수
all_text = ""

# 페이지별 텍스트 추출 및 페이지 번호 제거
for page in doc:
    text = page.get_text()
    # 페이지 번호 패턴 제거
    text = re.sub(r"-\s*\d+\s*-", "", text)
    # 정리된 텍스트를 합치기
    all_text += text

# 제주와 관련된 내용을 담을 리스트
jeju_related_info = []

# 해파리 종류와 관련된 섹션 패턴
species_patterns = {
    "노무라입깃해파리": r"노무라입깃해파리",
    "보름달물해파리": r"보름달물해파리",
    "두빛보름달해파리": r"두빛보름달해파리",
    "야광원양해파리": r"야광원양해파리",
    "유령해파리": r"유령해파리",
    "커튼원양해파리": r"커튼원양해파리",
    "기수식용해파리": r"기수식용해파리",
    "오이빗해파리": r"오이빗해파리",
    "평면해파리": r"평면해파리",
}

# 고밀도, 저밀도 출현 여부를 구분하는 패턴
density_patterns = {
    "고밀도": r"○고밀도 출현 해역",
    "저밀도": r"○저밀도 출현 해역"
}

# 제주 관련 특보 추출
jeju_special_warning = re.findall(r"제주[^\n]*특보[^\n]*", all_text)

# 제주 정보 초기화
jeju_info = {
    "출현율": {
        "노무라입깃해파리": "0%",
        "보름달물해파리": "0%",
        "기타 해파리": "0%"
    }
}

# 수정된 정규 표현식으로 제주 출현율 추출
match = re.search(r"제주\s+([\d\.\-]+)\s+(?!건\b)([\d\.\-]+)?\s+(?!건\b)([\d\.\-]+)?", all_text)
if match:
    # 그룹별로 값을 할당하며, '-' 혹은 None일 경우 "0%"로 대체
    jeju_info["출현율"]["노무라입깃해파리"] = match.group(1) + "%" if match.group(1) not in ['-', '', None] else "0%"
    jeju_info["출현율"]["보름달물해파리"] = match.group(2) + "%" if match.group(2) not in ['-', '', None] else "0%"
    jeju_info["출현율"]["기타 해파리"] = match.group(3) + "%" if match.group(3) not in ['-', '', None] else "0%"

# 각 해파리 종류와 고밀도/저밀도 출현 해역을 검색
for species, species_pattern in species_patterns.items():
    for density, density_pattern in density_patterns.items():
        # 해당 해파리와 밀도에 대한 텍스트 블록 찾기
        pattern = f"{species_pattern}[\s\S]+?{density_pattern}([\s\S]+?)(?={ '|'.join(species_patterns.values()) }|○|$)"
        matches = re.findall(pattern, all_text)
        
        if matches:
            if species in ["노무라입깃해파리", "오이빗해파리","평면해파리"]:
                jeju_matches = re.findall(r"- 제주[^\n]+", matches[0])
            else:
                jeju_matches = re.findall(r"- 제주[^\n]+", matches[1]) if len(matches) > 1 else []
                
            if jeju_matches:
                for jeju_match in jeju_matches:
                    jeju_match = jeju_match.strip()
                    jeju_match = jeju_match.split()[-2]+ ' ' + jeju_match.split()[-1]
                    jeju_related_info.append({
                        "species": species,
                        "density": density,
                        "location": jeju_match.strip(),
                    })

# JSON 데이터 생성
jeju_related_data = {
    "jeju_related_info": jeju_related_info,
    "jeju_special_warning": jeju_special_warning,
    "jeju_appearance_rate": jeju_info["출현율"]
}

# JSON으로 변환
jeju_related_json = json.dumps(jeju_related_data, ensure_ascii=False, indent=4)
print(jeju_related_json)
