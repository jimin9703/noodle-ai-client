import re

from text_processing.repository.text_processing_repository import TextProcessingRepository


class TextProcessingRepositoryImpl(TextProcessingRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    async def postprocessingTextToBacklogs(self, generatedBacklogsText):
        # 각 백로그 항목을 분리하여 반복 처리
        backlogs = re.split(r'(?=\*\*백로그 제목:\*\*)', generatedBacklogsText)

        # 첫 번째 백로그가 빈 값일 수 있으므로 필터링
        backlogs = [backlog for backlog in backlogs if backlog.strip()]

        # 각 항목에서 정보를 추출하여 리스트에 저장
        backlogList = []
        for backlog in backlogs:
            backlogTitle = re.search(r'\*\*백로그 제목:\*\*\s*(.*)', backlog)
            if backlogTitle is None:
                continue
            domainName = re.search(r'\+ 도메인 이름:\s*`(.*)`', backlog)
            successCriteria = re.search(r'\*\*Success Criteria:\*\*\s*(.*)', backlog)

            # To-do 목록에서 "도메인"이나 "Success Criteria"로 시작하는 문장을 제외하고, 앞에 붙은 \t나 공백 제거
            todoList = re.findall(r'^\s*\d+\.\s*(?!도메인|Success Criteria)(.*)', backlog, re.MULTILINE)

            # 앞에 붙은 탭이나 공백 제거
            todoList = [todo.strip() for todo in todoList]

            backlog_data = {
                '백로그 제목': backlogTitle.group(1) if backlogTitle else None,
                '도메인 이름': domainName.group(1) if domainName else None,
                'Success Criteria': successCriteria.group(1) if successCriteria else None,
                'To-do 목록': todoList if todoList else None
            }
            backlogList.append(backlog_data)

        return backlogList
