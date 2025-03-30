from sqlmodel import Session, select
from sqlalchemy.engine import Engine

from src.rag.schemas import Sentence


class SentenceRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def add_sentence_couple(self, sentence1: Sentence, sentence2: Sentence) -> None:
        with Session(self.engine) as session:
            session.add(sentence1)
            session.add(sentence2)
            session.commit()

    def get_potential_translations(
        self,
        source_language: str,
        target_language: str,
        query_embedding: list[float],
        top_k: int = 4,
    ) -> list[str]:
        with Session(self.engine) as session:
            src = Sentence.__table__.alias("src")  # type: ignore
            tgt = Sentence.__table__.alias("tgt")  # type: ignore
            stmt = (
                select(
                    src.c.sentence.label("source_sentence"),
                    tgt.c.sentence.label("target_sentence"),
                    src.c.embedding.cosine_distance(query_embedding).label("distance"),
                )
                .join(tgt, (src.c.id == tgt.c.id))
                .where(src.c.language == source_language)
                .where(tgt.c.language == target_language)
                .order_by("distance")
                .limit(top_k)
            )

            results = session.exec(stmt).fetchall()

        suggestions = [r[1] for r in results]
        return suggestions
