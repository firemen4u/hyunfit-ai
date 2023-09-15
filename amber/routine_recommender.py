import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from .api import get_member
from .preference_dto import Preference
from .member_dto import Member
from .routine_data_handler import routineDataHandler


class RoutineRecommender():
    routines = routineDataHandler.routines
    checked_cols = ['exc_type_cardio', 'exc_type_lower_weight', 'exc_type_upper_weight', 'experience_level']

    def routine_recommendations(self, member: Member):

        preferences = Preference.from_member(member)

        # 입력 사용자 프로필을 DataFrame으로 변환
        input_df = pd.DataFrame([preferences.model_dump()])

        # Label Encoding을 사용하여 범주형 데이터를 수치형으로 변환
        label_encoder = LabelEncoder()
        encoded_df = self.routines.copy()
        for col in self.routines.select_dtypes(include=['object']):
            encoded_df[col] = label_encoder.fit_transform(self.routines[col])
            input_df[col] = label_encoder.transform(input_df[col])

        excluded_columns = self.get_excluded_columns(preferences)

        # 유사도 측정 (코사인 유사도 사용)
        cosine_sim = cosine_similarity(encoded_df.drop(columns=excluded_columns), input_df.drop(columns=excluded_columns))

        cosine_sim_series = pd.Series(cosine_sim[:, 0])
        top_10_similar_users = cosine_sim_series.nlargest(10)
        top_10_indices = top_10_similar_users.index
        # 추천된 루틴 가져오기
        
        recommended_routines = self.routines.loc[top_10_indices]
        recommended_routines["score"] = top_10_similar_users.values
        print(recommended_routines)
        recommended_routines.sort_values(by="score", ascending=False)
        return recommended_routines['score'].to_list()


    def get_excluded_columns(self, preferences: Preference):
        c = []
        print(preferences.model_dump().items())
        for k, v in preferences.model_dump().items():
            if k in self.checked_cols and v == 1:
                continue
            c.append(k)
        return c


recommender = RoutineRecommender()
