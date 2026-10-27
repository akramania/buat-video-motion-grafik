#!/usr/bin/env python3
"""Apply reviewed Arabic text atomically after the harakat writer has stopped."""
import argparse
import fcntl
import json
import os
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--draft', type=Path, required=True)
    p.add_argument('--overrides', type=Path, required=True)
    p.add_argument('--lock', type=Path)
    a = p.parse_args()
    suffix = '_ar_draft.jsonl'
    if not a.lock and not a.draft.name.endswith(suffix):
        p.error('Supply the actual harakat writer lock with --lock.')
    lock = a.lock or a.draft.with_name(a.draft.name[:-len(suffix)] + '_harakat.lock')
    with lock.open('a') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        rows = [json.loads(x) for x in a.draft.read_text().splitlines() if x.strip()]
        by_id = {x['index']: x for x in rows}
        if len(by_id) != len(rows):
            raise ValueError('Duplicate draft indices')
        changes = json.loads(a.overrides.read_text())
        if not isinstance(changes, list) or len({x['index'] for x in changes}) != len(changes):
            raise ValueError('Overrides must be a list with unique indices')
        for x in changes:
            row = by_id[x['index']]
            if row['ar_official'] != x['source_ar']:
                raise ValueError('Source Arabic mismatch at index ' + str(x['index']))
            if not isinstance(x['text'], str) or not x['text'].strip():
                raise ValueError('Empty replacement')
        count = 0
        for x in changes:
            row = by_id[x['index']]
            if row.get('ar_vowelized_draft') == x['text'] and row.get('reviewed_override') and row.get('manual_review'):
                continue
            row.update(ar_vowelized_draft=x['text'], reviewed_override=True, manual_review=True)
            count += 1
        if count:
            tmp = a.draft.with_suffix(a.draft.suffix + '.tmp')
            tmp.write_text(''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in rows))
            os.replace(tmp, a.draft)
        print(json.dumps({'changed_units': count}))


if __name__ == '__main__':
    main()
