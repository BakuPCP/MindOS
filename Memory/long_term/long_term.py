from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class EpisodicMemory(Base):
    """Эпизодическая память (таблица)"""
    __tablename__ = 'episodic'
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    event = Column(Text)
    emotion_tag = Column(String)

class LongTermMemory:
    def __init__(self, db_path: str):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()
        print(f"🗃️ Долгосрочная память: {db_path} подключена")

    def save_state(self):
        """Сохранение текущего состояния памяти"""
        try:
            self.session.commit()
            print("💾 Память сохранена")
        except Exception as e:
            print(f"🚨 Ошибка сохранения: {str(e)}")

    def force_save(self):
        """Экстренное сохранение (для защитных привычек)"""
        self.save_state()