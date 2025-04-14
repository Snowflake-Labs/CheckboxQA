import argparse
from pathlib import Path
import json
from anls_star import anls_score

def read_jsonl(file_path):
    documents = {}
    with open(file_path, 'r') as file:
        for line in file:
            doc_dict = json.loads(line)
            qas = {}
            for ann in doc_dict['annotations']:
                answer = []
                for v in ann['values']:
                    if v['value'].lower() == 'none':
                        answer.append(None)
                    else:
                        if 'value_variants' in v:
                            answer.append(tuple([a for a in v['value_variants']]))
                        else:
                            answer.append(v['value'])
                    qas[ann['key']] = answer
            documents[doc_dict['name']] = qas
    return documents

def main(pred, gold):
    gold_dict = read_jsonl(gold)
    pred_dict = read_jsonl(pred)
    score = anls_score(gold_dict, pred_dict)
    print(f'ANLS* for {pred.name}: {score:.4f}')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate predictions against gold standard.')
    parser.add_argument('--pred', type=Path, default='./data/GPT.jsonl',
                        help='Path to the directory containing prediction files')
    parser.add_argument('--gold', type=Path, default='./data/gold.jsonl',
                        help='Path to the gold standard file')

    args = parser.parse_args()
    main(args.pred, args.gold)