from datetime import datetime


class DailyManager:


    def __init__(self, collection):

        self.collection = collection



    # =========================
    # 新增紀錄
    # =========================

    def insert(self, data):


        date = data.get(
            "date",
            datetime.now().strftime("%Y-%m-%d")
        )


        # 找同一天資料

        existing = self.collection.find_one(
            {
                "date": date
            }
        )



        if existing:


            merged = self.merge(
                existing,
                data
            )


            self.collection.update_one(

                {
                    "_id":
                    existing["_id"]
                },


                {
                    "$set":
                    merged
                }

            )


        else:


            self.collection.insert_one(
                data
            )



    # =========================
    # 合併每日資料
    # =========================

    def merge(
        self,
        old,
        new
    ):


        result = old.copy()



        for key,value in new.items():


            if key == "_id":

                continue



            if isinstance(value,dict):


                if not isinstance(
                    result.get(key),
                    dict
                ):

                    result[key] = {}



                for k,v in value.items():


                    # 有內容才覆蓋

                    if (
                        v != ""
                        and v is not None
                    ):

                        result[key][k] = v



            else:


                if (
                    value != ""
                    and value is not None
                ):

                    result[key] = value



        result["updated_at"] = datetime.now()



        return result



    # =========================
    # Dashboard 取得資料
    # =========================

    def get_records(self):


        records = list(

            self.collection.find()
            .sort(
                "created_at",
                -1
            )

        )


        for r in records:


            self.normalize(
                r
            )



        return records




    # =========================
    # 資料格式整理
    # =========================

    def normalize(
        self,
        r
    ):


        fields = {


            "sleep":
            [
                "hours",
                "quality"
            ],



            "brain":
            [
                "adhd_start",
                "focus",
                "flow",
                "thinking_speed",
                "noise"
            ],



            "body":
            [
                "fatigue",
                "training",
                "pain",
                "recovery"
            ],



            "output":
            [
                "coding",
                "study",
                "research",
                "writing",
                "music",
                "polevault"
            ],



            "emotion":
            [
                "stress",
                "anxiety",
                "happiness",
                "confidence",
                "loneliness"
            ],



            "desire":
            [
                "urge",
                "trigger",
                "control"
            ],



            "digital":
            [
                "phone",
                "youtube",
                "shorts",
                "social"
            ],



            "reflection":
            [
                "thoughts",
                "achievement",
                "breakthrough",
                "problem",
                "cause",
                "insight",
                "idea",
                "next_action",
                "tomorrow"
            ]

        }




        for group,keys in fields.items():


            # 舊資料可能是 float/string

            if not isinstance(
                r.get(group),
                dict
            ):

                r[group] = {}



            for key in keys:


                r[group].setdefault(
                    key,
                    "-"
                )



        return r