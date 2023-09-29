import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from .preference_dto import Preference
from .member_dto import Member
from .routine_data_handler import routineDataHandler


class RoutineRecommender():
    routines = routineDataHandler.routines
    must_be_included = ['exc_goal_diet', 'exc_goal_healthy',  'exc_type_lower_weight', 'exc_type_upper_weight', 'exc_type_all_weight', 'exc_type_cardio', 'experience_level']

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
        cosine_sim = cosine_similarity(encoded_df.drop(columns=excluded_columns + ['rtn_seq']), input_df.drop(columns=excluded_columns))

        cosine_sim_series = pd.Series(cosine_sim[:, 0])
        top_10_similar_users = cosine_sim_series.nlargest(8)
        top_10_indices = top_10_similar_users.index
        # 추천된 루틴 가져오기

        df_rcm: pd.DataFrame = self.routines.loc[top_10_indices]
        df_rcm = df_rcm.astype(int)
        df_rcm["score"] = top_10_similar_users.values
        df_rcm["score"] = df_rcm['score'].astype(float)
        df_rcm.sort_values(by="score", ascending=False)
        return df_rcm.to_dict('records')

    def get_excluded_columns(self, preferences: Preference):
        return [
            k
            for k, v in preferences.model_dump().items()
            if k not in self.must_be_included and v != 1
        ]


recommender = RoutineRecommender()
