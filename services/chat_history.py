import json
import os
from datetime import datetime


class ChatHistory:

    def __init__(self, history_dir="chats"):
        self.history_dir = history_dir
        os.makedirs(history_dir, exist_ok=True)

    def _filepath(self, session_id):
        return os.path.join(
            self.history_dir,
            f"{session_id}.json"
        )

    def create_session(self, session_id):

        file_path = self._filepath(session_id)

        if not os.path.exists(file_path):

            with open(file_path, "w") as f:
                json.dump([], f, indent=4)

    def load(self, session_id):

        self.create_session(session_id)

        with open(self._filepath(session_id), "r") as f:
            return json.load(f)

    def append(
        self,
        session_id,
        role,
        message,
    ):

        history = self.load(session_id)

        history.append(
            {
                "role": role,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        )

        with open(self._filepath(session_id), "w") as f:
            json.dump(
                history,
                f,
                indent=4,
                ensure_ascii=False
            )

    def clear(self, session_id):

        with open(self._filepath(session_id), "w") as f:
            json.dump([], f)

    def delete(self, session_id):

        path = self._filepath(session_id)

        if os.path.exists(path):
            os.remove(path)

    def sessions(self):

        return [
            file.replace(".json", "")
            for file in os.listdir(self.history_dir)
            if file.endswith(".json")
        ]