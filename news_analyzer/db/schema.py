from enum import Enum, unique

from sqlalchemy import (
    Column,
    ForeignKey,
    MetaData,
    String,
    Table,
    Integer,
    Identity,
    Numeric,
    Text,
    DateTime,
    Enum as DbEnum,
)

convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    # Именование индексов
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    # Именование уникальных индексов
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    # Именование CHECK-constraint-ов
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    # Именование внешних ключей
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    # Именование первичных ключей
    "pk": "pk__%(table_name)s",
}
metadata = MetaData(naming_convention=convention)


@unique
class TextSourceType(str, Enum):
    rss = "rss"
    file = "file"


@unique
class EntityType(Enum):
    LOC = "LOC"
    ORG = "ORG"
    PER = "PER"


articles_sources_table = Table(
    "articles_sources",
    metadata,
    Column(
        "src_id",
        Integer,
        Identity(start=1),
        primary_key=True,
    ),
    Column("name", String, unique=True),
    Column("src_type", DbEnum(TextSourceType)),
    Column("src", String),
)

articles_table = Table(
    "articles",
    metadata,
    Column("article_id", Integer, Identity(start=1), primary_key=True),
    Column(
        "src_id",
        Integer,
        ForeignKey("articles_sources.src_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("title", String(500), nullable=False),
    Column("text", Text, nullable=False),
    Column("date", DateTime, nullable=False),
    Column("neutral_sentiment", Numeric(6, 5, asdecimal=False), nullable=False),
    Column("negative_sentiment", Numeric(6, 5, asdecimal=False), nullable=False),
    Column("positive_sentiment", Numeric(6, 5, asdecimal=False), nullable=False),
    Column("skip_sentiment", Numeric(6, 5, asdecimal=False), nullable=False),
    Column("speech_sentiment", Numeric(6, 5, asdecimal=False), nullable=False),
)

named_entities_table = Table(
    "named_entities",
    metadata,
    Column("entity_id", Integer, Identity(start=1), primary_key=True),
    Column(
        "article_id",
        Integer,
        ForeignKey("articles.article_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("name", String(500), nullable=False),
    Column("entity_type", DbEnum(EntityType), nullable=False),
)
