import pandas as pd
import json


class DataIssueDetector:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.file_type = None

    def load_data(self):
        if self.file_path.endswith('.csv'):
            self.data = pd.read_csv(self.file_path, engine='python')
            self.file_type = 'csv'
        elif self.file_path.endswith('.json'):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.file_type = 'json'
        else:
            raise ValueError('Unsupported file type')

    def detect_missing_values(self):
        if self.file_type == 'csv':
            return self.data.isnull().sum().to_dict()
        elif self.file_type == 'json':
            issues = {}
            if isinstance(self.data, list):
                for idx, item in enumerate(self.data):
                    for k, v in item.items():
                        if v is None:
                            issues.setdefault(k, []).append(idx)
            return issues
        return {}

    def detect_duplicates(self):
        if self.file_type == 'csv':
            return self.data.duplicated().sum()
        elif self.file_type == 'json':
            if isinstance(self.data, list):
                seen = set()
                dup_count = 0
                for item in self.data:
                    item_str = json.dumps(item, sort_keys=True)
                    if item_str in seen:
                        dup_count += 1
                    else:
                        seen.add(item_str)
                return dup_count
        return 0
