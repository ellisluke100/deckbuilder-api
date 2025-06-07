from bson import ObjectId


def is_valid_object_id(id: str) -> str:
    if ObjectId.is_valid(id):
        return id

    raise ValueError(f"Invalid ObjectId {id}")


def is_valid_list_of_object_id(ids: list[str]) -> list[str]:
    if all([is_valid_object_id(id) for id in ids]):
        return ids
