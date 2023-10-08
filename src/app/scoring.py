import hashlib
import json


def get_score(store, phone, email, birthday=None, gender=None, first_name=None, last_name=None):
    phone = str(phone)
    key_parts = [
        first_name or "",
        last_name or "",
        phone or "",
        birthday if birthday is not None else "",
    ]
    key = "uid:" + hashlib.md5("".join(key_parts).encode()).hexdigest()
    # try get from cache,
    # fallback to heavy calculation in case of cache miss

    print("-------------------------------------")

    score = store.cache_get(key) or 0
    print("score-CACH =", score)

    if score:
        return score
    if phone:
        score += 1.5
    if email:
        score += 1.5
    if birthday and gender:
        score += 1.5
    if first_name and last_name:
        score += 0.5
    # cache for 60 minutes
    print("score-calc =", score)
    store.cache_set(key, score, 10)  # 60 * 60)
    return score


def get_interests(store, cid):
    r = store.get("i:%s" % cid)
    return json.loads(r) if r else []