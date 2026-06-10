def should_use_thor(work: dict) -> bool:
    return work.get('work_intent',{}).get('verb') in {'plan','review'}
